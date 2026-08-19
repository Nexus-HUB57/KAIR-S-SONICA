# UNLEASH THE DRAGON — programação de geração dos clipes reais restantes

## Contexto

A geração de vídeo por IA no plano atual possui limite diário (1 clipe por dia). Em 2026-08-19, o **clipe real 1 (camarote)** foi gerado com sucesso: `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4` (8,000 s, 720x1280 @24fps, H264/AAC), verificado visualmente como movimento físico contínuo conforme o cânone. Os clipes 2 e 3 ficaram pendentes.

## Roteiro de retomada (cada dia de limite resetado, um clipe)

| Ordem | Dia | Clipe | Keyframe (first frame) | Descrição do movimento |
| --- | --- | --- | --- | --- |
| 1 | Dia 1 (feito) | `realgclip-01-dressing-room` | `song1-fullmv-scene-a1-dressing-room.png` | Amarrar tênis, erguer o olhar para a câmera, dolly-in |
| 2 | Dia 2 (após reset) | `realgclip-02-door-to-stage` | `song1-unleash-the-dragon-door-to-stage.png` | Empurrar a porta do palco, travessia em passada firme, steadicam por trás |
| 3 | Dia 3 (após reset) | `realgclip-03-hook-perf` | `song1-fullmv-scene-c3-hook-perf.png` | Performance no microfone, gesticulação, luzes pulsando, câmera em arco |

Parâmetros fixos de cada geração: modelo gemini-omni-flash-preview, portrait 9:16, 720p, 8 s, sem áudio gerado, keyframe como primeiro frame, prompt descrevendo movimento físico contínuo (ver `docs/unleash-the-dragon-music-video-v2-full-script.md`).

## Pós-geração

Após cada geração: verificação técnica (ffprobe: duração exata 8,000 s, 720x1280 @24fps), verificação visual contra o cânone (movimento contínuo, identidade KTD, paleta, sem texto, sem elementos de outras faixas), aprovação ou regeneração, comit e push seguros (adições apenas). Com os 3 clipes aprovados, a montagem do teaser v2 (24 s, hard cuts) é feita com ffmpeg e enviada para revisão editorial. A **muxagem com áudio fica bloqueada** até a aprovação da nova mixagem de UNLEASH THE DRAGON.
