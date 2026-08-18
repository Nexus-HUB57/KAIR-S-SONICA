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

## Artista principal

O artista principal é a presença humana do universo. Káiros atua como seu DJ, maestro e orquestrador, responsável por batidas, melodia, produção, coerência de carreira e coordenação do pipeline. A identidade visual original do artista está documentada em [`docs/artist-principal.md`](docs/artist-principal.md), com manifesto em [`personas/artist-principal/manifest.json`](personas/artist-principal/manifest.json) e retrato oficial em [`assets/persona/artista-principal-diamante.png`](assets/persona/artista-principal-diamante.png).

A voz original do artista está descrita em [`personas/artist-principal/voice-profile.md`](personas/artist-principal/voice-profile.md). A primeira amostra falada em português brasileiro está em [`assets/audio/artista-principal-voz-demo.wav`](assets/audio/artista-principal-voz-demo.wav), com timbre grave, quente, controlado e levemente áspero, sem imitar nenhuma pessoa real.

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
| Gateway | API HTTP e eventos WebSocket | `services.api.main` | Fila distribuída, autenticação e storage S3 |
| Cliente | Formulário responsivo e acompanhamento de tarefa | `web-client` | Editor multifaixa e Web Audio API |

O diagrama detalhado e as decisões de engenharia estão em [`docs/architecture.md`](docs/architecture.md), o fluxo específico da central multimídia está em [`docs/multimedia-architecture.md`](docs/multimedia-architecture.md), e o contrato HTTP está em [`docs/api.md`](docs/api.md).

## Central multimídia

O endpoint `POST /v1/orchestrate` coordena uma referência de áudio opcional, análise técnica, transcrição e geração. Para processamento avançado, instale `pip install -e ".[multimedia]"`; para transcrição local, o backend Faster-Whisper também pode ser instalado por `pip install -r requirements/transcription.txt`. Sem esse backend, o modo `sidecar` lê um arquivo `.txt` ou `.json` ao lado da referência e mantém a execução reproduzível.

```bash
curl -X POST http://localhost:8000/v1/orchestrate \\
  -H 'Content-Type: application/json' \\
  -d @examples/requests/orchestrate.json
```

A tarefa expõe progresso por `GET /v1/tasks/{task_id}` e `WS /ws/tasks/{task_id}`. Quando concluída, o cliente pode buscar áudio, transcrição e metadados em `/v1/audio`, `/v1/transcript` e `/v1/metadata`.

O cliente web inclui um painel Live Ops que acompanha múltiplas tarefas pelo WebSocket, exibe progresso, estado de conexão, mensagens do worker e links para os artefatos. Execute-o com `cd web-client && npm install && npm run dev` e use `VITE_API_BASE` para apontar ao gateway.

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

O próximo ciclo deve adicionar persistência de tarefas, Redis ou outro broker, autenticação, armazenamento de objetos, métricas, streaming PCM por WebSocket e adaptadores testados para modelos open-source com licenças compatíveis. A política de integração está documentada em [`docs/roadmap.md`](docs/roadmap.md).

## Referências técnicas

[1]: https://fastapi.tiangolo.com/ "FastAPI"
[2]: https://numpy.org/doc/ "NumPy"
[3]: https://pytorch.org/audio/stable/index.html "TorchAudio"
[4]: https://github.com/facebookresearch/demucs "Demucs"
[5]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
