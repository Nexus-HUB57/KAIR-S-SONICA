# KTD Social Orchestrator — receptor HTTPS serverless v1

## Recomendação

Usar um **receptor HTTPS stateless gerenciado** para Meta/Instagram e TikTok, mantendo o processamento do KTD Social Orchestrator fora do caminho crítico do webhook. O receptor valida o handshake ou a assinatura, calcula uma chave idempotente, grava o evento mínimo em uma fila/banco gerenciado e responde rapidamente. Um worker/função separado processa o evento, atualiza a memória social e chama o agente peer quando necessário.

Essa arquitetura evita administrar um servidor próprio 24/7. Cloud Run oferece endpoint HTTPS estável, TLS gerenciado, autoscaling e scale-to-zero; seu filesystem é descartável, portanto estado deve ficar fora do container [1]. AWS Lambda Function URLs são adequadas para webhooks leves; API Gateway é preferível quando são necessários recursos adicionais de autenticação, validação e controle [2] [3].

## Fluxo

```text
Meta/TikTok
    │ HTTPS webhook
    ▼
Ingress Function / Cloud Run Service
    ├─ valida GET challenge ou assinatura HMAC
    ├─ rejeita payload inválido
    ├─ cria event_id + idempotency_key
    ├─ persiste payload mínimo
    └─ responde 200 rapidamente
          │
          ▼
Managed Queue / Database
    │
    ▼
Async Worker / Cloud Run Job / Lambda
    ├─ classifica evento
    ├─ deduplica
    ├─ chama SocialOrchestrator
    ├─ executa ou agenda ação conforme policy
    ├─ grava resultado e erro
    └─ retry com backoff
```

## Componentes mínimos

| Componente | Responsabilidade | Persistência |
|---|---|---|
| Ingress HTTPS | GET/POST Meta e POST TikTok, validação HMAC, resposta rápida | nenhuma local |
| Event store | payload mínimo, headers relevantes, event ID, status e timestamps | Firestore, Cloud SQL, DynamoDB, S3 + índice ou equivalente |
| Queue | desacoplar resposta do processamento | Pub/Sub, Cloud Tasks, SQS, EventBridge ou equivalente |
| Worker | chamar RAG, LLM, política, peer e adapters | stateless; escreve no event store |
| Token store | access/refresh tokens e expiração | secret manager, nunca Git ou logs |
| GitHub Actions | deploy, dry-run, health check, migrações e manutenção de baixa frequência | não recebe webhook diretamente |

## Rotas do repositório

O FastAPI atual já expõe:

```text
GET  /v1/social/webhooks/meta
POST /v1/social/webhooks/meta
POST /v1/social/webhooks/tiktok
```

Para um primeiro deployment, o mesmo container pode servir essas três rotas como Ingress Service. O worker não deve executar dentro da mesma requisição. O adapter atual pode continuar no código principal, mas o armazenamento de agenda/eventos deve migrar do SQLite local para datastore externo quando o runtime for serverless.

## Contrato de recebimento

### Meta/Instagram

- GET: validar `hub.mode=subscribe` e `hub.verify_token`; responder apenas `hub.challenge` quando o token coincidir.
- POST: validar `X-Hub-Signature-256` com HMAC-SHA256 e App Secret.
- Extrair objeto, entry IDs, change fields, event timestamp e comment/message ID.
- Gravar hash do corpo e `event_id` antes de enfileirar.
- Responder `200` somente depois da persistência mínima.

A Meta informa que eventos podem ser reenviados e recomenda deduplicação; o receptor não deve disparar duas respostas para o mesmo evento [4].

### TikTok

- POST: validar `TikTok-Signature` com timestamp e HMAC-SHA256 sobre `timestamp + "." + raw_body`.
- Extrair evento, `publish_id` e timestamps.
- Gravar o evento antes de enfileirar.
- Responder `200` para evento autenticado e aceito.
- Manter `status/fetch` como fallback para eventos não recebidos.

## Segurança

O endpoint deve ser público somente no caminho dos webhooks. Rotas administrativas, publicação manual e leitura de métricas devem exigir autenticação separada. O receptor deve limitar tamanho de body, rejeitar JSON malformado, aplicar janela de timestamp TikTok, validar conteúdo bruto antes de parsear, não registrar tokens nem payloads completos e mascarar identificadores sensíveis nos logs.

Os access tokens Meta/TikTok devem ser lidos de um secret manager no runtime. GitHub Actions pode usar Environment Secrets para deploy e health checks; OIDC deve ser usado para autenticar no provedor de nuvem quando disponível, evitando uma chave longa de deploy [5] [6].

## Retries e estados

```text
RECEIVED → VERIFIED → PERSISTED → QUEUED
                         ├─ PROCESSED
                         ├─ IGNORED
                         ├─ RETRY_WAIT
                         └─ DEAD_LETTER
```

O worker deve usar uma chave idempotente composta por plataforma, evento/provider ID e tipo de evento. Falhas transitórias usam backoff exponencial limitado. Falhas de autenticação, assinatura inválida, conteúdo proibido ou capability ausente não devem ser repetidas indefinidamente; entram em `DEAD_LETTER` e alertam o operador.

## Escolha prática

| Opção | Como funciona | Trade-off | Adequação ao KTD |
|---|---|---|---|
| **Cloud Run + datastore/fila gerenciada** | Empacota o FastAPI atual como container; autoscaling e HTTPS gerenciados | Requer conta/projeto Google Cloud e configuração de datastore | Melhor continuidade com o FastAPI existente |
| **API Gateway + Lambda + fila** | Gateway recebe webhook, Lambda valida e envia para fila | Mais componentes e mudança de runtime/adapters | Boa opção se o ambiente já for AWS |
| **Function URL + Lambda** | Uma função recebe e processa o webhook leve | Menos proteção/controle que API Gateway; exige disciplina de persistência | Apenas para MVP de baixo volume |

A recomendação inicial é **Cloud Run Service para o Ingress + Cloud Tasks/Pub/Sub + datastore gerenciado**, porque preserva o FastAPI atual e evita um host 24/7. A decisão final depende de qual provedor de hospedagem o operador já possui.

## Implantação por GitHub

1. GitHub Actions constrói e testa o container.
2. O workflow usa OIDC para autenticar no provedor, quando possível.
3. O deploy publica uma nova revisão do Ingress Service.
4. O workflow valida `/health`, o handshake Meta em ambiente de teste e a validação de assinatura com fixture local.
5. O domínio HTTPS da revisão é registrado nos portais Meta/TikTok.
6. O workflow de produção não imprime secrets e não envia payloads reais de teste.
7. O worker e o event store são provisionados como recursos externos ao filesystem do container.

## Não fazer

Não usar GitHub Actions como endpoint do webhook. Não deixar o webhook executar LLM, publicação ou resposta de comentário na mesma requisição. Não armazenar tokens em GitHub Issues, workflow logs, artefatos, imagens Docker ou arquivos `env` versionados. Não depender de SQLite local como fonte de verdade em runtime serverless. Não habilitar publicação pública enquanto o app Meta/TikTok estiver em modo de teste ou sem o estado editorial apropriado.

## Referências

[1]: https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run — Google Cloud, What is Cloud Run.

[2]: https://docs.aws.amazon.com/lambda/latest/dg/urls-webhook-tutorial.html — AWS Lambda, Creating a webhook endpoint using a Lambda function URL.

[3]: https://docs.aws.amazon.com/serverless/latest/devguide/starter-apigw.html — AWS, Get started with API Gateway.

[4]: https://developers.facebook.com/documentation/instagram-platform/webhooks — Meta, Setup Webhooks Subscriptions.

[5]: https://docs.github.com/en/actions/security/guides/using-secrets-in-github-actions — GitHub Docs, Using secrets in GitHub Actions.

[6]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers — GitHub Docs, Configuring OpenID Connect in cloud providers.
