# Single #17 — Princess, Come Back

## Relatório de QC das provas musicais v1

**Estado:** `TECHNICAL_TEST` — nenhuma prova é master oficial
**Data:** 1 de setembro de 2026
**Briefing:** [`single-17-princess-no-more-production-brief-v1.md`](../../../../docs/singles/single-17-princess-no-more-production-brief-v1.md)
**Letra-base:** [`single-17-princess-no-more-lyrics-candidate-v2.md`](../../../../docs/singles/single-17-princess-no-more-lyrics-candidate-v2.md)

## Arquivos verificados

| Prova | Direção | Duração medida | Codec | Amostragem | Canais | Bitrate | SHA-256 |
|---|---|---:|---|---:|---:|---:|---|
| `single-17-princess-come-back-proof-a-melodic-v1.mp3` | Hook precoce e abordagem melódica comercial | 170,866875 s | MP3 | 44.100 Hz | 2 | 192 kbps | `12be335f75f9e90b0b08ce7487df1a067fe3aa6696f33d92e6de490e0bc7d0cd` |
| `single-17-princess-come-back-proof-b-documentary-v1.mp3` | Ponte judicial em primeiro plano e abordagem documental | 172,590958 s | MP3 | 44.100 Hz | 2 | 192 kbps | `33fcb20ca744a0808b0b7d8c38395072f68f4027d9a0bbbeb3af734e90a9806a` |

A duração-alvo operacional do briefing era 3:25–3:50. As duas provas ficaram abaixo desse intervalo, mas permanecem tecnicamente válidas como material de comparação inicial; o ajuste de duração e o corte social devem ser decididos após escuta humana, não inferidos apenas do metadata.

## Checks executados

| Check | Resultado |
|---|---|
| Decodificação via `ffprobe` | Passou para os dois arquivos. |
| Codec e canais | MP3 estéreo, 2 canais, nos dois arquivos. |
| Amostragem e bitrate | 44,1 kHz e 192 kbps, nos dois arquivos. |
| Integridade | SHA-256 registrado em `SHA256SUMS`. |
| Status de entrega | Bloqueado: não copiar para `khairus_KTD`. |
| Aprovação editorial | Pendente de escuta e decisão humana. |

## Observações de comparação

A Prova A deve ser avaliada pela memorabilidade do hook e pela clareza de “those walls were never love” em volume baixo. A Prova B deve ser avaliada pela inteligibilidade de “I crossed a line”, pela leitura da justiça seletiva e pela capacidade de chegar à recuperação sem glorificar a reação.

Este relatório não afirma qualidade artística definitiva, não substitui escuta humana e não transforma as provas em masters, lançamentos ou ativos de campanha aprovados.
