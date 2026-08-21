# Núcleo audiovisual generativo — KAIR + SkyReels-V2

## Objetivo

Este documento define a integração não destrutiva do **KAIR-S-SONICA** com o clone independente do **SkyReels-V2**. O KAIR continua sendo o orquestrador de tarefas, contratos, progresso, armazenamento e auditoria; o SkyReels permanece um backend externo, isolado por processo, dependências, checkpoint e licença.

> **Regra operacional:** o núcleo não declara que um vídeo foi gerado por modelo neural quando o backend está desabilitado, o checkpoint não está disponível ou a execução não produziu um MP4 verificável.

A integração cobre os caminhos T2V, I2V, Diffusion Forcing para vídeos longos, extensão de vídeo e controle de frame inicial/final. A ponte utiliza os entry points versionados do clone `SkyReels-V2` e não copia seus módulos para dentro do pacote principal do KAIR.

## Arquitetura

```mermaid
flowchart LR
  C[Cliente / Web / CLI] --> G[POST /v1/video/generate]
  G --> T[TaskStore SQLite\nPENDING/RUNNING/SUCCEEDED/FAILED]
  T --> W[Worker de vídeo]
  W --> V[VideoOrchestrator]
  V --> A[SkyReelsVideoAdapter]
  A --> I[Ingestão segura\ndata/uploads ou data/output]
  A --> S[Staging isolado\ndata/output/.skyreels/{task_id}]
  S --> R[Clone independente\nSkyReels-V2 CLI]
  R --> M[Checkpoint local\nsem pesos no Git]
  R --> P[MP4]
  P --> O[data/output/{task_id}.mp4]
  O --> D[GET /v1/video/{task_id}]
  O --> J[{task_id}.metadata.json]
  T --> E[WS /ws/tasks/{task_id}]
```

O worker segue o mesmo modelo do pipeline de áudio atual: cria uma tarefa, publica progresso, executa fora do request HTTP e grava um snapshot durável. A saída é copiada do staging para um nome determinístico por tarefa somente depois de localizar um MP4 produzido pelo backend. Caso o destino já exista, a promoção falha em vez de sobrescrever o artefato.

| Camada | Implementação | Responsabilidade |
| --- | --- | --- |
| Contrato | `VideoRequest` | Validar modo, engine, resolução, frames, FPS, seed e referências |
| Orquestração | `VideoOrchestrator` | Padronizar intake e progresso do ecossistema KAIR |
| Adaptador | `SkyReelsVideoAdapter` | Resolver paths, montar CLI, executar subprocesso e promover o MP4 |
| Backend | `SkyReels-V2/generate_video.py` | T2V/I2V convencional |
| Backend | `SkyReels-V2/generate_video_df.py` | Diffusion Forcing, vídeo longo, extensão e start/end frame |
| Estado | `TaskStore` | Persistir status e resultado sem expor caminhos internos |
| Entrega | `/v1/video/{task_id}` | Servir apenas o artefato publicado para a tarefa concluída |
| Auditoria | `{task_id}.metadata.json` | Registrar modo, modelo, seed, comando, logs finais e staging |

## Modos suportados

| `mode` | `engine` | Entrada exigida | Uso canônico |
| --- | --- | --- | --- |
| `t2v` | `standard` ou `diffusion_forcing` | Prompt | Primeiro plano gerativo a partir de texto |
| `i2v` | `standard` ou `diffusion_forcing` | `image_path` | Animar keyframe aprovado |
| `extend` | `diffusion_forcing` | `video_path` | Continuar um plano preservando histórico temporal |
| `start_end` | `diffusion_forcing` | `image_path` e `end_image_path` | Controlar a abertura e o fechamento do plano |

A resolução `540P` usa como default 97 frames e `720P` usa 121 frames, conforme a convenção do entry point do SkyReels. Para geração longa, `num_frames` pode ser maior que `base_num_frames`; nesse caso, o adaptador aplica `overlap_history=17` quando o operador não informa outro valor.

## Mapeamento algorítmico

| Recurso do SkyReels-V2 | Parâmetros KAIR | Decisão de integração |
| --- | --- | --- |
| Diffusion Forcing | `engine=diffusion_forcing`, `ar_step`, `base_num_frames`, `overlap_history`, `addnoise_condition` | Caminho padrão para planos longos e continuidade temporal |
| Synchronous sampling | `ar_step=0` | Mais simples para planos curtos e testes de referência |
| Asynchronous/autoregressive sampling | `ar_step>0`, `causal_block_size>1` | Exige configuração explícita para evitar blocos incompatíveis |
| Text-to-video | `mode=t2v` sem imagem | Requer checkpoint T2V compatível |
| Image-to-video | `mode=i2v`, `image_path` | Requer keyframe em diretório permitido e checkpoint I2V compatível |
| Start/end frame control | `mode=start_end`, `image_path`, `end_image_path` | Mantém o fechamento do plano sob controle declarativo |
| Video extension | `mode=extend`, `video_path` | Preserva o prefixo como referência temporal do novo trecho |
| Prompt enhancer | `prompt_enhancer=true` | Permitido apenas para T2V, seguindo a restrição do CLI oficial |
| TeaCache | `teacache`, `teacache_thresh`, `use_ret_steps` | Otimização opcional; qualidade deve ser revisada humanamente |
| Offload | `offload=true` | Default para reduzir pressão de VRAM |
| Multi-GPU USP | `use_usp=true`, `seed` obrigatório | Só habilitar com ambiente distribuído validado |

O Diffusion Forcing trabalha com níveis de ruído variáveis por token e usa tokens mais limpos como contexto para recuperar tokens mais ruidosos; o mecanismo permite estender a sequência a partir do histórico final do trecho anterior [1]. O adaptador não reimplementa esse algoritmo: ele preserva o código oficial em seu clone e expõe seus parâmetros de forma tipada.

## Contrato HTTP

### Enfileirar uma geração

```http
POST /v1/video/generate
Content-Type: application/json
```

```json
{
  "prompt": "Cinematic live-action editorial rap music video, continuous rain, moving camera, no text, no watermark.",
  "mode": "i2v",
  "engine": "diffusion_forcing",
  "resolution": "540P",
  "image_path": "ktd-fire-in-the-flood-s01-approved-portrait-keyframe.png",
  "num_frames": 97,
  "fps": 24,
  "inference_steps": 30,
  "guidance_scale": 6.0,
  "shift": 8.0,
  "seed": 42,
  "offload": true
}
```

A resposta é `202 Accepted` com `task_id`. O estado é consultado em `GET /v1/tasks/{task_id}` ou acompanhado em `WS /ws/tasks/{task_id}`. Ao concluir, `artifact_url` aponta para `/v1/video/{task_id}` e `result.video` contém o resumo da execução. A documentação interativa fica disponível no `/docs` do gateway.

### Convenções de paths

Referências visuais e vídeos de entrada só podem estar em `KAIROS_UPLOAD_DIR` ou `KAIROS_OUTPUT_DIR`, após resolução canônica do caminho. O endpoint não aceita leitura arbitrária do host, e os pesos do modelo não são aceitos como upload da API. O operador deve montar o checkpoint em um caminho local conhecido no ambiente de inferência.

## Configuração segura

O backend está **desativado por padrão**. Para habilitá-lo, o ambiente precisa declarar explicitamente o clone, o checkpoint e a permissão operacional. O exemplo versionado em `.env.example` usa caminhos ilustrativos e não contém pesos nem credenciais.

| Variável | Default | Observação |
| --- | --- | --- |
| `KAIROS_ENABLE_SKYREELS` | `false` | Gate explícito do backend |
| `KAIROS_SKYREELS_REPO` | vazio | Caminho do clone independente |
| `KAIROS_SKYREELS_MODEL_ID` | vazio | Caminho local do checkpoint ou id remoto autorizado |
| `KAIROS_SKYREELS_PYTHON` | `python3` | Interpretador do ambiente SkyReels |
| `KAIROS_SKYREELS_ALLOW_MODEL_DOWNLOAD` | `false` | Bloqueia download implícito por padrão |
| `KAIROS_SKYREELS_TIMEOUT_SECONDS` | `3600` | Limite de uma execução do worker |

O repositório SkyReels informa requisitos de VRAM muito superiores ao perfil CPU do MVP do KAIR: a documentação reporta aproximadamente 14,7 GB para o modelo 1.3B em 540P e cerca de 51,2 GB para o 14B em 540P [2]. Portanto, o teste unitário deste núcleo é deliberadamente um dry-run do contrato e da segurança; a inferência real requer um ambiente CUDA compatível, dependências do clone e checkpoints autorizados.

## Integração com cenas canônicas

A fila existente de `Fire in the Flood` continua sendo a autoridade editorial para duração, keyframes, prompts e gates. Esta integração não altera seu status `blocked_audio_alignment`, não promove cenas automaticamente e não substitui a revisão humana. Cada item de fila pode ser convertido em um `VideoRequest` quando o gate de áudio, direitos, identidade visual e aprovação artística estiver liberado.

Para uma obra de múltiplos planos, o fluxo recomendado é gerar cada cena em uma tarefa própria, usar o keyframe aprovado quando disponível, preservar o `seed` e registrar o `task_id` produzido no relatório de produção. A montagem, normalização de 720×1280 a 24 fps e mux com a master permanecem responsabilidades do assembly downstream já existente; a geração neural não deve apagar ou reescrever masters históricos.

## Direitos, segurança e operação

A licença do SkyReels exige observância da **Skywork Community License** e inclui restrições de uso e responsabilidade que devem ser revisadas antes de distribuição comercial [3]. O KAIR registra o backend e o modelo no sidecar, mas não substitui a avaliação jurídica, a revisão de procedência dos dados ou a aprovação do titular da identidade visual e vocal.

Antes de exposição em internet, a documentação do KAIR recomenda autenticação, limites de tamanho, validação MIME, checksum, expiração de artefatos, métricas, logs estruturados e isolamento de workers. O novo endpoint herda o modelo assíncrono existente, mas a fila em threads deve ser substituída por worker durável em produção, especialmente porque a inferência pode durar minutos ou horas.

## Referências

[1]: https://arxiv.org/abs/2504.13074 "SkyReels-V2 technical report"
[2]: https://github.com/SkyworkAI/SkyReels-V2#quickstart "SkyReels-V2 Quickstart and model requirements"
[3]: https://github.com/SkyworkAI/Skywork/blob/main/Skywork%20Community%20License.pdf "Skywork Community License"
