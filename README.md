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

A prova de arranjo com a referência vocal oficial está em [`assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3`](assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3), com master WAV correspondente e base inédita em `assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav`. A nova tomada vocal v2 está em `assets/audio/releases/ktd-debut-single-unleash-the-dragon-vocal-take-v2.wav`, com validação em [`docs/ktd-debut-single-vocal-take-validation.md`](docs/ktd-debut-single-vocal-take-validation.md); ela permanece como candidato de audição porque a transcrição identificou repetições e alterações de palavras. A faixa está classificada como **candidata, pendente de aprovação humana**. As tentativas de geração neural integral com a nova letra não produziram uma tomada vocal confiável; por isso, o resultado atual é uma prova de composição, arranjo e pocket com a voz oficial, não um master final anunciado como lançamento.

## Pacote profissional de lançamento de KTD

A referência histórica original foi preservada integralmente em [`Artistics_References_KTD`](Artistics_References_KTD). O manifesto de criação está em [`docs/ktd-creation-manifesto.md`](docs/ktd-creation-manifesto.md) e a apresentação profissional, em formato de press kit, está em [`docs/ktd-professional-presentation.md`](docs/ktd-professional-presentation.md). Esses documentos preservam a história de origem, a transformação do crime e da violência em disciplina, a responsabilidade com seis irmãos, a fé, o ativismo, a filantropia, a identidade visual e a relação entre KTD e Káiros, com linguagem editorial mais clara e profissional.

A playlist de lançamento foi estruturada em três letras inéditas: [`docs/ktd-launch-playlist-lyrics.md`](docs/ktd-launch-playlist-lyrics.md) contém **DRAGON IN THE MIRROR**, **SIX NAMES** e **GOLDEN SCARS**. Cada faixa possui hook original, recorte de 15–30 segundos, direção de andamento, identidade emocional e regras de produção. Os hooks foram pensados para serem memoráveis e legíveis em vídeo curto, sem promessa de viralização ou cópia de tendências existentes.

O roadmap de carreira está em [`docs/ktd-launch-roadmap.md`](docs/ktd-launch-roadmap.md), com fases de fundação, laboratório, produção, pré-lançamento, estreia e expansão. O catálogo de imagens, voz, bases, mixes e documentos está em [`docs/ktd-asset-catalog.md`](docs/ktd-asset-catalog.md). A auditoria de povoamento em [`docs/ktd-assets-upload-audit.md`](docs/ktd-assets-upload-audit.md) confirma 8 imagens e 26 áudios rastreados, totalizando 34 ativos canônicos, sem arquivos visuais ou sonoros pendentes dentro das pastas oficiais. Para facilitar o consumo pelo persona, os mesmos ativos estão organizados em [`personas/artist-principal/media/`](personas/artist-principal/media/) e indexados por [`personas/artist-principal/media-manifest.json`](personas/artist-principal/media-manifest.json). O inventário técnico reproduzível com hashes, dimensões, duração, codec e classificação está em [`data/ktd/asset-inventory.json`](data/ktd/asset-inventory.json), gerado por [`scripts/build_ktd_asset_inventory.py`](scripts/build_ktd_asset_inventory.py). A pesquisa de contexto sobre descoberta musical em vídeo curto, com fontes do TikTok/Luminate e Billboard, está em [`docs/ktd-launch-research.md`](docs/ktd-launch-research.md).

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

O roadmap técnico do organismo — persistência, workers, autenticação, storage, métricas e adaptadores — está em [`docs/roadmap.md`](docs/roadmap.md). O roadmap artístico e de lançamento de KTD está em [`docs/ktd-launch-roadmap.md`](docs/ktd-launch-roadmap.md), com gates humanos para música, imagem, direitos, conteúdo e distribuição.

## Referências técnicas

[1]: https://fastapi.tiangolo.com/ "FastAPI"
[2]: https://numpy.org/doc/ "NumPy"
[3]: https://pytorch.org/audio/stable/index.html "TorchAudio"
[4]: https://github.com/facebookresearch/demucs "Demucs"
[5]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
