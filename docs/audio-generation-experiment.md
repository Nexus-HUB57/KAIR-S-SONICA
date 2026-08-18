# Experimento de geração musical de KTD

## Objetivo

Comparar rotas para chegar a uma faixa old school de KTD, preservando a identidade vocal oficial e registrando de forma reproduzível o que foi aprovado, rejeitado ou deixado como especificação.

## Referência vocal oficial

A voz oficial de KTD é `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. Ela permanece aprovada e deve orientar timbre, articulação, agressividade, poesia, double-time, resets em half-time, pausas de impacto e presença frontal.

`assets/audio/ktd-vocal-rough-take-v2.wav` foi **desaprovado** por apresentar voz abafada, lenta, sem autenticidade e sem as características de KTD. O arquivo não foi excluído para preservar auditoria, mas está proibido como referência de geração, interpretação ou mixagem final.

## Rotas e resultados

| Rota | Ativo/registro | Resultado | Decisão |
| --- | --- | --- | --- |
| 1. Gerador vocal integrado | Tentativa de faixa completa com voz e boom bap | O gerador falhou na saída integrada | Rejeitada por falha técnica; não promover saída inexistente |
| 2. Base boom bap determinística anterior | `assets/audio/ktd-old-school-boom-bap-beat-v1.mp3` | Instrumental com ritmo rejeitado pelo usuário | Preservada como experimento rejeitado; não usar como referência |
| 3. Arranjo técnico para produção externa | `docs/ktd-approved-track.md` | Direção de produção aprovada, aguardando renderização satisfatória | Mantida como alvo oficial |
| 4. Beat separado — rota 1 | `assets/audio/ktd-boom-bap-trial-route-1-bed-v2.wav` | Base boom bap gerada com espaço para vocal | Batida considerada boa; requer nova voz oficial antes de qualquer aprovação |
| 5. Beat separado — rota 2 | `assets/audio/ktd-boom-bap-trial-route-2-bed-v2.wav` | Base boom bap gerada com pocket mais pesado | Batida considerada boa; requer nova voz oficial antes de qualquer aprovação |
| 6. Beat separado — rota 3 | `assets/audio/ktd-boom-bap-trial-route-3-bed-v2.wav` | Base híbrida boom bap com variações de arranjo | Batida considerada boa; requer nova voz oficial antes de qualquer aprovação |
| 7. Mixes de teste 1–3 | `assets/audio/trials/ktd-boom-bap-trial-route-{1,2,3}-mix-v2.wav` | Mixes integrados com `ktd-vocal-rough-take-v2.wav` | Não aprovados; a voz usada foi rejeitada, mas as bases permanecem aproveitáveis |

## Critérios de aprovação

Uma nova faixa somente deve ser marcada como aprovada quando contiver a **referência vocal oficial de KTD** ou uma nova gravação explicitamente aprovada pelo usuário, integrada a um groove boom bap dançante, com kick e snare presentes, baixo conversando com o kick, swing humano, pouca guitarra, espaço para rimas rápidas e KTD claramente à frente na mixagem.

Um instrumental isolado pode ser classificado como **base aprovada para produção**, mas não substitui a faixa completa. Um mix que contenha a voz rejeitada não pode ser promovido, mesmo que a batida seja boa.

## Integração com o orquestrador

A rota deve ser representada como tarefa multimídia no core do Káiros, com `artist_id`, `route_id`, prompt, parâmetros, referência vocal, versão do ativo, metadados de áudio, status e decisão de aprovação. O endpoint de orquestração oferece o caminho para ingestão, análise, transcrição, geração e entrega; a aprovação humana continua sendo a autoridade final.

## Estado atual

As três bases boom bap novas foram consideradas boas como material rítmico de teste. A referência vocal oficial permanece `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. A tomada `ktd-vocal-rough-take-v2.wav` e os três mixes derivados dela estão rejeitados para uso artístico. O próximo passo de produção é regravar ou integrar a voz oficial de KTD às bases preservadas, sem reutilizar a tomada abafada.
