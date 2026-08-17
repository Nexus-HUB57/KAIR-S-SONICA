# Contrato da API

A API é servida pelo módulo `services.api.main`. Em desenvolvimento, a raiz padrão é `http://localhost:8000`.

## `GET /health`

Retorna o estado do gateway e a versão da API.

```json
{"status":"ok","service":"kairos-sonica-api","version":"0.1.0"}
```

## `POST /v1/plan`

Recebe um pedido musical e retorna o plano normalizado sem gerar áudio.

```json
{
  "prompt": "Trap Soul noturno, caixa atrás do tempo",
  "genre": "Trap Soul",
  "bpm": 140,
  "key": "C#",
  "scale": "minor",
  "lyrics": "Vida de artista, flow pesado",
  "duration_seconds": 8,
  "swing": 0.6,
  "humanize_ms": 8,
  "output_format": "wav",
  "stems": false
}
```

## `POST /v1/generate`

Cria uma tarefa assíncrona. A resposta contém `task_id` e o estado inicial.

```json
{"task_id":"...","status":"PENDING"}
```

## `GET /v1/tasks/{task_id}`

Retorna `PENDING`, `RUNNING`, `SUCCEEDED` ou `FAILED`, além de `progress`, `artifact_url`, `error` e timestamps.

## `GET /v1/audio/{task_id}`

Entrega o arquivo final quando a tarefa está concluída. O caminho é resolvido dentro de `KAIROS_OUTPUT_DIR`; não são aceitos caminhos arbitrários enviados pelo cliente.

## `WS /ws/tasks/{task_id}`

Envia snapshots JSON de progresso até a conclusão. Um cliente deve tratar desconexão e também consultar o endpoint HTTP, pois o WebSocket é um canal de atualização e não uma fila durável.
