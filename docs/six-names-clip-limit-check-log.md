# SIX NAMES — log de verificação do limite diário de geração de vídeo

## Contexto

O clipe real de 10 s de SIX NAMES (`docs/six-names-clip-10s-production-pack.md`) depende de uma geração de vídeo do plano gratuito, cujo limite é de **1 geração por dia**. O limite foi consumido em 19/08/2026 com o clipe de 10 s do camarote de UNLEASH THE DRAGON. A instrução do usuário é simular/verificar o reset do limite para iniciar a geração.

## Tentativas registradas

| # | Data/hora (UTC) | Resultado |
| --- | --- | --- |
| 1 | 2026-08-20 ~14:00 | Bloqueado (1/1 consumido) |
| 2 | 2026-08-20 ~14:05 | Bloqueado (1/1 consumido) |
| 3 | 2026-08-20 20:00 (esta verificação) | **Bloqueado — limite ainda não resetado** |

## Próximos passos

O pipeline completo está pronto e documentado: keyframe aprovada `assets/video/references/lyrics/song2-six-names-table-candles-v2.png`, prompt final em `docs/six-names-clip-10s-production-pack.md`, muxagem do trecho 60,0–70,0 s de `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` (fade-in 0,3 s, fade-out 0,5 s). Assim que o limite resetar (janela provável: 21/08/2026, a verificar entre 13:00 e 15:00 UTC), a geração deve ser executada imediatamente com o mesmo prompt e keyframe, seguida de muxagem e comit com segurança (pull --ff-only, push normal). Alternativa sem espera: upgrade do plano.
