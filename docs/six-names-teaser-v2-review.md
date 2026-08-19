# SIX NAMES — teaser v2 e revisão editorial

## Posição no pipeline

A montagem `six-names-hybrid-procedural-8s-validation.mp4` havia sido **reprovada** por não apresentar KTD como protagonista e por repetir uma referência visual no fechamento. A revisão v1 (`six-names-ktd-procedural-revision-v1.mp4`) corrigiu a presença de KTD com quatro imagens novas, mas manteve o mux com um áudio de referência anterior. A v2 (`assets/video/promos/tiktok/six-names-ktd-teaser-v2-8s.mp4`) preserva integralmente os quatro planos aprovados na revisão v1 e promove a peça ao áudio oficial de trabalho da faixa.

## Especificação técnica

| Campo | Valor |
| --- | --- |
| Arquivo | `assets/video/promos/tiktok/six-names-ktd-teaser-v2-8s.mp4` |
| Duração | 8,000 s (vertical 9:16, adequado a TikTok e Reels) |
| Resolução | 720 x 1280 px |
| Codec | H.264 (CRF 18) + AAC 192 kbps, faststart |
| Quadro | 24 fps, 192 quadros |
| SHA-256 | `b175c36690207c7fd9cdab6002014ded87dfda93a314b78c2c2736a496c7d52d` |
| Áudio muxado | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-proof-v2.wav` |
| BPM | 96 (beat ≈ 0,625 s; cortes a cada 2,0 s = 3,2 beats) |

## Roteiro implementado

A montagem usa o renderizador validado `scripts/render_ktd_six_names_hybrid.py` com as quatro imagens da revisão v1, todas com KTD como protagonista reconhecível. Cada imagem ocupa um único plano, sem repetição e sem retorno ao primeiro quadro.

| Tempo | Ação de KTD | Imagem | Movimento |
| --- | --- | --- | --- |
| 00,00–02,00 s | KTD canta e alcança a câmera na mesa com seis lugares | `six-names-ktd-shot-01-table-performance.png` | `push_in` |
| 02,00–04,00 s | KTD protege a vela e encara uma memória familiar | `six-names-ktd-shot-02-candle-memory.png` | `pan_right` |
| 04,00–06,00 s | KTD conduz a refeição e passa a tigela compartilhada | `six-names-ktd-shot-03-shared-meal.png` | `tilt_up` |
| 06,00–08,00 s | KTD caminha com a lanterna por um corredor doméstico | `six-names-ktd-shot-04-six-lights.png` | `push_out` |

## Conformidade com o padrão KTD

A peça preserva os elementos do vídeo de referência aprovado `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4`: sujeito centralizado no terço vertical, chiaroscuro com pretos densos, movimentos contínuos de câmera, cortes secos em intervalos regulares e ausência de texto ou gráficos sobrepostos. As restrições de não repetição do inventário visual são respeitadas — não há corredor industrial, chuva, porta metálica, olhos azuis luminosos nem paleta cinza/azul metálico; a faixa mantém a paleta âmbar doméstica com vela, mesa e memória familiar.

## Status editorial

Assim como a revisão v1, a v2 é um **candidato para avaliação humana**: a aprovação editorial prevalece sobre a validação técnica antes de qualquer uso promocional. Os critérios de aprovação permanecem — KTD reconhecível e dominante em todos os planos, ação legível em cada plano e montagem com movimento contínuo, sem aparência de sequência de imagens paradas.
