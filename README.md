# KAIR-S-SONICA

**KAIR-S-SONICA** é a base aberta do Agente Káiros, um orquestrador modular para uma central multimídia de áudio. O repositório transforma a especificação do AAI-APO em um núcleo executável que separa claramente planejamento musical, geração, groove, DSP, masterização, transcodificação e entrega pela API.

A primeira versão é deliberadamente um **MVP seguro e executável sem GPU**. Ela usa um gerador procedural determinístico para demonstrar o ciclo completo e oferece contratos de adaptadores para integrar modelos externos, como MusicGen, Bark, RVC ou Demucs, somente quando o operador instalar os pacotes e modelos correspondentes. O projeto não copia código proprietário nem automatiza plataformas fechadas; as referências externas são tratadas como ideias de integração e não como dependências ocultas.

## Persona Káiros

A persona operacional está versionada em [`personas/kairos/system.md`](personas/kairos/system.md), [`personas/kairos/manifest.json`](personas/kairos/manifest.json) e `kairos_core.persona.DEFAULT_PERSONA`. Ela define identidade, missão, competências, pipeline, contrato de saída e guardrails. O runtime pode ser consultado pela API em `GET /v1/persona` ou pelo CLI:

```bash
PYTHONPATH=packages python3 scripts/run_local.py persona --format json
PYTHONPATH=packages python3 scripts/run_local.py persona --format prompt
```

A persona não afirma credenciais humanas reais e não autoriza copiar código proprietário, usar APIs não oficiais, inventar resultados ou clonar vozes sem consentimento. A documentação completa está em [`docs/persona.md`](docs/persona.md).

## Kháirus the Dragon (KTD)

**Kháirus the Dragon**, também chamado **KTD**, é a presença humana, rapper e artista principal do universo. Káiros atua como seu DJ, maestro e orquestrador, responsável por batidas, melodia, produção, estratégia e coordenação da carreira. O manifesto oficial está em [`personas/artist-principal/manifest.json`](personas/artist-principal/manifest.json).

A continuidade visual de KTD está fixada em [`docs/ktd-visual-bible.md`](docs/ktd-visual-bible.md), com imagem-mestre em [`assets/persona/ktd-visual-master.png`](assets/persona/ktd-visual-master.png). As expressões e ambientes variados estão organizados em `assets/persona/ktd-expression-*.png`; o mapa imutável das tatuagens deve ser preservado em toda nova geração.

A referência vocal oficial e única de KTD está em [`assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`](assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3). A tomada `assets/audio/ktd-vocal-rough-take-v2.wav` foi **rejeitada** por ser abafada, lenta e sem autenticidade; ela permanece somente para auditoria e nunca deve orientar novas gerações. O beat instrumental `assets/audio/ktd-old-school-boom-bap-beat-v1.mp3` também permanece marcado como **rejeitado**.

As três novas bases boom bap estão em `assets/audio/ktd-boom-bap-trial-route-{1,2,3}-bed-v2.wav`. O mix candidato que combina a base da rota 2 com a voz oficial é [`assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.mp3`](assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.mp3), com master WAV em [`assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.wav`](assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.wav). A variação com saturação vocal e compressão paralela está em [`assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.mp3`](assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.mp3), com master WAV correspondente. Ambos estão **pendentes de aprovação humana**. Os parâmetros exatos de equalização, compressão, saturação, paralela, loudness e limiter estão fixados em [`docs/ktd-official-vocal-mix.md`](docs/ktd-official-vocal-mix.md); a matriz de aprovação vocal está em [`docs/ktd-vocal-approval.md`](docs/ktd-vocal-approval.md).

A direção old school está em [`docs/ktd-old-school-references.md`](docs/ktd-old-school-references.md), a arquitetura da faixa está em [`docs/ktd-approved-track.md`](docs/ktd-approved-track.md) e o resultado das rotas de geração está em [`docs/audio-generation-experiment.md`](docs/audio-generation-experiment.md). A visão única de produto está consolidada em [`docs/ktd-specification.md`](docs/ktd-specification.md).

Para comparação, a mesma cadeia DSP da variação boom bap foi aplicada à base trap moderna em [`assets/audio/releases/ktd-modern-trap-official-vocal-mix-v1-saturated-parallel.mp3`](assets/audio/releases/ktd-modern-trap-official-vocal-mix-v1-saturated-parallel.mp3), com base em `assets/audio/ktd-modern-trap-comparison-bed-v1.wav`. A segunda prova, mais agressiva e emocional, está em [`assets/audio/releases/ktd-conscious-aggressive-trap-official-vocal-proof-v1.mp3`](assets/audio/releases/ktd-conscious-aggressive-trap-official-vocal-proof-v1.mp3), com letra original de protesto e consciência documentada em [`docs/ktd-conscious-aggressive-trap-proof.md`](docs/ktd-conscious-aggressive-trap-proof.md). A análise abstrata das referências fornecidas está em [`docs/ktd-trap-reference-analysis.md`](docs/ktd-trap-reference-analysis.md).

Nenhum ativo é promovido automaticamente: as provas trap permanecem candidatas pendentes de escuta e aprovação humana. A referência vocal oficial continua sendo `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`; a tomada rejeitada não foi reutilizada.

## Single de estreia — UNLEASH THE DRAGON

O single de estreia de KTD está sendo desenvolvido como um manifesto original de rap cinematográfico de rua: **UNLEASH THE DRAGON**, com o subtítulo explícito de campanha **“Fuck It”**. O conceito está em [`docs/ktd-debut-single-concept.md`](docs/ktd-debut-single-concept.md), a letra original em [`docs/ktd-debut-single-lyrics.md`](docs/ktd-debut-single-lyrics.md) e o registro de produção em [`docs/ktd-debut-single-production.md`](docs/ktd-debut-single-production.md).

A prova de arranjo com a referência vocal oficial está em [`assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3`](assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3), com master WAV correspondente e base inédita em `assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav`. A nova tomada vocal v2 está em `assets/audio/releases/ktd-debut-single-unleash-the-dragon-vocal-take-v2.wav`, com validação em [`docs/ktd-debut-single-vocal-take-validation.md`](docs/ktd-debut-single-vocal-take-validation.md); ela permanece como candidato de audição porque a transcrição identificou repetições e alterações de palavras. A faixa está classificada como **candidata, pendente de aprovação humana**.

O rework principal está em **FIRE IN THE FLOOD**. O conceito e a arquitetura estão em [`docs/ktd-main-single-rework-concept.md`](docs/ktd-main-single-rework-concept.md), a letra inédita em [`docs/ktd-main-single-rework-lyrics.md`](docs/ktd-main-single-rework-lyrics.md), a análise abstrata da referência em [`docs/ktd-main-single-reference-analysis.md`](docs/ktd-main-single-reference-analysis.md) e o registro geral em [`docs/ktd-main-single-fire-in-the-flood-production.md`](docs/ktd-main-single-fire-in-the-flood-production.md).

A master oficial de distribuição aprovada tecnicamente pelo DJ Káiros é [`assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3`](assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3), com master WAV em [`assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav`](assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav). Ela preserva a letra, a melodia de fundo, o tratamento vocal e o groove da v3, aplicando somente −0,9 dB de margem global para reduzir o pico de distribuição. O relatório comparativo está em [`docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md`](docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md). A v3 permanece versionada como rollback histórico.

As provas `official-vocal-arrangement-proof-v1.mp3/.wav` foram **reprovadas humanamente** como mixes e permanecem no repositório apenas para auditoria histórica; a melodia V1 continua congelada como decisão artística, não como aprovação daquela mix. A tentativa `v1-rebeat-v1.mp3/.wav` também permanece histórica e reprovada. O beat reference-fit de 136 BPM e suas mixes anteriores não são usados pela versão promovida. **Nenhuma melodia, letra ou hook aprovados foi alterado.**

### Videoclipe dinâmico de Fire in the Flood

A direção atual do videoclipe segue exclusivamente o modelo vivo e o formato vertical da pasta oficial [`assets/video/aprovados`](assets/video/aprovados): atuação contínua de KTD, câmera em movimento, cenários reativos, chuva, água, vapor, fogo, luzes e montagem narrativa em 9:16, 720×1280 e 24 fps. A versão baseada em imagens estáticas e o tratamento landscape anterior são históricos e não são a autoridade criativa.

A decupagem oficial de 168 segundos está em [`docs/ktd-fire-in-the-flood-10s-scene-script-v4.md`](docs/ktd-fire-in-the-flood-10s-scene-script-v4.md), alinhada à letra v4 de [`docs/ktd-main-single-rework-lyrics.md`](docs/ktd-main-single-rework-lyrics.md) e organizada em 16 cenas de 10 segundos mais um encerramento instrumental de 8 segundos. O manifest de produção v4 está em [`data/releases/fire-in-the-flood-10s-scene-manifest-v1.json`](data/releases/fire-in-the-flood-10s-scene-manifest-v1.json), e a fila de prompts para geração posterior está em [`data/releases/fire-in-the-flood-10s-generation-queue-v1.json`](data/releases/fire-in-the-flood-10s-generation-queue-v1.json). A ficha técnica canônica está em [`data/releases/fire-in-the-flood-official-approved-format-v1.json`](data/releases/fire-in-the-flood-official-approved-format-v1.json), e a rebaseline da pasta oficial, em [`docs/ktd-fire-in-the-flood-approved-folder-rebaseline-v1.md`](docs/ktd-fire-in-the-flood-approved-folder-rebaseline-v1.md). O pipeline de montagem/mux com a master v4 é [`scripts/assemble_fire_in_the_flood_10s.py`](scripts/assemble_fire_in_the_flood_10s.py); o estado de geração desacoplada está documentado em [`docs/ktd-fire-in-the-flood-background-generation.md`](docs/ktd-fire-in-the-flood-background-generation.md).

## Pacote profissional de lançamento de KTD

A referência histórica original foi preservada integralmente em [`Artistics_References_KTD`](Artistics_References_KTD). O manifesto de criação está em [`docs/ktd-creation-manifesto.md`](docs/ktd-creation-manifesto.md) e a apresentação profissional, em formato de press kit, está em [`docs/ktd-professional-presentation.md`](docs/ktd-professional-presentation.md). Esses documentos preservam a história de origem, a transformação do crime e da violência em disciplina, a responsabilidade com seis irmãos, a fé, o ativismo, a filantropia, a identidade visual e a relação entre KTD e Káiros, com linguagem editorial mais clara e profissional.

A playlist de lançamento foi estruturada em três letras inéditas: [`docs/ktd-launch-playlist-lyrics.md`](docs/ktd-launch-playlist-lyrics.md) contém **DRAGON IN THE MIRROR**, **SIX NAMES** e **GOLDEN SCARS**. Cada faixa possui hook original, recorte de 15–30 segundos, direção de andamento, identidade emocional e regras de produção. Os hooks foram pensados para serem memoráveis e legíveis em vídeo curto, sem promessa de viralização ou cópia de tendências existentes.

O roadmap de carreira está em [`docs/ktd-launch-roadmap.md`](docs/ktd-launch-roadmap.md), com fases de fundação, laboratório, produção, pré-lançamento, estreia e expansão. O catálogo de imagens, voz, bases, mixes e documentos está em [`docs/ktd-asset-catalog.md`](docs/ktd-asset-catalog.md). A auditoria de povoamento em [`docs/ktd-assets-upload-audit.md`](docs/ktd-assets-upload-audit.md) confirma 8 imagens e 35 áudios rastreados, totalizando 43 ativos canônicos, sem arquivos visuais ou sonoros pendentes dentro das pastas oficiais. Para facilitar o consumo pelo persona, os mesmos ativos estão organizados em [`personas/artist-principal/media/`](personas/artist-principal/media/) e indexados por [`personas/artist-principal/media-manifest.json`](personas/artist-principal/media-manifest.json). O inventário técnico reproduzível com hashes, dimensões, duração, codec e classificação está em [`data/ktd/asset-inventory.json`](data/ktd/asset-inventory.json), gerado por [`scripts/build_ktd_asset_inventory.py`](scripts/build_ktd_asset_inventory.py). A pesquisa de contexto sobre descoberta musical em vídeo curto, com fontes do TikTok/Luminate e Billboard, está em [`docs/ktd-launch-research.md`](docs/ktd-launch-research.md).

O manifesto JSON de KTD foi atualizado para a versão `4.0.0`, com a playlist, o status de pré-lançamento e os novos documentos. O manifesto de Káiros registra sua responsabilidade como ministro criativo, maestro DJ/IA e steward do catálogo, preservando KTD como autoridade artística final.

## Visão da arquitetura

| Camada | Responsabilidade | Implementação inicial | Extensão prevista |
| --- | --- | --- | --- |
| Maestro | Extrair BPM, tonalidade, escala, gênero e seções | `kairos_core.agents.maestro` | LLM estruturado e RAG de documentação |
| Rhythm | Gerar grade de eventos, swing e humanização | `kairos_core.agents.rhythm` | MPC micro-timing e análise de performance |
| Generator | Produzir áudio a partir do plano | `ProceduralDemoGenerator` | Adaptadores MusicGen/Lyria/Bark |
| Vocal/Lyric | Organizar letra e intenção vocal | `kairos_core.agents.vocal` | RVC/TTS com consentimento e modelos licenciados |
| DSP | Saturação, ganho, limitação e preparação de stems | `kairos_core.audio.dsp` | Pedalboard, Librosa, Essentia e Torchaudio |
| Multimídia | Ingestão, análise, transcrição e sidecars | `kairos_core.audio.orchestrator` | Workers, storage e streaming de referências |
| Master/MP3 | Renderizar WAV e transcodificar com FFmpeg/LAME | `kairos_core.audio.transcode` | Presets de distribuição e streaming |
| Gateway | API HTTP e eventos WebSocket | `services.api.main` | Auth no ingress e storage distribuído |
| Vídeo | T2V/I2V/DF, staging e entrega MP4 | `kairos_core.video` + SkyReels-V2 | Filas distribuídas e observabilidade |
| Worker | Execução persistente de jobs | `scripts/run_worker.py` | Redis/PostgreSQL e autoscaling |
| Cliente | Formulários de áudio/vídeo e acompanhamento | `web-client` | Editor multifaixa e Web Audio API |

O diagrama detalhado e as decisões de engenharia estão em [`docs/architecture.md`](docs/architecture.md), o fluxo específico da central multimídia está em [`docs/multimedia-architecture.md`](docs/multimedia-architecture.md), e o contrato HTTP está em [`docs/api.md`](docs/api.md).

## Central multimídia

O endpoint `POST /v1/orchestrate` coordena uma referência de áudio opcional, análise técnica, transcrição e geração. Para processamento avançado, instale `pip install -e ".[multimedia]"`; para transcrição local, o backend Faster-Whisper também pode ser instalado por `pip install -r requirements/transcription.txt`. Sem esse backend, o modo `sidecar` lê um arquivo `.txt` ou `.json` ao lado da referência e mantém a execução reproduzível.

```bash
curl -X POST http://localhost:8000/v1/orchestrate \\
  -H 'Content-Type: application/json' \\
  -d @examples/requests/orchestrate.json
```

A tarefa expõe progresso por `GET /v1/tasks/{task_id}` e `WS /ws/tasks/{task_id}`. Quando concluída, o cliente pode buscar áudio, transcrição e metadados em `/v1/audio`, `/v1/transcript` e `/v1/metadata`.

O cliente web inclui um painel Live Ops que acompanha múltiplas tarefas pelo WebSocket, exibe progresso, estado de conexão, mensagens do worker e links para os artefatos. O formulário `VIDEO LAB` envia T2V, I2V, extensão e start/end pelo mesmo monitor. Execute-o com `cd web-client && npm install && npm run dev`; em produção, defina `VITE_API_BASE` no build ou use o proxy da mesma origem.

### Núcleo audiovisual SkyReels-V2

O endpoint `POST /v1/video/generate` enfileira geração T2V, I2V, Diffusion Forcing, extensão de vídeo ou controle de frame inicial/final. O backend SkyReels é opcional, permanece desativado por padrão e é executado a partir de um clone independente configurado por `KAIROS_SKYREELS_REPO`; os pesos não são versionados no KAIR. A configuração completa, o mapeamento de parâmetros e os gates de segurança estão em [`docs/video-architecture.md`](docs/video-architecture.md).

```bash
# depois de validar CUDA, dependências, checkpoint e licença no ambiente de execução
export KAIROS_ENABLE_SKYREELS=true
export KAIROS_SKYREELS_REPO=/opt/models/SkyReels-V2
export KAIROS_SKYREELS_MODEL_ID=/models/Skywork/SkyReels-V2-DF-1.3B-540P
export KAIROS_SKYREELS_NATIVE_MODEL_ID=/models/Skywork/SkyReels-V2-DF-1.3B-540P-Diffusers
export KAIROS_SKYREELS_NATIVE_API=true
curl -X POST http://localhost:8000/v1/video/generate \\
  -H 'Content-Type: application/json' \\
  -d '{"prompt":"A continuous cinematic live-action shot in rain, moving camera, no text, no watermark.","mode":"t2v","engine":"diffusion_forcing","backend":"native","resolution":"540P","num_frames":97,"seed":42}'
```

O estado da tarefa continua em `GET /v1/tasks/{task_id}` ou `WS /ws/tasks/{task_id}`, e o MP4 concluído é entregue em `GET /v1/video/{task_id}`. Falhas de configuração, checkpoint, GPU ou execução são retornadas como `FAILED`; o sistema não substitui uma falha real por um artefato procedural.

Para produção, use o worker persistente e os dois compose files:

```bash
# execute a partir de KAIR-S-SONICA; mantenha SkyReels-V2 e checkpoints fora do Git
export SKYREELS_REPO_PATH=/caminho/absoluto/SkyReels-V2
export SKYREELS_MODELS_PATH=/caminho/absoluto/models
export SKYREELS_MODEL_SUBPATH=Skywork/SkyReels-V2-DF-1.3B-540P
docker compose -f docker-compose.yml -f docker-compose.gpu.yml up --build
```

O gateway responde em `/health` enquanto está vivo. No modo CLI, `/ready` verifica clone, entry point Diffusion Forcing e checkpoint CLI; no modo nativo, verifica runtime `torch`/`diffusers`, CUDA quando `KAIROS_SKYREELS_DEVICE=cuda` e checkpoint `*-Diffusers`. O serviço `worker` compartilha `data/`, reivindica jobs persistidos e executa a inferência sem bloquear o request HTTP. O endpoint `/docs` permanece disponível para inspeção do contrato.

Para provisionar um checkpoint nativo no host CUDA sem download implícito durante a inferência:

```bash
python3 scripts/provision_skyreels.py \\
  --repo /opt/models/SkyReels-V2 \\
  --models-root /models \\
  --native-model-id Skywork/SkyReels-V2-DF-1.3B-540P-Diffusers \\
  --revision <revisao-auditada> \\
  --download
```

O comando é protegido por lock e pode ser repetido. Sem `--download`, ele apenas valida a instalação local. O token, se necessário, deve existir somente na variável `HF_TOKEN`; o script grava apenas o nome da variável e a revisão no manifesto.

### Núcleo complementar de desenvolvimento audiovisual

A arquitetura audiovisual proposta no anexo foi incorporada como um núcleo complementar de planejamento e handoff. Ela não cria uma segunda API Flask, não substitui o `TaskStore`, não troca o worker e não instala MoviePy/gTTS/Pexels no caminho obrigatório. O endpoint `GET /v1/complementary/capabilities` descreve a camada; `POST /v1/complementary/plan` divide o briefing em cenas e produz templates que podem ser revisados antes de encaminhar cenas para `/v1/video/generate` e áudio para `/v1/orchestrate`.

```bash
curl http://localhost:8000/v1/complementary/capabilities
curl -X POST http://localhost:8000/v1/complementary/plan \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"chuva neon em videoclipe vertical","duration_seconds":10,"scene_seconds":5,"seed":42}'
```

Para testar o fluxo completo de descoberta e probes sem GPU, credenciais ou internet, use o Compose local com mocks internos:

```bash
./scripts/test_agents_compose.sh
```

Esse comando usa `docker-compose.agents.local.yml`, sobe o gateway em `http://localhost:8001`, simula o SkyReels Space e o LlamaGen dentro da rede Docker, verifica os dois probes e desmonta os containers. O Compose GPU continua independente e é reservado à inferência real com CUDA/checkpoints.

### Logging, cache e provedores de mídia opcionais

A camada complementar agora inclui logging estruturado JSON em `kairos_core.observability`, com campos de evento e redaction de tokens, chaves e senhas. O cache `MediaCache` usa SHA-256 da URL, limite de tamanho, arquivo temporário e promoção atômica. `MediaProviderChain` tenta os provedores na ordem `KAIROS_MEDIA_PROVIDER_ORDER`, inicialmente Pexels e depois Unsplash; sem as chaves `PEXELS_API_KEY`/`UNSPLASH_API_KEY`, ambos permanecem inativos e não há chamada externa.

```bash
./scripts/setup_dev.sh
# ou, se o ambiente já existir:
make lint && make test
```

O workflow [`.github/workflows/ci.yml`](.github/workflows/ci.yml) existente foi ampliado apenas para abranger branches `feat/**` e `sync/**`, compilar `tools/` e validar os manifestos Compose. Nenhum workflow ou diretório de outro desenvolvedor é removido.

### Validação no host GPU público

Para executar o Compose GPU em um host NVIDIA/CUDA com checkpoints já provisionados, use `./scripts/test_agents_gpu_compose.sh`. O script verifica `nvidia-smi`, Compose v2, readiness do backend native, capacidades do vídeo, catálogo agentico e o modo contract-first. Probes remotos ficam desligados por padrão; para testar o SkyReels Space após revisar a integração, defina `KAIROS_AGENT_AGGREGATOR_ENABLED=true`, `KAIROS_SKYREELS_SPACE_ENABLED=true` e `KAIROS_RUN_EXTERNAL_PROBES=true`. O probe LlamaGen exige adicionalmente `KAIROS_LLAMAGEN_ENABLED=true` e `LLAMAGEN_API_KEY` fornecida pelo secret manager.

### Estúdio de Gravação e Mixagem do DJ / Produtor Káiros

A primeira console do estúdio está disponível no `web-client`: captura via microfone, importação de takes, waveform de monitoramento, volume, panorama, mute, solo, reprodução de mix e exportação de bounce WAV. O áudio permanece local no navegador e não cria tarefas automaticamente. O contrato e o roadmap estão em [`docs/recording-mixing-studio.md`](docs/recording-mixing-studio.md); a próxima fase deve adicionar upload autenticado e handoff explícito para o pipeline de áudio.

### Núcleo agentico end-to-end

A equipe agentica dos anexos foi implementada como uma camada contract-first com 12 papéis: CEO, CCO, Roteirista, DoP, Designer de Som, Editor, VFX, Social, Produtor, RAG, Acessibilidade e QA. O orquestrador gera estratégia, cenas, storyboard, handoffs `VideoRequest`/`MultimediaRequest`, variantes sociais, plano de acessibilidade, memória de projeto e gates de qualidade sem exigir AutoGen, LangChain, Chroma ou um LLM para o caminho determinístico.

```bash
curl http://localhost:8000/v1/agentic/capabilities
curl -X POST http://localhost:8000/v1/agentic/run \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"clipe de rap cinematográfico em chuva neon","project_id":"campaign-001","duration_seconds":15,"scene_seconds":5,"seed":42,"submit_handoffs":false}'
```

O modo padrão produz um pacote `READY_FOR_APPROVAL` sem criar tarefas. Para encaminhar cenas e áudio ao `TaskStore`/worker existentes, o operador deve enviar simultaneamente `submit_handoffs=true` e `approve_handoffs=true`; a execução segue `KAIROS_WORKER_MODE` e não contorna `ffprobe`, staging, promoção atômica ou entrega HTTP. RAG externo exige adicionalmente `KAIROS_AGENTIC_EXTERNAL_TOOLS_ENABLED=true`; memória local fica em `KAIROS_AGENTIC_MEMORY_DIR` e não é versionada.

### Agregador de agentes externos

O catálogo de agentes é consultado sem rede em [`GET /v1/agents/capabilities`](docs/api.md), que lista `skyreels-native`, `skyreels-space` e `llamagen` com skills, algoritmos, operações, origem e prontidão. Os agentes remotos são **desabilitados por padrão**; o catálogo não faz upload, não cria gerações e não consome serviços externos.

```bash
curl http://localhost:8000/v1/agents/capabilities
```

O probe é deliberado e separado do catálogo. Depois de revisar licença, procedência, retenção e custo, habilite os gates correspondentes no ambiente e consulte, por exemplo:

```bash
export KAIROS_AGENT_AGGREGATOR_ENABLED=true
export KAIROS_SKYREELS_SPACE_ENABLED=true
# ou, separadamente:
export KAIROS_LLAMAGEN_ENABLED=true
export LLAMAGEN_API_KEY='valor fornecido pelo operador via secret manager'

curl http://localhost:8000/v1/agents/skyreels-space/probe
curl http://localhost:8000/v1/agents/llamagen/probe
```

`skyreels-space` usa o Space Gradio documentado em [`agents.md`](https://huggingface.co/spaces/fffiloni/SkyReels-V2/agents.md), com descoberta de `/config`, upload e polling SSE. `llamagen` usa o Comic API REST conforme a [documentação oficial](https://llamagen.ai/comic-api/docs), com Bearer somente pela variável de ambiente e operações de upload, geração, consulta e atualização encapsuladas no cliente. Uma geração externa nunca é iniciada pelo catálogo ou pelo probe. A chave fornecida para esta sincronização retornou HTTP 403 e precisa ser renovada antes do uso.

## Carga e observabilidade

O utilitário [`scripts/load_test_orchestrate.py`](scripts/load_test_orchestrate.py) submete tarefas concorrentes, acompanha cada `task_id` e grava latências, throughput, taxa de sucesso e resultados individuais em JSON. O cenário de referência usa 20 tarefas com concorrência 5; execute `make load` ou ajuste `REQUESTS` e `CONCURRENCY`. O relatório experimental está documentado em [`docs/load-testing.md`](docs/load-testing.md).

## Execução rápida

A execução local requer Python 3.10 ou superior. Para instalar o núcleo e as dependências de desenvolvimento, execute `python3 -m pip install -e ".[dev]"`. Em seguida, `make test` roda a suíte unitária e `make run` inicializa a API em `http://localhost:8000`.

Também é possível gerar um artefato de demonstração sem iniciar servidor:

```bash
PYTHONPATH=packages python3 scripts/run_local.py demo --duration 8 --output data/output/demo.wav
```

Depois, consulte `http://localhost:8000/docs` para a documentação interativa da API. A imagem conceitual da persona está em [`assets/persona/kairos-persona.png`](assets/persona/kairos-persona.png), e o material da apresentação da arquitetura está em [`docs/slides-kairos-architecture.md`](docs/slides-kairos-architecture.md).

## Geração e limites da base inicial

A rota `POST /v1/generate` cria uma tarefa em memória, executa o pipeline e expõe o WAV ou MP3 final. O backend inclui uma implementação procedural para testes e uma interface `AudioGenerator` para trocar o motor. A separação de stems e a geração neural são opcionais: quando não estão configuradas, o sistema não finge que executou um modelo; retorna o resultado do modo demo e registra a capacidade ausente.

Não coloque chaves, tokens ou arquivos de modelos no Git. Copie `.env.example` para `.env` somente no ambiente local. Arquivos gerados ficam em `data/output`, que é ignorado pelo Git. Referências de entrada devem ficar em `data/uploads`; o endpoint rejeita caminhos fora dos diretórios permitidos.

## Roadmap

O roadmap técnico do organismo — persistência, workers, autenticação, storage, métricas e adaptadores — está em [`docs/roadmap.md`](docs/roadmap.md). O roadmap artístico e de lançamento de KTD está em [`docs/ktd-launch-roadmap.md`](docs/ktd-launch-roadmap.md), com gates humanos para música, imagem, direitos, conteúdo e distribuição.

## Referências técnicas

[1]: https://fastapi.tiangolo.com/ "FastAPI"
[2]: https://numpy.org/doc/ "NumPy"
[3]: https://pytorch.org/audio/stable/index.html "TorchAudio"
[4]: https://github.com/facebookresearch/demucs "Demucs"
[5]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
