# Contrato da API

A API é servida pelo módulo `services.api.main`. Em desenvolvimento, a raiz padrão é `http://localhost:8000`.

## `GET /health`

Retorna o estado do gateway e a versão da API.

```json
{"status":"ok","service":"kairos-sonica-api","version":"0.1.0"}
```

## `GET /v1/persona`

Retorna a persona operacional versionada do Agente Káiros. O payload inclui identidade, missão, papéis, capacidades, pipeline, contrato de saída, guardrails e o prompt de sistema. Em produção, o endpoint deve ser protegido por autenticação e política de versionamento.

```json
{
  "id": "kairos.aai_apo",
  "name": "Káiros",
  "version": "1.0.0",
  "language": "pt-BR",
  "roles": ["Maestro Layer", "Rhythm and Groove Agent"],
  "pipeline": ["intake", "maestro_plan", "generation", "master_and_delivery"]
}
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

## `POST /v1/orchestrate`

Cria uma tarefa assíncrona para a central multimídia. O endpoint pode analisar um áudio existente, transcrever por sidecar ou Faster-Whisper e gerar um novo artefato pelo pipeline do Káiros. O caminho relativo de `audio_path` deve estar em `data/uploads` ou `data/output`; não são aceitos caminhos arbitrários.

```json
{
  "prompt": "Reimaginar a referência como Trap Soul noturno",
  "audio_path": "reference.wav",
  "transcribe": true,
  "transcription_backend": "sidecar",
  "transcription_model": "small",
  "transcription_language": "pt",
  "analyze_audio": true,
  "generate_audio": true,
  "genre": "Trap Soul",
  "bpm": 140,
  "key": "C#",
  "scale": "minor",
  "duration_seconds": 8,
  "output_format": "wav",
  "stems": false
}
```

O backend `sidecar` lê `reference.txt` ou `reference.json` ao lado do áudio e é o default sem download de modelo. O backend `faster-whisper` é opcional e deve ser instalado e configurado explicitamente pelo operador.

A resposta inicial segue o mesmo contrato de tarefa:

```json
{"task_id":"...","status":"PENDING"}
```

## `GET /v1/tasks/{task_id}`

Retorna `PENDING`, `RUNNING`, `SUCCEEDED` ou `FAILED`, além de `progress`, `artifact_url`, `error` e timestamps.

## `GET /v1/audio/{task_id}`

Entrega o arquivo final quando a tarefa está concluída. O caminho é resolvido dentro de `KAIROS_OUTPUT_DIR`; não são aceitos caminhos arbitrários enviados pelo cliente.

## `GET /v1/transcript/{task_id}` e `GET /v1/metadata/{task_id}`

Entregam, respectivamente, o sidecar JSON da transcrição e os metadados completos da orquestração. O snapshot da tarefa também inclui `result.analysis`, `result.transcription`, `result.plan` e URLs relativas dos artefatos quando disponíveis.

## `WS /ws/tasks/{task_id}`

Envia snapshots JSON de progresso até a conclusão. Um cliente deve tratar desconexão e também consultar o endpoint HTTP, pois o WebSocket é um canal de atualização e não uma fila durável.
