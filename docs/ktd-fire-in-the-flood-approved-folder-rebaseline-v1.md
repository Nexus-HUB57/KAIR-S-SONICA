# FIRE IN THE FLOOD — rebaseline pelo formato oficial aprovado

## Decisão

A pasta [`assets/video/aprovados`](https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/assets/video/aprovados) passa a ser a **autoridade única de formato** para o desenvolvimento do videoclipe de 2min48s. O tratamento anterior em landscape 16:9 foi superseded no pipeline; o vídeo final deve seguir a gramática e a proporção vertical dos reels aprovados.

## Formato confirmado

A inspeção técnica dos cinco arquivos MP4 aprovados confirmou a mesma base de publicação: **H.264, 720×1280, 24 fps, proporção 9:16, AAC estéreo a 44,1 kHz**, com planos individuais de 8 ou 10 segundos. A pasta contém duplicatas exatas de alguns arquivos; duplicatas não serão tratadas como cenas adicionais.

| Arquivo oficial | Duração | Função de referência |
|---|---:|---|
| `fire-in-the-flood-ktd-approved-dynamic-8s.mp4` | 8 s | Caminhada frontal deliberada, dolly-back, porta metálica, corredor industrial, rua molhada e passagem orgânica entre ambientes |
| `golden-scars-v1-frame-the-whole-picture-approved.mp4` | 8 s | Referência complementar de performance e enquadramento vertical |
| `six-names-ktd-clip-table-candles-10s-with-audio (1).mp4` | 10 s | Ação concreta de acender vela, mudança médio → close, fumaça, fogo e microexpressão |
| `unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4` | 10 s | Ação corporal em ambiente interno e progressão viva de câmera |
| `unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio (1).mp4` | 10 s | Duplicata SHA-256 da entrada anterior; não adicionar como nova cena |

## Gramática obrigatória

Cada plano deve conter uma microação física completa, com início, desenvolvimento e encerramento. KTD deve caminhar, tocar, abrir, atravessar, acender, carregar, conectar, respirar, performar ou reagir. A câmera deve viajar em dolly-back, travelling, arco, handheld suave, push-in físico ou acompanhamento contínuo. O ambiente deve reagir com água, chuva, vapor, fumaça, fogo, tecido, cabos, luzes, portas, reflexos ou passos.

A transição de escala do reel de Six Names — ação concreta em plano médio, aproximação progressiva, close nos olhos, mudança de luz e fumaça contínua — será aplicada nos momentos de intimidade da letra. A marcha frontal e o match cut de caminhada do reel de Fire in the Flood serão aplicados nos versos e hooks de resistência.

> Os PNGs de KTD servem apenas para identidade, referência de continuidade e preparação de keyframes. Nenhum PNG pode entrar como quadro final do videoclipe.

## Consequência para a montagem

O roteiro mantém a cobertura integral de 168 segundos em 16 blocos de 10 segundos e um encerramento de 8 segundos. A geração será vertical desde a origem; o montador fará apenas normalização de codec, duração e taxa de quadros, sem converter para landscape. A master de áudio v4 entra somente no mux final, preservando os 168,000 segundos do WAV oficial.

## Arquivos derivados atualizados

| Arquivo | Atualização |
|---|---|
| `data/releases/fire-in-the-flood-official-approved-format-v1.json` | Ficha técnica canônica 9:16 / 720×1280 / 24 fps |
| `data/releases/fire-in-the-flood-10s-scene-manifest-v1.json` | Target vertical e vínculo com a ficha canônica |
| `data/releases/fire-in-the-flood-10s-generation-queue-v1.json` | Fila em portrait |
| `scripts/assemble_fire_in_the_flood_10s.py` | Normalização e saída 720×1280 |
| `docs/ktd-fire-in-the-flood-10s-scene-script-v1.md` | Roteiro explicitamente vertical |

## Referências

[1]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/assets/video/aprovados "Pasta oficial de vídeos aprovados"

[2]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/assets/video/aprovados/fire-in-the-flood-ktd-approved-dynamic-8s.mp4 "Fire in the Flood — reel aprovado"

[3]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/assets/video/aprovados/six-names-ktd-clip-table-candles-10s-with-audio%20(1).mp4 "Six Names — reel aprovado"

[4]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md "Revisão da master de áudio v4"
