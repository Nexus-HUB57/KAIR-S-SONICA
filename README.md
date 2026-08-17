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

## Visão da arquitetura

| Camada | Responsabilidade | Implementação inicial | Extensão prevista |
| --- | --- | --- | --- |
| Maestro | Extrair BPM, tonalidade, escala, gênero e seções | `kairos_core.agents.maestro` | LLM estruturado e RAG de documentação |
| Rhythm | Gerar grade de eventos, swing e humanização | `kairos_core.agents.rhythm` | MPC micro-timing e análise de performance |
| Generator | Produzir áudio a partir do plano | `ProceduralDemoGenerator` | Adaptadores MusicGen/Lyria/Bark |
| Vocal/Lyric | Organizar letra e intenção vocal | `kairos_core.agents.vocal` | RVC/TTS com consentimento e modelos licenciados |
| DSP | Saturação, ganho, limitação e preparação de stems | `kairos_core.audio.dsp` | Pedalboard, Librosa, Essentia e Torchaudio |
| Master/MP3 | Renderizar WAV e transcodificar com FFmpeg/LAME | `kairos_core.audio.transcode` | Presets de distribuição e streaming |
| Gateway | API HTTP e eventos WebSocket | `services.api.main` | Fila distribuída, autenticação e storage S3 |
| Cliente | Formulário responsivo e acompanhamento de tarefa | `web-client` | Editor multifaixa e Web Audio API |

O diagrama detalhado e as decisões de engenharia estão em [`docs/architecture.md`](docs/architecture.md), e o contrato HTTP está em [`docs/api.md`](docs/api.md).

## Execução rápida

A execução local requer Python 3.10 ou superior. Para instalar o núcleo e as dependências de desenvolvimento, execute `python3 -m pip install -e ".[dev]"`. Em seguida, `make test` roda a suíte unitária e `make run` inicializa a API em `http://localhost:8000`.

Também é possível gerar um artefato de demonstração sem iniciar servidor:

```bash
PYTHONPATH=packages python3 scripts/run_local.py demo --duration 8 --output data/output/demo.wav
```

Depois, consulte `http://localhost:8000/docs` para a documentação interativa da API. O cliente web pode ser executado com `cd web-client && npm install && npm run dev`; a variável `VITE_API_BASE` permite apontar para outro gateway.

## Geração e limites da base inicial

A rota `POST /v1/generate` cria uma tarefa em memória, executa o pipeline e expõe o WAV ou MP3 final. O backend inclui uma implementação procedural para testes e uma interface `AudioGenerator` para trocar o motor. A separação de stems e a geração neural são opcionais: quando não estão configuradas, o sistema não finge que executou um modelo; retorna o resultado do modo demo e registra a capacidade ausente.

Não coloque chaves, tokens ou arquivos de modelos no Git. Copie `.env.example` para `.env` somente no ambiente local. Arquivos gerados ficam em `data/output`, que é ignorado pelo Git.

## Roadmap

O próximo ciclo deve adicionar persistência de tarefas, Redis ou outro broker, autenticação, armazenamento de objetos, métricas, streaming PCM por WebSocket e adaptadores testados para modelos open-source com licenças compatíveis. A política de integração está documentada em [`docs/roadmap.md`](docs/roadmap.md).

## Referências técnicas

[1]: https://fastapi.tiangolo.com/ "FastAPI"
[2]: https://numpy.org/doc/ "NumPy"
[3]: https://pytorch.org/audio/stable/index.html "TorchAudio"
[4]: https://github.com/facebookresearch/demucs "Demucs"
[5]: https://ffmpeg.org/documentation.html "FFmpeg documentation"
