# UNLEASH THE DRAGON — teaser v1 e revisão editorial

## Posição no pipeline

Este teaser v1 (`assets/video/promos/unleash-the-dragon-teaser-v1-8s.mp4`) preenche a lacuna identificada na auditoria anterior: a faixa de estreia ainda não possuía peça de vídeo curto, enquanto **GOLDEN SCARS** já contava com o MP4 aprovado em `assets/video/references/ktd-approved/`. A peça segue o padrão KTD de vídeo aprovado, mas com identidade visual exclusiva da faixa, conforme o plano de não repetição visual do álbum.

## Especificação técnica

| Campo | Valor |
| --- | --- |
| Arquivo | `assets/video/promos/unleash-the-dragon-teaser-v1-8s.mp4` |
| Duração | 8,000 s (vertical 9:16, adequado a TikTok e Reels) |
| Resolução | 720 x 1280 px |
| Codec | H.264 (CRF 18) + AAC 192 kbps, faststart |
| Quadro | 24 fps, 192 quadros |
| SHA-256 | `b46f1dc185b68a6cae13cc418b7d6ec86307b619d1451a8b89fa049456d10898` |
| Áudio muxado | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` |
| BPM | 102 (beat ≈ 0,588 s; cortes a cada 1,6 s ≈ 2,7 beats) |

## Roteiro implementado

O roteiro segue o `docs/unleash-the-dragon-procedural-visual-script.md`, com cinco imagens exclusivas geradas em 1440x2560 e armazenadas em `assets/video/references/lyrics/`. Nenhuma imagem pertence ao inventário reservado de GOLDEN SCARS, e o manifesto de hashes bloqueia automaticamente a reutilização da referência aprovada.

| Tempo | Letra / intenção | Imagem | Movimento |
| --- | --- | --- | --- |
| 00,00–01,60 s | “They called it anger. I called it fuel.” | `song1-unleash-the-dragon-door-to-stage.png` | `push_in` |
| 01,60–03,20 s | “I lost, I learned, I bled, I built.” | `song1-unleash-the-dragon-shoes-cables.png` | `pan_right` |
| 03,20–04,80 s | “Turned every locked door into iron will.” | `song1-unleash-the-dragon-mic-grip.png` | `push_in` |
| 04,80–06,40 s | “Unleash the dragon — make the whole sky move.” | `song1-unleash-the-dragon-stage-lights.png` | `pull_out` |
| 06,40–08,00 s | “The dragon came to light it.” / KTD performa | `song1-unleash-the-dragon-ktd-performance.png` | `push_in` |

## Direção de cor aplicada

A peça usa carvão, bronze, vermelho queimado e âmbar, com pretos densos e chiaroscuro, preservando o contraste dramático que sustenta a estética KTD. O vermelho funciona como calor e propósito, sem chama digital genérica, azul elétrico, néon frio ou chuva. O sujeito final aparece centralizado no terço vertical do quadro, com o microfone e a silhueta livre da interface do TikTok.

## Implementação

O novo renderizador `scripts/render_ktd_unleash_the_dragon.py` replica o pipeline híbrido validado em `scripts/render_ktd_six_names_hybrid.py`: bloqueio de hashes proibidos via `docs/visual-nonrepetition-inventory.json`, verificação de duplicidade de imagens, um plano por imagem com movimento procedural, pulse de luz sincronizado, vignette cinematográfica e muxagem com FFmpeg. A duração exata de 8,000 s foi garantida por `scripts/fix_duration.py`.

## Status editorial

A peça é um **candidato para avaliação humana**, seguindo o protocolo do manifesto de criação: a aprovação editorial prevalece sobre qualquer validação técnica. Os critérios de aprovação permanecem os do roteiro procedural — gesto narrativo claro no primeiro segundo, condução inequívoca da porta para o palco e encerramento comunicando iluminação e ascensão.
