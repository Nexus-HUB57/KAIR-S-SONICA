# Credenciais, tokens e webhooks — Meta/Instagram e TikTok

## Meta/Instagram

Fontes oficiais consultadas:

1. Instagram Platform: https://developers.facebook.com/documentation/instagram-platform
2. Instagram API with Instagram Login — Get Started: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/get-started
3. Instagram API with Facebook Login for Business — Get Started: https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/get-started
4. Access Token: https://developers.facebook.com/documentation/instagram-platform/reference/access_token
5. Setup Webhooks Subscriptions: https://developers.facebook.com/documentation/instagram-platform/webhooks
6. Content Publishing: https://developers.facebook.com/docs/instagram-api/guides/content-publishing
7. Comment Moderation: https://developers.facebook.com/docs/instagram-api/guides/comment-moderation

A Meta oferece duas rotas principais: Instagram API com Business Login for Instagram, para contas Instagram Business ou Creator, e Instagram API com Facebook Login for Business, para contas profissionais ligadas a uma Facebook Page. A plataforma permite obter/publicar mídia, gerenciar e responder comentários, receber menções e usar webhooks; a conta precisa ser profissional [1].

O guia Business Login for Instagram informa que o app deve ser do tipo Business. O token gerado pelo App Dashboard é long-lived e válido por 60 dias; tokens do fluxo de login podem ser short-lived e válidos por uma hora. O endpoint `/me?fields=user_id,username` retorna o ID profissional e o username da conta [2].

O endpoint `GET https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=<APP_SECRET>&access_token=<SHORT_TOKEN>` troca o token de curta duração por token longo. O app secret só deve ser usado no servidor, nunca no cliente, binário ou dispositivo [4].

No caminho Facebook Login for Business, é necessário ter conta profissional, Facebook Page conectada, usuário com Tasks na Page e app registrado. O fluxo usa `/me/accounts` para obter Pages e depois `/{page-id}?fields=instagram_business_account` para obter o Instagram User ID conectado [3].

Para publicação, a documentação atual descreve `/<IG_ID>/media` para criar container e `/<IG_ID>/media_publish` para publicar. A mídia precisa estar em URL pública no momento da tentativa [6]. Para comentários, o app pode ler comentários, responder, ocultar/exibir e apagar, com permissões específicas e webhooks `comments`/`live_comments` [7].

Para webhooks Meta, o endpoint deve aceitar GET de verificação com `hub.mode=subscribe`, `hub.challenge` e `hub.verify_token`, respondendo o challenge somente quando o verify token coincidir. Eventos POST devem validar `X-Hub-Signature-256` usando HMAC-SHA256 com o App Secret e responder `200 OK`. A Meta informa que o app deve estar em Live Mode; comments/live_comments exigem Advanced Access; a conta profissional que possui a mídia deve ser pública para notificações de comentários/menções [5].

## TikTok

Fontes oficiais consultadas:

8. Login Kit for Web: https://developers.tiktok.com/doc/login-kit-web/
9. User Access Token Management: https://developers.tiktok.com/doc/oauth-user-access-token-management
10. Content Posting API — Get Started: https://developers.tiktok.com/doc/content-posting-api-get-started
11. Content Posting API — Direct Post: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post
12. Content Posting API — Get Post Status: https://developers.tiktok.com/doc/content-posting-api-reference-get-video-status
13. TikTok Webhook Events: https://developers.tiktok.com/doc/webhooks-events
14. TikTok Webhook Verification: https://developers.tiktok.com/doc/webhooks-verification

No Login Kit web, o app deve ser registrado no portal de desenvolvedores, e o client key/client secret ficam disponíveis no portal. O redirect URI precisa ser HTTPS, absoluto, estático, registrado no produto Login Kit e não pode conter parâmetros ou fragmentos. O fluxo deve usar um state anti-CSRF e comparar o state recebido no callback [8].

O callback devolve um authorization code. O servidor troca o code em `POST https://open.tiktokapis.com/v2/oauth/token/` usando `client_key`, `client_secret`, `code`, `grant_type=authorization_code` e `redirect_uri`. A resposta contém `open_id`, `scope`, `access_token`, `expires_in`, `refresh_token` e `refresh_expires_in`. O TikTok informa que o access token expira em cerca de 24 horas e pode ser renovado sem novo consentimento usando o refresh token; ambos devem permanecer no backend [9].

Para publicação direta, o app precisa do produto Content Posting API, configuração Direct Post, escopo `video.publish`, autorização do usuário e aprovação desse escopo. O fluxo consulta creator info, inicializa `/v2/post/publish/video/init/`, envia arquivo ou usa `PULL_FROM_URL` com URL pública verificada e consulta `/v2/post/publish/status/fetch/`. Clientes não auditados ficam restritos a conteúdo privado até passarem pelo processo de auditoria [10] [11].

A documentação do TikTok oferece Fetch Status e Content Posting webhooks. Eventos incluem `post.publish.failed`, `post.publish.complete`, `post.publish.publicly_available` e `post.publish.no_longer_publicaly_available`. Webhooks devem validar o header `TikTok-Signature`, que usa timestamp e assinatura HMAC-SHA256 sobre `timestamp + "." + raw_body`; payloads fora da janela tolerável devem ser rejeitados [12] [13] [14].

## Implicações para o KTD Social Orchestrator

O repositório já contém os adapters, as rotas `/v1/social/webhooks/meta` e `/v1/social/webhooks/tiktok`, armazenamento de agenda e variáveis server-side. Para ativar publicação real, ainda é necessário preencher secrets no ambiente de execução, configurar URLs públicas HTTPS, concluir os fluxos OAuth e testar primeiro em modo privado/simulado. Nenhum token deve ser enviado por chat, colocado no Git ou registrado em logs.
