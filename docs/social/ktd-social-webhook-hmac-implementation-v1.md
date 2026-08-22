# KTD Social Orchestrator — validação HMAC-SHA256 v1

## Princípio central

A assinatura deve ser calculada sobre o **corpo bruto recebido**, antes de `json.loads()`, normalização de whitespace ou reserialização. Alterar o corpo antes da validação muda os bytes e invalida a assinatura. Em ambos os provedores, a comparação final deve usar `hmac.compare_digest`, não `==`, para evitar comparação não constante.

O segredo nunca deve ser colocado no código, no cliente, no workflow YAML ou no log. Leia-o do secret manager/runtime:

```text
KTD_INSTAGRAM_APP_SECRET=<App Secret Meta>
KTD_TIKTOK_CLIENT_SECRET=<Client Secret TikTok>
```

## 1. Meta/Instagram: `X-Hub-Signature-256`

A Meta envia um header no formato:

```text
X-Hub-Signature-256: sha256=<64 caracteres hexadecimais>
```

A assinatura é o HMAC-SHA256 do corpo bruto usando o App Secret da aplicação. Uma implementação isolada em Python é:

```python
from __future__ import annotations

import hashlib
import hmac


def verify_meta_signature(
    *,
    signature_header: str,
    raw_body: bytes,
    app_secret: str,
) -> bool:
    if not app_secret:
        raise ValueError("App Secret ausente")

    prefix = "sha256="
    if not signature_header.startswith(prefix):
        return False

    received = signature_header[len(prefix):].strip()
    if len(received) != hashlib.sha256().digest_size * 2:
        return False

    try:
        int(received, 16)
    except ValueError:
        return False

    expected = hmac.new(
        app_secret.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(received, expected)
```

No repositório, essa lógica está em `InstagramProvider.verify_webhook_signature()`. O endpoint FastAPI deve preservar o corpo bruto:

```python
from fastapi import Header, Request
from fastapi.responses import JSONResponse


@router.post("/v1/social/webhooks/meta")
async def meta_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None),
):
    raw_body = await request.body()
    if not x_hub_signature_256:
        return JSONResponse({"error": "signature_missing"}, status_code=401)

    provider = InstagramProvider()
    if not provider.verify_webhook_signature(
        signature_header=x_hub_signature_256,
        raw_body=raw_body,
    ):
        return JSONResponse({"error": "signature_invalid"}, status_code=401)

    payload = json.loads(raw_body)
    await persist_and_enqueue("meta", payload, raw_body)
    return {"received": True}
```

O GET de verificação da Meta é um fluxo separado; ele não usa HMAC. A aplicação deve conferir `hub.verify_token` e devolver `hub.challenge` somente quando os valores coincidirem.

## 2. TikTok: `TikTok-Signature`

O TikTok usa um header com campos separados por vírgulas:

```text
TikTok-Signature: t=<unix_timestamp>,s=<hex_signature>
```

O material assinado é a concatenação do timestamp, um ponto e o corpo bruto como UTF-8:

```text
signed_payload = timestamp + "." + raw_body_as_utf8
signature = HMAC_SHA256(client_secret, signed_payload)
```

Implementação isolada:

```python
from __future__ import annotations

import hashlib
import hmac
import time


def verify_tiktok_signature(
    *,
    signature_header: str,
    raw_body: bytes,
    client_secret: str,
    now: int | None = None,
    tolerance_seconds: int = 300,
) -> bool:
    if not client_secret:
        raise ValueError("Client Secret ausente")

    parts: dict[str, str] = {}
    for item in signature_header.split(","):
        key, separator, value = item.partition("=")
        if separator:
            parts[key.strip()] = value.strip()

    timestamp = parts.get("t")
    received = parts.get("s")
    if not timestamp or not received:
        return False

    try:
        timestamp_int = int(timestamp)
    except ValueError:
        return False

    current = int(time.time() if now is None else now)
    if abs(current - timestamp_int) > tolerance_seconds:
        return False

    try:
        body_text = raw_body.decode("utf-8")
    except UnicodeDecodeError:
        return False

    signed_payload = f"{timestamp}.{body_text}".encode("utf-8")
    expected = hmac.new(
        client_secret.encode("utf-8"),
        signed_payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(received, expected)
```

No repositório, essa lógica está em `TikTokProvider.verify_webhook()`. O endpoint deve obter `await request.body()` e encaminhar os bytes sem parse prévio:

```python
@router.post("/v1/social/webhooks/tiktok")
async def tiktok_webhook(
    request: Request,
    tiktok_signature: str | None = Header(default=None),
):
    raw_body = await request.body()
    if not tiktok_signature:
        return JSONResponse({"error": "signature_missing"}, status_code=401)

    provider = TikTokProvider()
    if not provider.verify_webhook(
        signature_header=tiktok_signature,
        raw_body=raw_body,
        tolerance_seconds=300,
    ):
        return JSONResponse({"error": "signature_invalid"}, status_code=401)

    payload = json.loads(raw_body)
    await persist_and_enqueue("tiktok", payload, raw_body)
    return {"received": True}
```

## 3. Replay, deduplicação e retries

HMAC autentica a origem e a integridade, mas por si só não impede que um atacante repita um payload válido. O receptor deve aplicar uma janela de timestamp ao TikTok e criar uma chave idempotente para ambos:

```python
idempotency_key = sha256(
    provider.encode() + b":" + provider_event_id.encode()
).hexdigest()
```

A persistência deve acontecer antes da resposta `200`. Se a chave já existir com estado `PROCESSED`, devolva `200` sem executar novamente. Se existir como `RETRY_WAIT`, deixe o worker continuar o retry existente. Falhas transitórias usam backoff; assinatura inválida, segredo ausente e capability não autorizada vão para rejeição/dead-letter, não para retry infinito.

```text
RECEIVED → VERIFIED → PERSISTED → QUEUED → PROCESSED
                              ├─ RETRY_WAIT
                              ├─ IGNORED
                              └─ DEAD_LETTER
```

## 4. Testes essenciais

Os testes devem usar um segredo de fixture, nunca um secret real:

```python
import hashlib
import hmac


def meta_header(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def tiktok_header(secret: str, body: bytes, timestamp: int) -> str:
    signed = f"{timestamp}.".encode() + body
    digest = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    return f"t={timestamp},s={digest}"
```

A matriz mínima é:

| Caso | Resultado esperado |
|---|---|
| Corpo e secret corretos | `True` |
| Um byte alterado no corpo | `False` |
| Secret diferente | `False` |
| Header ausente ou prefixo Meta incorreto | `False` |
| Hex inválido ou comprimento incorreto | `False` |
| TikTok timestamp fora da tolerância | `False` |
| TikTok header com whitespace normal | `True` |
| Corpo TikTok não UTF-8 | `False` |
| Evento já persistido | `200`, sem segunda execução |

## 5. Checklist de produção

O corpo bruto deve ser capturado antes do parsing. O App Secret Meta e o Client Secret TikTok devem vir do secret manager. A comparação deve usar `compare_digest`. A janela TikTok deve ter tolerância operacional pequena, com relógio UTC sincronizado. Eventos devem ser persistidos e deduplicados antes do processamento assíncrono. Logs devem registrar provider, status, event ID mascarado e motivo da rejeição, nunca o token, o secret, a assinatura completa ou o payload sensível. O endpoint deve impor limite de body e rate limiting no gateway.

O código atual já valida os formatos básicos e as rotas; a camada de persistência/fila serverless deve manter a mesma ordem `raw_body → verify → persist → enqueue → 200`.

## Referências oficiais

[1]: https://developers.facebook.com/documentation/instagram-platform/webhooks — Meta, Setup Webhooks Subscriptions.

[2]: https://developers.tiktok.com/doc/webhooks-events — TikTok, Webhook Events.

[3]: https://docs.aws.amazon.com/lambda/latest/dg/urls-webhook-tutorial.html — AWS, webhook HMAC example and secret handling.
