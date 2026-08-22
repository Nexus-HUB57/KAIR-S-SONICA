# Publicação agendada via GitHub Actions — KTD Social Orchestrator v1

## Resultado

O repositório possui dois caminhos:

| Caminho | Uso |
|---|---|
| `social-publish.yml` | Publicação avulsa manual via `workflow_dispatch` |
| `social-scheduled-dispatch.yml` | A cada cinco minutos, chama o serviço HTTPS persistente e despacha agendas vencidas |

O segundo workflow não contém tokens Meta/TikTok. Ele envia somente um token interno de scheduler ao endpoint HTTPS. O serviço persistente lê as credenciais das plataformas no seu próprio secret manager e executa `SocialScheduleStore.dispatch_due()`.

> GitHub Actions não é o servidor que recebe webhooks nem a fonte de verdade da agenda. O workflow é um relógio externo que acorda o serviço persistente. O GitHub documenta que `schedule` pode sofrer atrasos em períodos de alta carga; a agenda deve usar `run_at` em UTC, idempotência e tolerância operacional [1] [2].

## Pré-requisitos

Antes de ativar a publicação agendada, confirme:

1. A API KTD está publicada em domínio HTTPS persistente.
2. O serviço mantém o banco de agenda entre reinícios. A implementação atual usa SQLite e, portanto, precisa de filesystem persistente; em Cloud Run/serverless, migrar para Firestore, Cloud SQL, DynamoDB ou outro datastore antes de produção.
3. Meta e TikTok já possuem tokens válidos e permissões oficiais.
4. O asset está em URL HTTPS pública, estável e acessível pelos provedores.
5. O conteúdo tem estado `approved` ou `released`.
6. O endpoint interno de dispatch exige `KTD_SOCIAL_SCHEDULER_TOKEN`.

## Passo 1 — criar o Environment

No GitHub, abra:

```text
Settings → Environments → New environment → production-social
```

O GitHub libera Environment secrets somente para jobs que referenciam o Environment e depois das regras configuradas [3]. Para a autonomia diária, não é necessário exigir aprovação em cada postagem. É possível proteger apenas a alteração do ambiente com branch/tag permitida, wait timer ou reviewer na ativação inicial.

## Passo 2 — cadastrar a URL e o token interno

Cadastre `KTD_SOCIAL_API_BASE_URL` como variable do Environment:

```bash
gh variable set KTD_SOCIAL_API_BASE_URL \
  --env production-social \
  --body "https://social.example.com"
```

Cadastre o token interno de scheduler de forma interativa:

```bash
gh secret set --env production-social KTD_SOCIAL_SCHEDULER_TOKEN
```

O valor desse token deve ser criado aleatoriamente, ser diferente dos tokens Meta/TikTok e existir também no secret manager do serviço HTTPS. Nunca coloque o valor em `--body`, commit, URL, log ou issue.

## Passo 3 — cadastrar os secrets das plataformas

No mesmo Environment, configure os secrets OAuth já obtidos nos portais oficiais:

```bash
gh secret set --env production-social KTD_INSTAGRAM_ACCESS_TOKEN
gh secret set --env production-social KTD_INSTAGRAM_APP_SECRET
gh secret set --env production-social KTD_TIKTOK_ACCESS_TOKEN
gh secret set --env production-social KTD_TIKTOK_CLIENT_SECRET
gh secret set --env production-social KTD_META_WEBHOOK_VERIFY_TOKEN
```

Configure a variável não secreta:

```bash
gh variable set KTD_INSTAGRAM_USER_ID \
  --env production-social \
  --body "<INSTAGRAM_USER_ID_CONFIRMADO>"
```

Não forneça os valores reais ao agente por chat. O GitHub recomenda referenciar secrets pelo contexto `secrets`, evitar exposição em linha de comando e usar variáveis de ambiente no step [4].

## Passo 4 — validar os tokens

Abra **Actions → Social · token health → Run workflow**. Selecione `production-social` quando aplicável e execute.

O workflow consulta o perfil Instagram e o `creator_info` TikTok, mas não publica. O resultado esperado é semelhante a:

```text
instagram_token_ok username=khairusktd_ofc account_type=...
tiktok_token_ok creator_info_ok=true
```

Ele não deve imprimir access token, refresh token, App Secret, Client Secret ou payload completo.

## Passo 5 — criar uma agenda

O serviço persistente expõe:

```text
POST /v1/social/schedules
```

Envie um request com `schedule_at` em UTC, `execute_actions=true`, asset HTTPS e estado editorial aprovado:

```bash
curl --fail-with-body --request POST \
  --url "https://social.example.com/v1/social/schedules" \
  --header "Authorization: Bearer <TOKEN_ADMIN_DO_SERVICO>" \
  --header "Content-Type: application/json" \
  --data '{
    "objective": "Publish the approved KTD short for the Single 11 launch",
    "campaign_id": "single-11-model-a-premiere-2026-08-30",
    "platforms": ["instagram", "tiktok"],
    "autonomy_mode": "autonomous",
    "peer_mode": "optional",
    "content_intent": "launch",
    "asset_refs": ["https://cdn.example.com/ktd/single-11-model-a.mp4"],
    "schedule_at": "2026-08-30T18:00:00Z",
    "execute_actions": true,
    "include_llm": false,
    "include_rag": true,
    "content_state": "approved",
    "metadata": {
      "song_title": "I Won’t Waste This Life",
      "source": "scheduled-campaign"
    }
  }'
```

O token administrativo acima é um placeholder e não deve ser enviado ao GitHub Actions como texto de workflow. O serviço deve autenticar essa rota com o mecanismo administrativo adotado no ambiente.

Liste agendas para confirmar:

```bash
curl --fail-with-body \
  --url "https://social.example.com/v1/social/schedules?status=SCHEDULED" \
  --header "Authorization: Bearer <TOKEN_ADMIN_DO_SERVICO>"
```

## Passo 6 — executar um dispatch manual de teste

Abra **Actions → Social · scheduled dispatch → Run workflow**. O workflow chama:

```text
POST /v1/social/schedules/dispatch-due?limit=10
X-KTD-Scheduler-Token: <secret interno>
```

Se não houver agenda vencida, a resposta esperada é `200` com `count: 0`. Para testar sem publicar, use primeiro uma agenda com `execute_actions=false` ou execute somente o workflow `Social · dry run`. Para publicação real, o request agendado precisa ter `execute_actions=true` e `content_state=approved` ou `released`.

## Passo 7 — ativar o schedule

O arquivo `.github/workflows/social-scheduled-dispatch.yml` já contém:

```yaml
"on":
  workflow_dispatch:
  schedule:
    - cron: "*/5 * * * *"
```

O intervalo de cinco minutos é o menor intervalo documentado pelo GitHub para schedules. O workflow roda com o commit mais recente do default branch e pode ser atrasado, especialmente no início da hora [1] [2]. Portanto, `schedule_at` significa “não publicar antes de”, com atraso possível, e não uma garantia de precisão de segundo.

Para horários editoriais críticos, o worker do serviço persistente deve ser o mecanismo de disparo principal, e o GitHub Actions deve permanecer como fallback/controle. Para uma primeira versão simples, o schedule de cinco minutos é suficiente para posts comuns.

## Passo 8 — observar e interromper

Monitore a aba **Actions**, os logs do serviço HTTPS e os estados da agenda:

```text
SCHEDULED → CLAIMED → PUBLISHED
                    ├─ PARTIAL
                    ├─ FAILED
                    └─ DEAD_LETTER
```

O workflow usa `concurrency` para evitar duas execuções simultâneas. O serviço marca a agenda após o resultado e usa claim idempotente. Se houver publicação incorreta ou erro de API, desative temporariamente o workflow no GitHub; o GitHub documenta a desativação como medida para evitar chamadas incorretas ou consumo desnecessário [5].

## Limitações importantes

O GitHub Actions não é adequado para receber callbacks Meta/TikTok, manter filas em memória ou garantir publicação em segundo exato. Os webhooks continuam apontando para `/v1/social/webhooks/meta` e `/v1/social/webhooks/tiktok` no serviço HTTPS persistente. O workflow também não renova automaticamente tokens OAuth nesta versão; o token store do ambiente deve tratar refresh e expiração.

A implementação atual marca agendas SQLite, mas SQLite em disco local não é apropriado como fonte de verdade em um runtime serverless com filesystem descartável. Antes de executar Cloud Run com scale-to-zero, substitua o store por um datastore gerenciado ou use um volume persistente compatível.

## Referências oficiais

[1]: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions — GitHub Docs, Workflow syntax for GitHub Actions.

[2]: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule — GitHub Docs, Events that trigger workflows — schedule.

[3]: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment — GitHub Docs, Managing environments for deployment.

[4]: https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions — GitHub Docs, Using secrets in GitHub Actions.

[5]: https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow — GitHub Docs, Disabling and enabling a workflow.
