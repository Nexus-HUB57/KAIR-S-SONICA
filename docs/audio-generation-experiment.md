# Experimento de geração de áudio — KTD

## Objetivo

Comparar três rotas para chegar à faixa old school de KTD e registrar de forma reproduzível o que foi aprovado, rejeitado ou deixado como especificação.

| Rota | Resultado | Ativo/registro | Decisão |
| --- | --- | --- | --- |
| 1. Gerador vocal minimalista | As tentativas de faixa completa com voz e boom bap falharam no gerador; nenhuma saída deve ser tratada como aprovada. | Logs de execução não versionados; prompts podem ser reconstituídos pelo histórico de tarefa. | Rejeitada por falha técnica do gerador. |
| 2. Base boom bap determinística | Gerou `assets/audio/ktd-old-school-boom-bap-beat-v1.mp3` com 88,8 s, mas o usuário rejeitou o ritmo e o resultado como instrumental. | `ktd-old-school-boom-bap-beat-v1.mp3` | Preservada como experimento rejeitado, não como referência musical. |
| 3. Arranjo técnico para produção externa | Especificação completa de andamento, pocket, bateria, baixo, sample, pouca guitarra, flow e estrutura. | `docs/ktd-approved-track.md` e `docs/ktd-old-school-references.md` | Aprovada como direção de produção, aguardando uma renderização musical satisfatória. |

## Critérios de aprovação

Uma nova faixa somente deve ser marcada como aprovada quando contiver voz e instrumental integrados, groove boom bap dançante, kick e snare com presença, baixo conversando com o kick, swing humano, pouca guitarra, espaço para as rimas rápidas e uma mixagem em que KTD permaneça claramente à frente. Um instrumental isolado não substitui a faixa completa.

## Integração com o orquestrador

A rota deve ser representada como tarefa multimídia no core do Káiros, com prompt, backend, versão do ativo, metadados de áudio, status, decisão de aprovação e artefatos derivados. O endpoint de orquestração já oferece o caminho para ingestão, análise, transcrição, geração e entrega; esta experiência adiciona o registro de aprovação humana ao ciclo de produção.

## Estado atual

A voz de KTD permanece aprovada em `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. A direção old school está consolidada, mas a faixa completa boom bap ainda não foi aprovada. O próximo passo técnico é gerar uma nova saída de faixa completa ou conectar uma sessão de produção externa à especificação documentada, sem promover o beat rejeitado.
