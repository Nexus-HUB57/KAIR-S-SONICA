# Contrato da API

A API é servida pelo módulo `services.api.main`. Em desenvolvimento, a raiz padrão é `http://localhost:8000`.

## `GET /health`

Retorna o estado do gateway e a versão da API.

```json
{"status":"ok","service":"kairos-sonica-api","version":"0.1.0"}
```

## `GET /ready`

Retorna `200` quando o serviço está vivo e, se `KAIROS_ENABLE_SKYREELS=true`, quando o clone, o entry point Diffusion Forcing e o checkpoint configurado estão acessíveis. Caso contrário, retorna `503` com o mapa de verificações. O endpoint é adequado para readiness probe; `/health` permanece como liveness probe.

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

## `GET /v1/video/capabilities`

Retorna os backends e modos disponíveis no processo atual. O campo `native.runtime` indica apenas se `torch` e `diffusers` podem ser importados; a prontidão completa de checkpoint e device continua sendo responsabilidade de `GET /ready`.

```json
{
  "backends": {
    "cli": {"enabled": true, "engine": ["standard", "diffusion_forcing"]},
    "native": {
      "enabled": true,
      "engine": ["standard", "diffusion_forcing"],
      "runtime": true,
      "ready": false,
      "checkpoint": {"configured": true, "exists": false}
    }
  },
  "modes": ["t2v", "i2v", "extend", "start_end"],
  "default_backend": "native"
}
```

## `GET /v1/agents/capabilities`

Retorna o catálogo versionado de agentes, skills, algoritmos e operações conhecidas pelo agregador. O endpoint não faz chamadas de rede, não dispara geração e informa explicitamente quais integrações estão habilitadas. Os agentes externos permanecem desabilitados por padrão.

```json
{
  "schema_version": 1,
  "enabled": false,
  "agents": [
    {
      "name": "skyreels-space",
      "kind": "remote_gradio_agent",
      "enabled": false,
      "ready": false,
      "skills": ["remote-text-to-video", "sse-polling"]
    },
    {
      "name": "llamagen",
      "kind": "remote_rest_agent",
      "enabled": false,
      "ready": false,
      "skills": ["storyboard", "comic-panels", "panel-regeneration"]
    }
  ]
}
```

## `GET /v1/agents/{agent_name}/probe`

Executa explicitamente um probe contra o agente selecionado. Para `skyreels-space`, consulta `/gradio_api/info` e `/config`; para `llamagen`, consulta `GET /v1/comics/generations/nonexistent` com o Bearer configurado. O probe exige `KAIROS_AGENT_AGGREGATOR_ENABLED=true` e o agente específico habilitado. Retorna `503` quando a integração está desabilitada ou o nome é desconhecido e `502` quando o terceiro está indisponível ou rejeita a autenticação. Nenhum segredo é incluído no payload ou nos logs do cliente.

Exemplos de nomes aceitos: `skyreels-native`, `skyreels-space` e `llamagen`.

## `POST /v1/video/generate`

Cria uma tarefa assíncrona para T2V, I2V, Diffusion Forcing, extensão ou controle de frame inicial/final. O backend exige `KAIROS_ENABLE_SKYREELS=true`, clone e checkpoint configurados; referências de imagem/vídeo só podem estar em `data/uploads` ou `data/output`.

```json
{
  "prompt": "A continuous cinematic live-action shot in rain, moving camera, no text, no watermark.",
  "mode": "i2v",
  "engine": "diffusion_forcing",
  "backend": "native",
  "resolution": "540P",
  "image_path": "keyframe.png",
  "num_frames": 97,
  "fps": 24,
  "seed": 42,
  "offload": true
}
```

A resposta é `202 Accepted` com `task_id`. Em modo `inline`, a API inicia o worker local; em modo `queue`, apenas grava o payload no `TaskStore` e o processo `scripts/run_worker.py` reivindica e executa o job. O MP4 é validado com `ffprobe` antes de ser publicado. Com `backend=native`, o worker seleciona as pipelines Diffusers nativas e usa `KAIROS_SKYREELS_NATIVE_MODEL_ID`; com `backend=cli`, usa os entry points do clone e `KAIROS_SKYREELS_MODEL_ID`.

## `GET /v1/tasks/{task_id}`

Retorna `PENDING`, `RUNNING`, `SUCCEEDED` ou `FAILED`, além de `progress`, `artifact_url`, `error` e timestamps.

## `GET /v1/video/{task_id}`

Entrega o MP4 publicado para uma tarefa de vídeo concluída. O serviço não expõe o staging e não sobrescreve uma saída existente.

## `GET /v1/audio/{task_id}`

Entrega o arquivo final quando a tarefa está concluída. O caminho é resolvido dentro de `KAIROS_OUTPUT_DIR`; não são aceitos caminhos arbitrários enviados pelo cliente.

## `GET /v1/transcript/{task_id}` e `GET /v1/metadata/{task_id}`

Entregam, respectivamente, o sidecar JSON da transcrição e os metadados completos da orquestração. O snapshot da tarefa também inclui `result.analysis`, `result.transcription`, `result.plan` e URLs relativas dos artefatos quando disponíveis.

## `WS /ws/tasks/{task_id}`

Envia snapshots JSON de progresso até a conclusão. Um cliente deve tratar desconexão e também consultar o endpoint HTTP, pois o WebSocket é um canal de atualização e não substitui o `TaskStore` persistente.
