# KTD Social Orchestrator — manual operacional v1

## Estado atual

O módulo está implementado no pacote `kairos_core.social` e exposto no gateway FastAPI em `/v1/social`. O modo padrão é seguro: planeja ações, valida contratos e não publica porque `execute_actions` é `false`. A autonomia real depende das credenciais e permissões oficiais das contas `@khairusktd_ofc` e `@ktd_oficial`.

O Single 11 continua sujeito à avaliação humana da Prova 2. Portanto, seus posts não devem ser executados com `content_state: approved` ou `released` até que exista aprovação explícita do conteúdo correspondente.

## Capabilities

```bash
curl -s http://localhost:8000/v1/social/capabilities | python3 -m json.tool
```

A resposta informa modo híbrido, perfis-alvo, módulos, providers configurados, LLM e políticas. `configured: true` significa somente que a variável de ambiente existe; ainda é necessário validar OAuth, permissões e o account ID no provedor.

## Planejamento seguro

```bash
curl -s -X POST http://localhost:8000/v1/social/run \
  -H 'Content-Type: application/json' \
  -d '{
    "objective": "prepare a short old-school rap launch package for KTD",
    "campaign_id": "single-11",
    "platforms": ["instagram", "tiktok"],
    "autonomy_mode": "simulate",
    "peer_mode": "optional",
    "content_intent": "launch",
    "asset_refs": ["https://cdn.example.test/ktd-short.mp4"],
    "include_rag": true,
    "include_llm": false,
    "execute_actions": false,
    "content_state": "candidate",
    "metadata": {
      "song_title": "I Won’t Waste This Life",
      "audience": "listeners of narrative old-school rap"
    }
  }' | python3 -m json.tool
```

Esse fluxo retorna evidências RAG, estratégia, pacotes por plataforma, ações, handoffs peer e plano de métricas. O asset precisa ser trocado por um caminho/URL real quando a campanha estiver pronta.

## Autonomia híbrida

`simulate` apenas calcula e valida. `collaborative` cria handoffs para `pr-risk`, `brand-guardian` e `analytics`, mantendo a decisão disponível para reconciliação. `autonomous` permite execução quando `execute_actions: true`, desde que o conteúdo seja `approved` ou `released`, o provider esteja configurado e a política autorize.

A autonomia não permite publicar prova musical pendente, disparar DM proativa por padrão, comprar mídia, aceitar parceria comercial ou responder casos de crise. Esses casos entram em `BLOCKED` ou `ESCALATE`.

## Configuração de providers

Copie `config/social/env.example` para o ambiente de execução. Nunca coloque tokens reais em `config`, no Git ou em logs. O Instagram exige conta profissional, fluxo de login Meta e permissões de publicação. A mídia precisa estar publicamente acessível para que a Meta consiga buscá-la durante a criação do container [1].

O TikTok exige aplicativo registrado, produto Content Posting, escopo `video.publish`, autorização do usuário e aprovação do cliente para sair das restrições de cliente não auditado. Para publicação por URL, o domínio/URL prefix precisa estar verificado [2] [3].

## Interações de comunidade

### Instagram

```bash
curl -s -X POST http://localhost:8000/v1/social/interaction \
  -H 'Content-Type: application/json' \
  -d '{
    "platform": "instagram",
    "operation": "fetch_comments",
    "media_id": "IG_MEDIA_ID",
    "execute": true
  }'
```

A API oficial documenta leitura de comentários, respostas, ocultação/exclusão e webhooks `comments`/`live_comments`; o adapter usa essas capacidades quando o token tiver as permissões correspondentes [4].

### TikTok

A v1 não inventa um endpoint normal para responder comentários TikTok. A documentação pública localizada para consulta de comentários pertence ao Research API e requer escopo de pesquisa; esse caminho não deve ser tratado como capability de gerenciamento comercial sem autorização específica [5].

### Triagem local

```bash
curl -s -X POST http://localhost:8000/v1/social/community/triage \
  -H 'Content-Type: application/json' \
  -d '{"text":"I won’t waste this life either."}' | python3 -m json.tool
```

A triagem local classifica comentários como `positive`, `question`, `general`, `spam`, `privacy`, `crisis` ou `safety`. Casos de privacidade, crise, ameaça ou discurso de ódio devem ser escalados, nunca convertidos em copy promocional.

## Webhook TikTok

O endpoint `/v1/social/webhooks/tiktok` verifica `TikTok-Signature` com HMAC-SHA256 e rejeita payloads fora da janela de tolerância. A aplicação deve ser publicada em HTTPS e o endpoint deve ser configurado no TikTok Developer Portal. Webhooks são preferíveis para status final; polling do endpoint `status/fetch` permanece como fallback [3] [6].

## Checklist de ativação real

1. Confirmar que o asset é aprovado, tem hash registrado e atende ao formato do canal.
2. Configurar tokens em secret manager do ambiente, nunca no repositório.
3. Validar `KTD_INSTAGRAM_USER_ID` e permissões Meta.
4. Validar token TikTok, `video.publish`, domínio verificado e auditoria do app.
5. Fazer uma publicação privada/de teste conforme as regras do provedor.
6. Confirmar status por webhook ou polling e registrar o ID do provedor.
7. Só então habilitar `execute_actions: true` para uma campanha pequena.
8. Medir publicação, comentários, compartilhamentos, alcance, views e retorno ao asset completo.
9. Reavaliar a política antes de ampliar frequência ou automatizar respostas.

## Referências

[1]: https://developers.facebook.com/docs/instagram-api/guides/content-publishing — Meta for Developers, “Content Publishing”.

[2]: https://developers.tiktok.com/doc/content-posting-api-get-started — TikTok for Developers, “Get Started — Direct Post”.

[3]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post — TikTok for Developers, “Direct Post”.

[4]: https://developers.facebook.com/docs/instagram-api/guides/comment-moderation — Meta for Developers, “Comment Moderation”.

[5]: https://developers.tiktok.com/doc/research-api-specs-query-video-comments — TikTok for Developers, “Query Video Comments”.

[6]: https://developers.tiktok.com/doc/content-posting-api-reference-get-video-status — TikTok for Developers, “Get Post Status”.
