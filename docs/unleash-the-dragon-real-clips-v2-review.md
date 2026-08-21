# UNLEASH THE DRAGON — revisão da prévia v2 com clipes reais

## Estado da entrega

Esta entrega prossegue o desenvolvimento da música 1 migrando a montagem para **clipes de vídeo real com movimento físico contínuo**, conforme a reprovação registrada do v1 procedural. A prévia cobre o arco inicial **preparação no camarote → decisão de atravessar a porta → aproximação do palco**, sem muxagem de áudio, porque a nova mixagem ainda não foi aprovada editorialmente.

| Item | Estado | Arquivo |
| --- | --- | --- |
| Clipe real 1 — camarote | Disponível e reutilizado como entrada | `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4` |
| Clipe real 2 — porta para o palco | **Gerado nesta continuidade e normalizado sem áudio** | `assets/video/promos/unleash-the-dragon-realgclip-02-door-to-stage.mp4` |
| Prévia v2 — montagem atual | **Concluída, técnica, sem áudio** | `assets/video/promos/unleash-the-dragon-real-v2-work-in-progress-16s.mp4` |
| Clipe real 3 — performance no palco | Pendente de geração | `assets/video/references/lyrics/song1-fullmv-scene-c3-hook-perf.png` |
| Muxagem com faixa oficial | Bloqueada até nova mixagem aprovada | — |

## Direção criativa

O primeiro plano conserva o gesto íntimo de preparação: KTD está concentrado, amarra o tênis e levanta o olhar. A transição para a porta muda a energia sem abandonar a contenção: a mão gira a maçaneta de bronze, a luz âmbar invade o bastidor, a hesitação se transforma em decisão e o corpo cruza o limiar. O objetivo emocional é fazer a passagem parecer uma escolha conquistada, não apenas uma mudança de cenário.

A paleta mantém carvão, bronze envelhecido, vermelho queimado e âmbar, com sombras densas, fontes práticas e profundidade de palco. O tratamento evita a gramática visual de **GOLDEN SCARS** — corredor industrial, chuva, cadeados, olhos azuis luminosos e azul metálico — e também não repete os elementos domésticos de **SIX NAMES**.

> **Nota de continuidade de personagem.** Sempre que o peito de KTD aparecer, a geração deve usar `assets/persona/ktd-visual-master.png` como referência adicional e incluir o mapa imutável de tatuagens descrito em `docs/ktd-chest-tattoo-official-map-audit.md`. O clipe real de 10 s existente apresenta divergência no peito e não deve ser usado como fonte de identidade para novas gerações.

## Ficha técnica

| Saída | Duração | Formato | Áudio | SHA-256 |
| --- | ---: | --- | --- | --- |
| Clipe 2 normalizado | 8,000 s | H.264, 720×1280, 24 fps, yuv420p | Ausente | `ab1ed263d1b937630aa9d2656d1bd2f755c7d2fec40e099a66b0122c4afc9c32` |
| Prévia v2 | 16,000 s | H.264, 720×1280, 24 fps, yuv420p, CRF 18 | Ausente | `99278ef676ff9e834450c62ffb6139ef53e685adb6cca81a08c4b3c6de9ec0da` |

A montagem foi produzida por `scripts/assemble_unleash_the_dragon_real_v2.py`, que normaliza todos os inputs para 720×1280 a 24 fps, concatena os vídeos com corte seco, omite qualquer faixa de áudio e grava um manifesto técnico quando solicitado. O manifesto desta execução está em `work/verification/unleash_the_dragon_real_v2_manifest.json`.

## Critérios verificados

A prévia foi verificada tecnicamente com `ffprobe`: duração exata de 16,000 s, vídeo H.264 em 720×1280, 24 fps, pixel format yuv420p e ausência total de stream de áudio. O clipe 2 foi originalmente retornado com uma faixa AAC silenciosa; essa faixa foi removida por remux sem recodificação do vídeo antes da montagem.

A aprovação criativa ainda é humana e permanece pendente. A prévia deve ser considerada **work in progress**, não material promocional final. O próximo avanço natural é gerar o clipe real 3 de performance no palco e montar a sequência mínima v2 de 24 s; depois disso, os clipes 4–8 podem ampliar o arco para trabalho técnico, família, recompensa coletiva e outro com microfone solitário.

## Próxima etapa recomendada

Com o clipe 3 disponível, a montagem deve seguir `realclip-01-dressing-room → realclip-02-door-to-stage → realclip-03-hook-perf`, mantendo cortes secos e sem áudio. A revisão editorial deve observar principalmente continuidade de rosto, heterocromia, tatuagens, boca durante a performance, mãos no microfone, comportamento da fumaça, exposição entre a porta e o palco e ausência de elementos proibidos do inventário de não repetição.
