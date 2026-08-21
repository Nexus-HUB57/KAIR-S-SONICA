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

## `GET /v1/complementary/capabilities`

Retorna as capacidades da camada complementar de planejamento e handoff. Essa camada é um núcleo aditivo: não substitui o gateway, o `TaskStore`, o worker, o pipeline de áudio ou os backends SkyReels. O endpoint não consulta a rede e não habilita Pexels, TTS, MusicGen ou agentes remotos.

```json
{
  "name": "complementary-audiovisual-core",
  "version": 1,
  "enabled": true,
  "role": "planning-and-handoff",
  "replaces_existing_core": false,
  "capabilities": ["prompt-to-scene-plan", "stock-media-slot-planning", "skyreels-request-handoff"]
}
```

## `POST /v1/complementary/plan`

Cria um plano síncrono de pré-produção a partir de um prompt. A resposta divide a duração em cenas, cria slots opcionais para mídia stock e áudio, e gera templates compatíveis com `POST /v1/video/generate`. A rota não cria `task_id`, não baixa mídia, não chama Pexels, não gera áudio, não chama LlamaGen/SkyReels e não grava MP4.

```json
{
  "prompt": "chuva neon em videoclipe vertical",
  "duration_seconds": 10,
  "aspect_ratio": "9:16",
  "resolution": "720P",
  "fps": 24,
  "scene_seconds": 5,
  "audio_mode": "external-slot",
  "media_mode": "generated-or-stock-slot",
  "seed": 42
}
```

O consumidor pode revisar o plano e, em uma etapa posterior, enviar cada `video_request_template` para a fila existente ou encaminhar a parte sonora para `POST /v1/orchestrate`. A promoção, a validação `ffprobe` e a entrega HTTP continuam pertencendo ao núcleo existente.

## `POST /v1/complementary/media/search`

Busca ativos de mídia por uma ação explícita. O campo `kind` aceita `image` ou `video`; o campo `download` permanece `false` por padrão e, quando `true`, grava os resultados no `MediaCache` configurado com promoção atômica. A cadeia usa `KAIROS_MEDIA_PROVIDER_ORDER`, por padrão Pexels e Unsplash. Se as chaves opcionais não estiverem presentes, os provedores são ignorados e a resposta contém `assets: []`; o endpoint não é chamado pelo planner automaticamente.

```json
{
  "query": "rain-soaked rap video",
  "kind": "image",
  "per_page": 5,
  "orientation": "portrait",
  "download": false
}
```

A resposta inclui `provider_order`, `assets` normalizados e `downloaded`. URLs, chaves e conteúdo não são colocados em logs estruturados; downloads são limitados por `KAIROS_MEDIA_CACHE_MAX_BYTES`.

## `GET /v1/agentic/capabilities`

Retorna os 12 papéis agenticos, skills, estágios e contratos de handoff. O catálogo é local, não chama LLM, não consulta provedores e não cria tarefas.

```json
{
  "schema_version": 1,
  "name": "kairos-agentic-studio",
  "enabled": true,
  "execution_mode": "deterministic-contract-first",
  "external_tools_default": false,
  "roles": ["ceo", "cco", "scriptwriter", "dop", "sound_designer", "editor", "vfx", "social", "producer", "rag", "accessibility", "qa"]
}
```

## `POST /v1/agentic/run`

Executa o planejamento agentico completo em modo síncrono de contrato. O resultado contém estratégia, direção criativa, roteiro/cenas, storyboard, plano de áudio, VFX, distribuição, acessibilidade, QA, memória e handoffs validáveis como `VideoRequest`/`MultimediaRequest`. Por padrão, `submit_handoffs=false` e nenhuma tarefa é criada.

Para submeter handoffs ao `TaskStore` e ao worker existentes, envie `submit_handoffs=true` e `approve_handoffs=true` deliberadamente. Cada cena vira uma tarefa `video`, o handoff de áudio vira uma tarefa `multimedia`, e o comportamento `inline`/`queue` segue `KAIROS_WORKER_MODE`. A rota nunca substitui `POST /v1/video/generate`, `POST /v1/orchestrate`, a validação `ffprobe` ou a entrega HTTP.

```json
{
  "prompt": "clipe de rap cinematográfico em chuva neon",
  "project_id": "campaign-001",
  "duration_seconds": 15,
  "scene_seconds": 5,
  "aspect_ratio": "9:16",
  "resolution": "720P",
  "fps": 24,
  "seed": 42,
  "include_media_references": false,
  "submit_handoffs": false,
  "approve_handoffs": false
}
```

`include_media_references=true` só consulta a cadeia Pexels/Unsplash se `KAIROS_AGENTIC_EXTERNAL_TOOLS_ENABLED=true`; downloads continuam fora do fluxo agentico e exigem a rota explícita de mídia.

### Contrato de submissão e processamento no `TaskStore`

O pedido de `/v1/agentic/run` é validado por `AgenticRunRequest`. `prompt` e `project_id` identificam o briefing; `duration_seconds`, `scene_seconds`, `aspect_ratio`, `resolution` e `fps` controlam o plano; `seed` mantém reprodutibilidade; `include_media_references` controla apenas a pesquisa opcional; e `max_iterations` limita a preparação determinística. `submit_handoffs` é o comando de escrita na fila e `approve_handoffs` é o gate de autorização. Se o primeiro for `true` e o segundo `false`, a API retorna `409` e não escreve no banco.

Com ambos em `true`, o orquestrador termina primeiro a validação do pacote. Para cada handoff `video_request`, ele reconstrói o payload com `VideoRequest.model_validate`, gera um `task_id` novo e chama `TaskStore.create(task_id, job_kind="video", payload=...)`. Para o handoff `multimedia_request`, executa a mesma operação com `MultimediaRequest` e `job_kind="multimedia"`. Cada chamada grava uma linha em `tasks` com status `PENDING` e uma linha em `task_jobs` com `claimed_at=NULL`; a resposta inclui os IDs em `submissions`.

No modo `KAIROS_WORKER_MODE=queue`, o processo HTTP encerra após persistir os jobs e o worker `scripts/run_worker.py` os reivindica atomicamente com `claim_recoverable_jobs`. No modo `inline`, a API inicia o runner correspondente em thread daemon depois da persistência. O runner atualiza `PENDING → RUNNING → SUCCEEDED/FAILED`; em estado terminal o `TaskStore` remove a linha de `task_jobs`, preservando o snapshot em `tasks`. Reinícios devolvem jobs não terminais à fila. O handoff não publica diretamente um MP4: vídeo continua sujeito ao staging, `ffprobe`, promoção atômica e `GET /v1/video/{task_id}`; áudio continua sujeito ao pipeline multimídia e `GET /v1/audio/{task_id}`.

Resposta de planejamento sem submissão:

```json
{
  "status": "READY_FOR_APPROVAL",
  "run_id": "...",
  "handoffs": [
    {"kind": "video_request", "requires_approval": true},
    {"kind": "video_request", "requires_approval": true},
    {"kind": "multimedia_request", "requires_approval": true}
  ],
  "submissions": []
}
```

Resposta após aprovação e submissão:

```json
{
  "status": "SUBMITTED",
  "run_id": "...",
  "submissions": [
    {"task_id": "...", "kind": "video", "agent": "vfx"},
    {"task_id": "...", "kind": "multimedia", "agent": "audio_pipeline"}
  ]
}
```

## `GET /v1/artistic-island/capabilities`

Retorna o estado do núcleo complementar da Ilha Artística, a origem do Atlas, o número de instrumentos, os 12 algoritmos-base registrados e o modo de execução. `enabled=true` significa que o planejador está disponível; não significa que plugins VST/AU/LV2, downloads, RAG externo ou DSP profissional estejam habilitados.

## `GET /v1/artistic-island/instruments`

Retorna os perfis normalizados do Atlas para a interface do estúdio. A resposta contém `instrument`, `family`, `roles`, `tags`, presets iniciais de EQ, compressão, espaço e dados vocais quando aplicáveis. Se `KAIROS_ARTISTIC_ISLAND_ENABLED=false`, a API retorna `503`.

## `POST /v1/artistic-island/mix-plan`

Gera uma cadeia de processamento revisável para um instrumento e contexto musical. O request aceita `instrument`, `context`, `prompt`, `max_steps` entre 5 e 15, `include_optional` e `reference_id` opcional. A resposta retorna `chain`, `master_bus`, `provenance` e `warnings`. Cada etapa contém `order`, `algorithm`, `parameters`, `rationale` e `execution_mode`.

Este endpoint é síncrono e sem efeitos externos: não lê ou grava áudio, não carrega plugins, não consulta provedores e não cria uma entrada no `TaskStore`. Instrumento ausente no Atlas resulta em `422`; ilha desabilitada resulta em `503`.

## `GET /v1/studio-master/capabilities`

Expõe a camada complementar de orquestração musical. O retorno declara o analisador determinístico disponível, os adapters opcionais, o número de padrões do cânone e o número de perfis de repertório. A habilitação não carrega PyTorch, librosa, aubio, pedalboard, FluidSynth, samples ou modelos.

## `GET /v1/studio-master/canon` e `GET /v1/studio-master/repertoire`

Retornam, respectivamente, o índice editorial de padrões culturais e os perfis instrumentais/cadeias de mixagem. Os arquivos `config/canon_index.yaml` e `config/instrumentation_repertoire.yaml` são metadados versionados; não contêm áudio, MIDI, embeddings, loops ou presets proprietários. Cada projeto deve substituir `asset_ref` apenas por material próprio, licenciado ou de domínio público.

## `POST /v1/studio-master/groove/analyze`

Recebe uma forma de onda mono em `samples`, `sample_rate`, `bpm` e `canon_id` opcional. O request é limitado por `KAIROS_STUDIO_MASTER_MAX_INPUT_SAMPLES`, cujo default é 250.000 amostras. O retorno `GrooveDna` contém onsets, densidade, offset médio, desvio de microtiming, swing ratio, confiança, probabilidades culturais heurísticas e o padrão canônico mais próximo.

O método atual é `deterministic-onset-energy/v1`: ele é uma referência CPU sem treinamento e não deve ser descrito como classificação neural. Os adapters de GrooveExtractor neural, librosa e aubio devem ser adicionados separadamente, com pesos fora do Git, licença, checksum e gate explícito.

## `POST /v1/studio-master/responsive-plan`

Funde `style`, `canon_id`, `repertoire_id`, BPM, swing, humanização, `grid_follow`, foco vocal e um `flow` opcional em um `ResponsiveMixPlan`. O plano declara sidechain multibanda, punchline, cadeia instrumental, destino de handoff e um patch compatível com `MultimediaRequest`. Ele é `READY_FOR_APPROVAL`: não cria tarefa, não renderiza áudio e não grava arquivos.

Exemplo mínimo:

```json
{
  "style": "brazilian_funk_heavy",
  "canon_id": "br_funk_mandelao",
  "repertoire_id": "brazilian_funk_heavy_kit",
  "bpm": 140,
  "swing_ratio": 0.55,
  "grid_follow": true
}
```

## `GET /v1/studio-master/performance/{session_id}` e `WS /ws/studio-master/{session_id}/performance`

O snapshot HTTP e o canal WebSocket controlam o estado efêmero de uma sessão. Os comandos aceitos são `SET_SWING`, `SET_GRID_FOLLOW`, `SET_BPM`, `BOOST_PUNCHLINE`, `RESET` e `PUSH_TO_LIBRARY`. O valor de swing pode ser enviado como `0.65` ou `65%`; os limites são 0,50–0,67. `PUSH_TO_LIBRARY` cria apenas uma proposta de metadados `PENDING_APPROVAL`; não persiste áudio, MIDI ou sample e exige aprovação editorial/licença antes de qualquer futura publicação.

## Handoff agentico do StudioMaster

O `AgenticToolbox` injeta um `studio_master_plan` no handoff `multimedia_request` do Sound Designer. O patch contém BPM, swing, humanização, gênero e `stems=true`, mas a submissão continua sujeita a `approve_handoffs=true` e usa o mesmo `TaskStore`/worker. Os 12 papéis existentes não foram substituídos nem duplicados.

## Validação no Compose GPU público

No host NVIDIA/CUDA público, o fluxo completo de readiness e descoberta pode ser executado com:

```bash
./scripts/test_agents_gpu_compose.sh
```

O harness valida `nvidia-smi`, Docker Compose v2, o manifesto `docker-compose.gpu.yml`, `/ready`, `/health`, `/v1/video/capabilities`, `/v1/agents/capabilities` e `/v1/agentic/capabilities`. Por padrão, exige que o backend native esteja pronto, não faz chamadas a terceiros e mantém `KAIROS_RUN_EXTERNAL_PROBES=false`. Depois de revisar custo, procedência, retenção e credenciais, o operador pode habilitar os gates e executar os probes remotos:

```bash
KAIROS_AGENT_AGGREGATOR_ENABLED=true \
KAIROS_SKYREELS_SPACE_ENABLED=true \
KAIROS_RUN_EXTERNAL_PROBES=true \
./scripts/test_agents_gpu_compose.sh
```

O probe LlamaGen só é executado quando `KAIROS_LLAMAGEN_ENABLED=true` e `LLAMAGEN_API_KEY` estão presentes; `KAIROS_REQUIRE_LLAMAGEN_PROBE=true` transforma sua ausência em falha explícita. A chave é interpolada pelo ambiente do host, nunca colocada no Compose, na imagem ou no Git.

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

## StudioMaster 2.0: arranjo, expressão e operação segura

A segunda camada do StudioMaster amplia o command deck sem criar uma API paralela. Todas as rotas abaixo exigem `KAIROS_STUDIO_MASTER_ENABLED=true`, são síncronas e produzem propostas ou previews determinísticos; elas não criam `task_id`, não gravam áudio/MIDI, não publicam conteúdo e não promovem checkpoints.

### `POST /v1/studio-master/arrangement`

Recebe `style`, `mood`, `bpm`, `total_bars` e `key` e retorna um `ArrangementPlan` com seções, energia, instrumentos abstratos e automações de filtro, reverb e drive. O orçamento de compassos é validado e a resposta permanece `READY_FOR_APPROVAL`.

### `POST /v1/studio-master/expression`

Recebe notas abstratas, BPM, `swing_ratio`, `humanize_ms`, um `energy_map` e um `seed`. Retorna as mesmas notas com velocity e microtiming determinísticos. O motor não muta a entrada, não usa randomismo global e mantém a variação dentro dos limites do contrato.

### `POST /v1/studio-master/hum-to-midi`

Recebe frames de pitch já extraídos (`time_seconds`, `frequency_hz`, `confidence`) e produz um sketch de notas MIDI abstratas. CREPE, exportação binária MIDI e renderização por FluidSynth são adapters opcionais; o caminho base não recebe arquivo temporário, não baixa modelo e não retorna áudio.

### `POST /v1/studio-master/signature-plan`

Gera o plano paramétrico do Modo Káiros para `audio_input`, `mix_bus` ou `vocal_bus`. A resposta descreve EQ, compressão, excitação harmônica, largura estéreo, reverb e limiter, com `source_imitation=false`, `automatic_file_write=false` e `approval_required=true`. O plano representa atributos de produção configurados pelo operador, não uma reprodução de artista, gravação ou curva externa.

### `POST /v1/studio-master/ducking/preview`

Executa um preview RMS envelope em NumPy sobre `mix_bus` e `reference_track`. O resultado retorna um array limitado e o método `numpy-rms-envelope/v1`. Ducking espectral multibanda profissional requer adapter Pedalboard/SciPy habilitado separadamente.

### `POST /v1/studio-master/perceptual/score`

Calcula `peak_dbfs`, `rms_dbfs`, faixa dinâmica e um score técnico de saúde de sinal. Esse score não é MOS subjetivo. MOSNet/TorchAudio permanecem opcionais e não são carregados automaticamente.

### `GET /v1/studio-master/adapters`

Lista adapters detectados no ambiente — Groove neural, pitch tracking, Pedalboard, Matchering, memória vetorial, MOS, FluidSynth e renderer social — sem importá-los ou habilitá-los. Todos retornam `enabled=false` até uma configuração explícita.

### `POST /v1/studio-master/memory/feedback`

Registra feedback textual somente quando `KAIROS_STUDIO_MASTER_MEMORY_ENABLED=true`. O backend base é JSONL local append-only e metadata-only; ele não armazena áudio, embeddings proprietários ou referências externas. Chroma/embeddings são caminhos opcionais.

### `GET /v1/studio-master/analytics`

Lê, quando existente, `KAIROS_STUDIO_MASTER_ANALYTICS_PATH` e normaliza total de produções, MOS médio disponível, distribuição de gêneros e últimos registros. Na ausência de histórico, retorna uma estrutura vazia. A rota não cria ou modifica o histórico.

### `GET /v1/studio-master/retraining`

Consulta `KAIROS_STUDIO_MASTER_RETRAIN_MANIFEST_PATH` por meio do `AutoRetrainGuard`. O status pode ser `DISABLED`, `WAITING_MANIFEST`, `READY_FOR_APPROVAL` ou `BLOCKED`. O manifesto precisa declarar samples aprovados, aprovação do operador, proveniência/licença e split de validação. Mesmo elegível, nenhum treino ou promoção ocorre pela API.

O comando `scripts/auto_retrain.py` imprime o mesmo plano em JSON e é adequado para inspeção futura por cron no host de treinamento. O script deliberadamente não importa Torch, não baixa dataset, não sobrescreve `models/` e não executa troca de checkpoint.

### `POST /v1/studio-master/viral-clip-plan`

Gera o plano de um clip social de 5–60 segundos, com canvas `9:16`, `1:1` ou `16:9`, waveform RMS, título, watermark e adapter `moviepy-or-browser-canvas`. O asset de áudio deve ser gerado ou carregado pelo operador; o plano não baixa fontes, não escreve MP4 e não publica em TikTok, Reels ou Shorts.

O command deck browser consulta analytics, retraining e adapters ao carregar, e permite propor arranjo, Modo Káiros e clip. Cada resultado é visualizado com estado de aprovação; o pipeline de áudio, o worker, o `TaskStore`, o SkyReels e o fluxo de `ffprobe` permanecem inalterados.
