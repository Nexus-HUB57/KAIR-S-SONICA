# Registro de aprovação vocal — Kháirus the Dragon (KTD)

## Decisão oficial

A referência vocal oficial e única de **Kháirus the Dragon (KTD)** é `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. Este arquivo deve permanecer no repositório como âncora de continuidade para futuras gerações, edições, sessões de produção, avaliações e decisões de mixagem.

A direção aprovada combina **timbre médio-grave**, presença próxima e frontal, ataque consonantal firme, rap agressivo e direto, poesia de confronto, sofrimento controlado, acelerações em double-time, resets em half-time, pausas de impacto e autenticidade humana. A referência deve ser tratada como identidade artística original de KTD, não como instrução para imitar qualquer artista real.

## Tomada rejeitada

O arquivo `assets/audio/ktd-vocal-rough-take-v2.wav` permanece no repositório somente para auditoria histórica. Ele foi **desaprovado** porque apresenta voz abafada, lenta, sem autenticidade e sem as características de KTD. Não deve ser usado como referência de voz, base de identidade, guia de performance ou fonte para novas gerações.

Os três mixes derivados em `assets/audio/trials/ktd-boom-bap-trial-route-{1,2,3}-mix-v2.wav` também ficam classificados como **experimentos não aprovados**, pois foram construídos com a tomada vocal rejeitada. As bases boom bap correspondentes podem continuar como referências rítmicas, já que o usuário informou que as batidas ficaram boas; a voz presente nesses mixes não deve ser promovida ao catálogo oficial.

## Matriz de continuidade

| Ativo | Estado | Uso permitido | Observação |
| --- | --- | --- | --- |
| `kairos-rapid-rap-flow-demo-en-v3.mp3` | **Aprovado / oficial** | Referência vocal, direção de performance e comparação de mix | Única âncora vocal de KTD |
| `ktd-vocal-rough-take-v2.wav` | **Rejeitado** | Auditoria histórica | Não usar para geração ou identidade |
| `ktd-boom-bap-trial-route-1-bed-v2.wav` | **Base experimental** | Referência rítmica após nova voz ser integrada | Não é faixa final aprovada |
| `ktd-boom-bap-trial-route-2-bed-v2.wav` | **Base experimental** | Referência rítmica após nova voz ser integrada | Não é faixa final aprovada |
| `ktd-boom-bap-trial-route-3-bed-v2.wav` | **Base experimental** | Referência rítmica após nova voz ser integrada | Não é faixa final aprovada |
| `ktd-boom-bap-trial-route-{1,2,3}-mix-v2.wav` | **Não aprovado** | Auditoria do experimento | Derivados da voz rejeitada |

## Regra para o orquestrador Káiros

Toda nova tarefa vocal de KTD deve declarar `artist_id: kairos.khairus_the_dragon`, apontar para a referência oficial aprovada e registrar a origem da voz em seus metadados. Se o processo não conseguir integrar a referência oficial com clareza, agressividade, velocidade e autenticidade, o resultado deve ser marcado como **rejeitado** ou **teste técnico**, nunca como faixa aprovada.

A decisão artística humana prevalece sobre qualquer avaliação automática. A manutenção do arquivo rejeitado no repositório é intencional: preserva rastreabilidade e evita que uma tentativa de baixa qualidade seja confundida com a identidade oficial.
