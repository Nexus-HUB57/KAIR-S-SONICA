# KTD Social Orchestrator — credenciais, tokens e webhooks v1

**Objetivo:** habilitar publicação real e recebimento de eventos para `@khairusktd_ofc` no Instagram e `@ktd_oficial` no TikTok sem expor secrets no chat, no GitHub ou no cliente.

> **Regra de segurança:** nunca envie access tokens, refresh tokens, app secrets, client secrets ou códigos OAuth nesta conversa. O procedimento abaixo usa placeholders deliberados; os valores reais devem ser inseridos apenas no secret manager do ambiente de execução.

## 1. O que o orquestrador espera

| Plataforma | Variáveis secretas | Identificadores não secretos | Recursos implementados |
|---|---|---|---|
| Meta/Instagram | `KTD_INSTAGRAM_ACCESS_TOKEN`, `KTD_INSTAGRAM_APP_SECRET` | `KTD_INSTAGRAM_USER_ID`, `KTD_META_WEBHOOK_VERIFY_TOKEN` | Reels, comentários, respostas, insights, handshake Meta e validação HMAC |
| TikTok | `KTD_TIKTOK_ACCESS_TOKEN`, `KTD_TIKTOK_CLIENT_SECRET` | `KTD_TIKTOK_PRIVACY_LEVEL` | Creator info, Direct Post por URL pública verificada, status e validação HMAC de webhook |

O client key do TikTok também será necessário durante o fluxo OAuth/refresh. Na versão atual, ele deve ser usado pelo componente de autenticação/renovação do ambiente; não deve ser colocado em uma URL de callback ou em um arquivo versionado.

A implementação encontra-se em `packages/kairos_core/social/platforms/`, e as rotas ficam em `/v1/social`. O conteúdo só pode ser publicado se o request usar `execute_actions=true`, os providers estiverem configurados e `content_state` for `approved` ou `released`.

## 2. Hospedagem obrigatória

Webhooks exigem um endpoint público em HTTPS com certificado válido. O sandbox local/efêmero não deve ser usado para receber callbacks. Use o ambiente persistente já escolhido para a API ou uma hospedagem HTTPS equivalente, com:

| Requisito | Meta/Instagram | TikTok |
|---|---|---|
| URL pública HTTPS | obrigatória | obrigatória para callback OAuth e webhooks |
| Rota | `GET/POST /v1/social/webhooks/meta` | `POST /v1/social/webhooks/tiktok` |
| Persistência | armazenar payload/event ID e deduplicar | armazenar publish ID/event ID e deduplicar |
| Resposta | challenge em GET; `200` em POST válido | `200` em evento válido |

O domínio exato deve ser decidido antes de registrar os callbacks. Não use o endereço temporário do sandbox como endpoint de produção.

## 3. Meta/Instagram — caminho recomendado

Para a conta `@khairusktd_ofc`, primeiro confirme no Instagram que a conta é **Business ou Creator profissional**. A Meta documenta dois caminhos: **Instagram API com Instagram Login/Business Login for Instagram**, sem depender de uma Facebook Page, e **Instagram API com Facebook Login for Business**, que exige conta profissional ligada a uma Page e usuário com Tasks nessa Page [1] [2].

### 3.1 Criar e configurar o app Meta

1. Entre em [Meta for Developers](https://developers.facebook.com/) com a conta proprietária da marca.
2. Crie um app do tipo **Business** quando o fluxo Instagram Login solicitar esse tipo.
3. Adicione o produto Instagram e configure o Login/Business Login for Instagram.
4. Registre o callback OAuth HTTPS do orquestrador, por exemplo `https://social.example.com/auth/meta/callback`.
5. Solicite somente as permissões que serão usadas. Para publicar e gerenciar a comunidade, valide as permissões atuais no painel e na referência oficial; o conjunto esperado para o caminho Business Login inclui `instagram_business_basic`, `instagram_business_content_publish` e, para comentários/insights, permissões de gerenciamento correspondentes [1] [3].
6. Adicione a conta Instagram de teste e conclua o login/consentimento.
7. Faça App Review/Advanced Access quando a Meta exigir para usar a conta em Live Mode. Webhooks de `comments`/`live_comments` exigem Advanced Access; a documentação também exige o app em Live Mode para receber notificações [4].

### 3.2 Obter o token e o Instagram User ID

No App Dashboard, use a área de configuração do Instagram para gerar um token de teste para `@khairusktd_ofc`, ou implemente o fluxo OAuth no callback registrado. O guia oficial informa que o token do Dashboard é long-lived por 60 dias; tokens short-lived podem ter validade de uma hora [1].

Troque um token short-lived por long-lived somente no backend:

```bash
curl -G 'https://graph.instagram.com/access_token' \
  --data-urlencode 'grant_type=ig_exchange_token' \
  --data-urlencode 'client_secret=<META_APP_SECRET>' \
  --data-urlencode 'access_token=<SHORT_LIVED_INSTAGRAM_TOKEN>'
```

Não coloque o `client_secret` em frontend, aplicativo móvel, script distribuído ou histórico de shell. A resposta contém o token longo e `expires_in`; guarde ambos no secret manager e programe renovação antes da expiração [5].

Obtenha o ID profissional e confirme o username usando:

```bash
curl -G 'https://graph.instagram.com/v26.0/me' \
  --data-urlencode 'fields=user_id,username,account_type' \
  --data-urlencode 'access_token=<INSTAGRAM_USER_ACCESS_TOKEN>'
```

O valor retornado em `user_id` deve ser colocado como `KTD_INSTAGRAM_USER_ID`. Confirme que o `username` corresponde a `khairusktd_ofc` antes de habilitar publicação [1].

### 3.3 Ativar webhooks Meta

O endpoint `GET /v1/social/webhooks/meta` usa `KTD_META_WEBHOOK_VERIFY_TOKEN` para responder ao challenge. No painel Meta:

1. Abra o produto Webhooks do app.
2. Cadastre a URL `https://<dominio>/v1/social/webhooks/meta`.
3. Informe o mesmo verify token configurado somente no secret manager.
4. Inscreva os campos realmente necessários, inicialmente `comments`; adicione `live_comments`, `mentions` ou `messages` somente quando as permissões e o fluxo de atendimento estiverem prontos.
5. Vincule/assine a conta profissional ao app conforme o guia da Meta.
6. Use o botão de teste do painel e confirme que o endpoint responde o challenge e `200` para eventos válidos.

No POST, a Meta envia `X-Hub-Signature-256: sha256=<digest>`. O adapter calcula HMAC-SHA256 sobre o corpo bruto com `KTD_INSTAGRAM_APP_SECRET`. O payload deve ser persistido com um identificador de deduplicação antes de disparar qualquer resposta. A Meta informa que eventos podem ser reenviados; o sistema deve tratar reentrega de forma idempotente [4].

### 3.4 Caminho alternativo Facebook Login for Business

Use este caminho somente se a conta já estiver conectada a uma Facebook Page e o operador tiver Tasks adequadas. O fluxo oficial é: obter User Access Token, consultar `/me/accounts`, identificar a Page, consultar `/{page-id}?fields=instagram_business_account` e usar o IG User ID retornado [2]. Esse caminho normalmente envolve permissões de Page, App Review e Business Verification adicionais.

## 4. TikTok — OAuth e Content Posting API

### 4.1 Criar e configurar o app

1. Abra [TikTok for Developers](https://developers.tiktok.com/) e crie ou abra o app da operação KTD.
2. Ative **Login Kit for Web** e registre o callback HTTPS estático, por exemplo `https://social.example.com/auth/tiktok/callback`.
3. Ative **Content Posting API** e configure Direct Post.
4. Solicite o escopo `video.publish` e os escopos de identidade realmente necessários.
5. Verifique o domínio/URL prefix que será usado para `PULL_FROM_URL`.
6. Submeta o app à auditoria exigida pelo TikTok. Clientes não auditados podem ficar restritos a conteúdo privado e limitações de teste [6] [7].

O Login Kit exige `state` anti-CSRF, callback HTTPS, URI absoluta, estática, previamente registrada e sem fragmentos ou parâmetros dinâmicos [8].

### 4.2 Trocar authorization code por token

O callback OAuth devolve um `code`. O backend troca esse code em:

```bash
curl --location --request POST 'https://open.tiktokapis.com/v2/oauth/token/' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'client_key=<TIKTOK_CLIENT_KEY>' \
  --data-urlencode 'client_secret=<TIKTOK_CLIENT_SECRET>' \
  --data-urlencode 'code=<AUTHORIZATION_CODE>' \
  --data-urlencode 'grant_type=authorization_code' \
  --data-urlencode 'redirect_uri=https://social.example.com/auth/tiktok/callback'
```

Guarde `open_id`, `scope`, `access_token`, `expires_in`, `refresh_token` e `refresh_expires_in` no backend. A documentação do TikTok informa que o access token expira em cerca de 24 horas e pode ser renovado com `grant_type=refresh_token`; implemente renovação antecipada e rotação sem interromper a fila [9].

O orquestrador deverá usar:

```text
KTD_TIKTOK_ACCESS_TOKEN=<access token atual>
KTD_TIKTOK_CLIENT_SECRET=<client secret do app>
KTD_TIKTOK_PRIVACY_LEVEL=PUBLIC_TO_EVERYONE
```

O client key, refresh token e os timestamps de expiração devem ficar no componente seguro de OAuth/token store. Não reutilize refresh token no frontend nem o escreva em logs.

### 4.3 Testar publicação

Antes de usar `PUBLIC_TO_EVERYONE`, chame `creator_info` e confirme as opções de privacidade devolvidas. Faça primeiro um teste com escopo e visibilidade permitidos pelo app. O fluxo Direct Post inicializa o post, recebe `publish_id` e consulta status; o asset precisa estar numa URL pública/permitida quando usado `PULL_FROM_URL` [6] [7].

O endpoint local de publicação recusa caminhos de arquivo e exige URL HTTP(S). Isso é intencional: o próximo componente deve fazer upload para armazenamento público controlado, registrar checksum e só então enviar a URL ao TikTok.

### 4.4 Ativar webhooks TikTok

No portal do app, abra a configuração de webhooks, informe `https://<dominio>/v1/social/webhooks/tiktok` e selecione os eventos de Content Posting necessários, especialmente conclusão e falha. O endpoint valida `TikTok-Signature` com o client secret e HMAC-SHA256 sobre `timestamp + "." + raw_body`; rejeita timestamp antigo e assinatura inválida. Mantenha polling de `status/fetch` como fallback para eventos perdidos [10] [11].

## 5. Inserir os valores sem expô-los

### Ambiente local seguro

Use um arquivo fora do repositório, com permissão restrita:

```bash
install -d -m 700 /etc/ktd-social
install -m 600 /dev/null /etc/ktd-social/credentials.env
# editar /etc/ktd-social/credentials.env no host seguro
```

O arquivo deve conter os valores reais apenas no host de execução. Não o copie para `config/social/env.example`, não o anexe ao chat e não execute `env`/`printenv` em logs.

### Secret manager/CI

No ambiente persistente, crie secrets com nomes equivalentes aos campos do `config/social/env.example`. No GitHub Actions, use **Settings → Secrets and variables → Actions** e injete secrets somente no job de deploy/runtime. Não coloque secrets em `docker-compose.yml`, imagem Docker, artefato, URL, issue ou pull request.

Depois de injetar os valores, reinicie o serviço de forma controlada e valide apenas flags não secretas:

```bash
curl -s https://<dominio>/v1/social/capabilities | python3 -m json.tool
```

A resposta deve mostrar `configured: true` para o provider correspondente, mas não deve mostrar token, secret ou payload completo.

## 6. Ordem de ativação recomendada

1. Configurar HTTPS e testar health/readiness do serviço.
2. Criar o app Meta e o app TikTok, registrar callbacks e completar OAuth.
3. Confirmar os IDs não secretos: `KTD_INSTAGRAM_USER_ID`, TikTok `open_id` e domínio de mídia.
4. Inserir secrets no secret manager.
5. Validar `/me?fields=user_id,username,account_type` na Meta e `creator_info` no TikTok.
6. Habilitar webhooks e validar handshake/assinatura com payload de teste.
7. Rodar `/v1/social/run` em `simulate` com asset aprovado.
8. Fazer um teste real de baixa exposição, respeitando as limitações de cada app.
9. Só depois habilitar `execute_actions=true` para a campanha.
10. Monitorar expiração, refresh, retries, duplicidades, status de publicação e eventos rejeitados.

## 7. O que preciso receber do operador

Não preciso receber tokens no chat. Para a próxima etapa, basta informar os estados não secretos: se o Instagram é Business/Creator, se existe Facebook Page conectada, se o app Meta está em Development ou Live, se o TikTok app tem Content Posting e `video.publish` aprovados, qual é o domínio HTTPS de produção e se o secret manager já foi preenchido. Com esses estados, o próximo passo pode ser um smoke test sem revelar credenciais.

## 8. Operação pelo GitHub Actions

O repositório agora contém três workflows separados:

| Workflow | Gatilho | Ação externa |
|---|---|---|
| `social-dry-run.yml` | manual ou dias úteis | nenhuma; valida planejamento e política |
| `social-token-health.yml` | manual ou diário | consulta `/me` do Instagram e `creator_info` do TikTok |
| `social-publish.yml` | somente `workflow_dispatch` | publica em Instagram e TikTok quando o Environment e os secrets estão configurados |

Configure no repositório `Nexus-HUB57/KAIR-S-SONICA` um Environment chamado `production-social`. Coloque nele `KTD_INSTAGRAM_ACCESS_TOKEN`, `KTD_INSTAGRAM_APP_SECRET`, `KTD_TIKTOK_ACCESS_TOKEN`, `KTD_TIKTOK_CLIENT_SECRET`, `KTD_META_WEBHOOK_VERIFY_TOKEN` e demais secrets necessários. Coloque `KTD_INSTAGRAM_USER_ID` como Environment variable não secreta. O workflow de publicação usa apenas `workflow_dispatch`, exige `content_state=approved` ou `released`, valida URL HTTPS e não é acionado por push ou pull request.

O GitHub suporta secrets de repositório e de Environment; secrets de Environment só são liberados para jobs que referenciam esse Environment e depois das regras de proteção configuradas [12]. Para o primeiro deploy, é recomendável usar branch/tag de produção restrita e um wait timer ou required reviewer no Environment. Isso não torna a operação diária manual: depois de liberado, o job pode executar de forma autônoma conforme a política do orquestrador.

Para acessar o ambiente persistente, prefira OIDC do GitHub em vez de uma chave longa de deploy quando o provedor de hospedagem oferecer suporte. OIDC exige `id-token: write` e uma relação de confiança que limite repositório, branch e Environment [13]. OIDC autentica o deploy; ele não substitui os tokens OAuth da Meta/TikTok, que continuam no secret manager do runtime.

O workflow `social-token-health.yml` não publica. Ele serve para detectar token ausente, conta Instagram incorreta e falha no `creator_info` TikTok. O GitHub Actions pode atrasar schedules em períodos de carga; por isso, o health check é uma verificação complementar, não um substituto para os webhooks ou para o token store persistente [14].

## Referências oficiais

[1]: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/get-started — Meta, Instagram API with Instagram Login — Get Started.

[2]: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/get-started — Meta, Instagram API with Facebook Login for Business — Get Started.

[3]: https://developers.facebook.com/docs/instagram-api/guides/content-publishing — Meta, Instagram Content Publishing.

[4]: https://developers.facebook.com/documentation/instagram-platform/webhooks — Meta, Setup Webhooks Subscriptions.

[5]: https://developers.facebook.com/documentation/instagram-platform/reference/access_token — Meta, Access Token.

[6]: https://developers.tiktok.com/doc/content-posting-api-get-started — TikTok, Content Posting API — Get Started.

[7]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post — TikTok, Content Posting API — Direct Post.

[8]: https://developers.tiktok.com/doc/login-kit-web/ — TikTok, Login Kit for Web.

[9]: https://developers.tiktok.com/doc/oauth-user-access-token-management — TikTok, User Access Token Management.

[10]: https://developers.tiktok.com/doc/content-posting-api-reference-get-video-status — TikTok, Get Post Status.

[11]: https://developers.tiktok.com/doc/webhooks-events — TikTok, Webhook Events.

[12]: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment — GitHub Docs, Managing environments for deployment.

[13]: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-cloud-providers — GitHub Docs, Configuring OpenID Connect in cloud providers.

[14]: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule — GitHub Docs, Events that trigger workflows — schedule.
