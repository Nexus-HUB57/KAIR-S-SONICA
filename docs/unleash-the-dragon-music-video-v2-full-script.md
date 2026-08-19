# UNLEASH THE DRAGON — status atual e roteiro visual do clipe v2 (pós-nova-mixagem)

## Premissa editorial

O clipe v1, construído sobre slides de imagens estáticas com movimento procedural (Ken Burns), foi **reprovado** em 2026-08-19, junto com a prova de arranjo `proof-v1`, reprovada por batidas e mixagem fora de sincronia. A referência obrigatória para todo material MP4 do projeto é o cânone `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4`: vídeo real com movimento físico contínuo — andar, gestos naturais, paralaxe entre planos de fundo e personagem, sombras e luz dinâmicas —, câmera fluida no estilo steadicam ou dolly, cortes secos de um a dois segundos, vertical 720x1280 a 24 fps, chiaroscuro com pretos densos e paleta restrita de carvão, bronze, vermelho queimado e âmbar, sem texto ou logotipo sobrepostos.

O gatilho de produção deste roteiro é a **aprovação da nova mixagem** de UNLEASH THE DRAGON. Nenhum material será muxado com áudio antes dessa aprovação; os clipes de vídeo podem, contudo, ser gerados e revisados individualmente sem áudio, com status de aprovação explícito por clipe.

## Status atual (2026-08-19)

| Item | Estado |
| --- | --- |
| Áudio definitivo da faixa | Não aprovado — aguarda nova mixagem alinhada e aprovação editorial |
| Teaser v1 (8 s, slides) | Reprovado junto ao clipe v1 |
| Clipe v1 completo (150 s, slides) | Reprovado em 2026-08-19 (movimento artificial, não contínuo) |
| Clipe real 1 — camarote | **Gerado e verificado**: `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4`, 8,000 s, 720x1280 @24fps, H264/AAC |
| Clipe real 2 — porta para o palco | Pendente de geração (limite diário de vídeo; gerar no reset) |
| Clipe real 3 — performance no palco | Pendente de geração (limite diário de vídeo; gerar no reset) |
| Montagem final com muxagem | Bloqueada até aprovação da nova mixagem |

A verificação do clipe real 1 confirmou movimento físico contínuo em toda a duração: KTD amarra os cadarços do tênis preto com movimentos naturais de dedos e mãos, o torso acompanha a respiração, a cabeça se ergue lentamente até o olhar direto para a câmera, e a câmera executa dolly-in estável com as luzes do espelho tremulando de forma orgânica. A identidade KTD permanece íntegra (heterocromia âmbar/azul-claro, cabeça raspada, barba longa, sete garras no peito) e nenhum elemento de GOLDEN SCARS ou SIX NAMES aparece.

## Roteiro visual planejado

A montagem v2 será composta por clipes de vídeo real de 8 segundos gerados com modelo de vídeo, cada um usando a keyframe correspondente como primeiro frame — prática que trava a identidade KTD e garante continuidade facial e de tatuagens entre planos. A ordem segue o arco narrativo da faixa: bastidor e preparação, travessia, palco, trabalho técnico, a família e recompensa.

| # | Clipe | Cena e keyframe de referência | Movimento físico descrito no prompt | Estado |
| --- | --- | --- | --- | --- |
| 1 | `realgclip-01-dressing-room` | Camarote: KTD amarrando o tênis diante do espelho de luzes | Amarra os cadarços, levanta o rosto lentamente e encara a câmera; respiração natural; luzes tremulam | Gerado e verificado |
| 2 | `realgclip-02-door-to-stage` | Porta de acesso ao palco entreaberta (`song1-unleash-the-dragon-door-to-stage.png`) | Mão tatuada empurra a porta, o vão de luz quente cresce, ele atravessa em passada firme com braços balançando; steadicam por trás em ângulo baixo | Gerar no reset diário |
| 3 | `realgclip-03-hook-perf` | Performance no palco sob luzes em leque (`song1-fullmv-scene-c3-hook-perf.png`) | KTD rima no microfone vintage, gesticula, corpo gira lentamente, luzes pulsam, fumaça se move; câmera em arco orbital | Gerar no reset diário |
| 4 | `realgclip-04-pick-grip` | Mão apertando a palheta sobre o violão (`song1-fullmv-scene-b1-pick-grip.png`) | Dedos tensionam a palheta, corda é tocada, amplificador valvulado vibrando ao fundo; braço sobe ao braço do violão | Estender pós-aprovação (opcional) |
| 5 | `realgclip-05-mic-grip` | Mão no microfone vintage com dragão vermelho ao fundo (`song1-unleash-the-dragon-mic-grip.png`) | Dedos se fecham no microfone, respiração forte, fumaça atravessa o feixe de luz; dolly-in lento | Estender pós-aprovação (opcional) |
| 6 | `realgclip-06-crowd` | Plateia em silhueta com mãos no alto (`song1-fullmv-scene-e2-crowd-silhouettes.png`) | Ondulação de braços da multidão, celulares brilhando, KTD em contraluz gesticulando na ponta do palco | Estender pós-aprovação (opcional) |
| 7 | `realgclip-07-final-perf` | KTD de braços abertos na luz principal (`song1-fullmv-scene-f1-final-perf.png`) | Braços se abrem na luz, cabeça tomba para trás, poeira dourada no feixe principal; dolly-out | Estender pós-aprovação (opcional) |
| 8 | `realgclip-08-solo-mic` | Microfone solitário sob spotlight (`song1-fullmv-scene-f2-solo-mic.png`) | Luz pulsante, fumaça subindo, flare de lente, câmera recua lentamente até o escuro | Estender pós-aprovação (opcional) |

## Regras técnicas por clipe

Cada clipe é gerado em portrait 9:16, 720p, 8 segundos, sem áudio gerado pela IA, com a keyframe correspondente como primeiro frame. A verificação de conformidade com o cânone acontece antes de qualquer avanço: duração exata de 8,000 s, movimento contínuo e crível em toda a duração (nunca Ken Burns), sujeito centralizado no terço vertical, paleta correta, ausência de texto, logotipo ou elementos de outra faixa. Um clipe reprovado é regenerado antes de entrar na montagem.

## Montagem final (após aprovação da mixagem)

Com os clipes aprovados um a um, a montagem é feita por concatenação com hard cuts, sem dissolves, em output 720x1280 @24fps, H264 CRF18 yuv420p com AAC 192 kbps, muxada com a nova mixagem aprovada — o arquivo definitivo designado na tabela oficial de áudios. A sequência mínima v2 (clipes 1 a 3, 24 segundos) pode ser enviada como teaser; a versão completa com os clipes 4 a 8 segue para revisão editorial antes de qualquer uso promocional. A duração total do clipe não deve exceder a da faixa sem decisão editorial de corte.

## Critérios de aprovação por clipe

Antes de avançar, cada clipe é aprovado por cinco critérios: movimento físico contínuo e crível em toda a duração; identidade KTD sem deformação facial ou de tatuagens; nenhum texto, logotipo ou elemento de outra faixa; câmera fluida no estilo steadicam ou dolly com cortes secos; coerência de paleta entre planos. Clipe reprovado é regenerado antes da montagem.
