# Arquitetura e fluxo de dados da central multimídia

## Escopo

A central multimídia é o caminho de execução que recebe uma intenção textual e, opcionalmente, uma referência de áudio. Ela pode inspecionar o arquivo, transcrever fala ou letra, transformar o texto em contexto musical, gerar uma nova peça e publicar artefatos com metadados. O endpoint de entrada é `POST /v1/orchestrate`; o estado é consultado por polling HTTP ou por WebSocket.

> **Princípio:** o Káiros orquestra capacidades; ele não afirma que um modelo pesado foi executado quando o modelo não está instalado. Cada backend declara suas dependências e oferece fallback ou erro explícito.

## Diagrama de arquitetura

```mermaid
flowchart LR
  U[Cliente Web/Mobile/CLI] --> G[API Gateway\nPOST /v1/orchestrate]
  G --> Q[TaskStore\nPENDING/RUNNING/SUCCEEDED/FAILED]
  Q --> W[Worker de Orquestração]
  W --> I[Ingestão segura\ndata/uploads]
  I --> P[AudioProcessor\nSoundFile / WAV fallback]
  P --> A[Análise\nduração, canais, RMS, peak, BPM opcional]
  I --> T[Transcrição]
  T --> S[Sidecar TXT/JSON]
  T --> F[Faster-Whisper opcional]
  W --> M[Maestro + TrackPlan]
  M --> R[Rhythm/Groove]
  R --> N[Generator Adapter]
  N --> D[DSP/Mix/Master]
  D --> X[WAV / MP3 FFmpeg]
  W --> J[Sidecars JSON\ntranscript + metadata]
  X --> O[data/output]
  J --> O
  O --> H[GET audio/transcript/metadata]
  Q --> E[WS /ws/tasks/{task_id}]
  E --> U
  H --> U
```

## Componentes e responsabilidades

| Componente | Responsabilidade | Entrada | Saída |
| --- | --- | --- | --- |
| API Gateway | Validar schema, criar tarefa e retornar `202` sem bloquear | `MultimediaRequest` | `task_id` |
| TaskStore | Manter estado e progresso no MVP | eventos do worker | `TaskSnapshot` |
| Ingestão segura | Resolver somente caminhos em `data/uploads` ou `data/output` | `audio_path` | `Path` validado |
| `AudioProcessor` | Decodificar, converter para mono/target rate e calcular métricas | áudio | PCM e `AudioAnalysis` |
| `SidecarTranscriber` | Ler texto ou segmentos fornecidos pelo operador | `.txt`/`.json` | `TranscriptResult` |
| `FasterWhisperTranscriber` | Executar transcrição local opcional | áudio | segmentos e idioma |
| Maestro | Criar intenção estruturada a partir de prompt/transcrição | texto + parâmetros | `TrackPlan` |
| AudioPipeline | Gerar, aplicar DSP e transcodificar | `TrackRequest` | WAV/MP3 |
| Sidecar Writer | Persistir transcrição e metadados | resultados | JSON em `data/output` |
| Delivery API | Entregar artefatos por URLs controladas | `task_id` | áudio, JSON e metadados |

## Fluxo de dados principal

### 1. Intake e validação

O cliente envia um JSON para `POST /v1/orchestrate`. `audio_path` é opcional. Quando informado, o caminho relativo é resolvido dentro de `KAIROS_UPLOAD_DIR`; caminhos absolutos só são aceitos se já estiverem dentro de `data/uploads` ou `data/output`. Essa barreira evita que o endpoint seja usado para ler arquivos arbitrários do host.

O gateway cria uma tarefa em memória e inicia um worker em thread para o MVP. Em uma implantação de produção, a mesma função deve ser deslocada para uma fila durável sem alterar o contrato do cliente.

### 2. Análise e transcrição

Se `analyze_audio=true`, o `AudioProcessor` carrega o áudio com SoundFile quando disponível. Para WAV PCM, existe um fallback na biblioteca padrão que permite testar o fluxo sem dependências pesadas. A análise retorna duração, sample rate, canais, frames, RMS, pico e BPM quando Librosa está instalada.

Se `transcribe=true`, o backend padrão `sidecar` procura um arquivo com o mesmo nome-base e extensão `.txt` ou `.json`. Esse modo não faz inferência e é adequado para testes, revisão humana ou transcrições produzidas por outro sistema. O backend `faster-whisper` é opcional, carrega o modelo somente quando escolhido e pode exigir download de pesos, CPU/GPU e memória compatíveis.

### 3. Conversão de contexto musical

A transcrição, quando disponível, pode preencher automaticamente `lyrics` e `prompt` se esses campos não forem enviados. O Káiros então cria um `TrackRequest`, preservando gênero, BPM, tonalidade, escala, duração, swing, humanização, formato e seed. O `MaestroAgent` transforma esses dados em `TrackPlan` e o `AudioPipeline` segue o fluxo de geração já existente.

### 4. Geração e processamento

O gerador procedural é o fallback funcional em CPU. Adaptadores neurais podem substituir o gerador, mas precisam declarar dependências, checkpoint, licença e dispositivo. Após a geração, o pipeline aplica o processamento DSP leve, grava WAV e, se solicitado, chama FFmpeg/LAME para MP3 CBR de 320 kbps.

A análise da referência e a geração são caminhos independentes. É possível analisar/transcrever um áudio sem gerar uma nova peça usando `generate_audio=false`; também é possível gerar a partir de prompt sem fornecer `audio_path`.

### 5. Persistência e entrega

O worker grava até três famílias de artefatos em `data/output`:

| Artefato | Nome | Endpoint |
| --- | --- | --- |
| Áudio | `{task_id}.wav` ou `{task_id}.mp3` | `GET /v1/audio/{task_id}` |
| Transcrição | `{task_id}.transcript.json` | `GET /v1/transcript/{task_id}` |
| Metadados | `{task_id}.metadata.json` | `GET /v1/metadata/{task_id}` |

O snapshot não expõe caminhos internos; ele retorna URLs relativas e o resultado estruturado de análise, transcrição e plano. Os sidecars preservam a rastreabilidade da execução e permitem que um cliente reconstitua o contexto sem reler o arquivo de áudio.

## Estados e observabilidade

A tarefa percorre `PENDING`, `RUNNING` e `SUCCEEDED` ou `FAILED`. Os passos de progresso são `ingesting`, `analyzing_audio`, `transcribing`, `orchestrating_generation`, `planning`, `generating`, `mastering`, `transcoding` e `completed`. O WebSocket envia snapshots periódicos, mas não substitui armazenamento durável; clientes devem tratar reconexão consultando `GET /v1/tasks/{task_id}`.

## Dependências por perfil

| Perfil | Instalação | Uso |
| --- | --- | --- |
| Base | `pip install -e .` | API, schemas, geração procedural e WAV |
| Áudio | `pip install -e ".[audio]"` | Librosa, Pedalboard, Pydub, SoundFile e Essentia |
| Multimídia | `pip install -e ".[multimedia]"` | Processamento e transcrição local opcional |
| Transcrição | `pip install -r requirements/transcription.txt` | Faster-Whisper e stack de áudio |
| Sistema | FFmpeg/LAME | MP3, probe e formatos comprimidos |

## Segurança, direitos e operação

A central não baixa modelos automaticamente no modo sidecar, não inclui credenciais no repositório e não usa APIs não oficiais. Para Faster-Whisper, o operador deve escolher o modelo, dispositivo e tipo de computação conscientemente. Para material vocal, letra ou referência de terceiros, a procedência e os direitos de uso devem ser registrados fora do código e respeitados pelo pipeline.

Em produção, substitua o `TaskStore` em memória por uma combinação de fila, banco de tarefas e armazenamento de objetos. Adicione autenticação, limites de tamanho, validação MIME, checksum, expiração de artefatos, métricas de latência, logs estruturados e isolamento de workers antes de expor a central à internet.
