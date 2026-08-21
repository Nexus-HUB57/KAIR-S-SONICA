# UNLEASH THE DRAGON — revisão de identidade e handoff v2

## Estado editorial atual

A prévia v2 anterior está **reprovada e quarantinada**. O usuário identificou que o homem que aparece a partir da segunda frame do clipe da porta não é KTD. O diagnóstico é consistente com uma falha de referência: o keyframe original mostrava apenas mão, maçaneta e palco, sem KTD visível para travar a identidade. O modelo de vídeo então introduziu um personagem genérico, invalidando rosto, heterocromia e continuidade corporal.

> **Regra de produção:** nenhum arquivo em `assets/video/promos/reprovados/` pode voltar à montagem. O pipeline agora exige um manifesto de identidade com aprovação explícita para rosto, heterocromia e tatuagens antes do FFmpeg.

| Item | Estado atual | Local |
| --- | --- | --- |
| Clipe real 1 — camarote | Mantido como referência de continuidade anterior; requer revisão editorial final antes da promoção | `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4` |
| Clipe real 2 anterior — porta | **REPROVADO por identity drift e movido para quarentena** | `assets/video/promos/reprovados/unleash-the-dragon-realgclip-02-door-to-stage-identity-drift.mp4` |
| Keyframe corrigido — porta com KTD visível | **Concluído; KTD aparece desde o primeiro quadro** | `assets/video/references/lyrics/song1-unleash-the-dragon-door-to-stage-ktd-lock-v2.png` |
| Clipe real 2 corrigido | Pendente de geração após reset de quota | `assets/video/promos/unleash-the-dragon-realgclip-02-door-to-stage-ktd-lock-v2.mp4` |
| Clipe real 3 — performance no palco | Pendente de geração após reset de quota | `assets/video/promos/unleash-the-dragon-realgclip-03-hook-perf-ktd-lock-v2.mp4` |
| Prévia v2 anterior — 16 s | **REPROVADA e movida para quarentena** porque contém o clipe 2 errado | `assets/video/promos/reprovados/unleash-the-dragon-real-v2-work-in-progress-identity-drift-16s.mp4` |
| Montagem v2 de 24 s | Bloqueada corretamente até existirem os clipes 2 e 3 aprovados | — |

## Correção aplicada

Foi gerado o keyframe `song1-unleash-the-dragon-door-to-stage-ktd-lock-v2.png` a partir do cenário original, preservando a porta metálica, a maçaneta de bronze, o microfone, o dragão vermelho e o palco âmbar, mas colocando KTD inequivocamente no vão da porta. A imagem foi travada com a master visual e o turnaround físico como referências de identidade.

A nova formulação de geração exige que KTD apareça desde o primeiro quadro como homem negro de pele marrom profunda, cabeça raspada, barba cheia longa, porte atlético compacto, marcas douradas nas sobrancelhas e heterocromia natural — olho esquerdo mel/âmbar e olho direito azul-pálido. A ação prevista é física e contínua: girar a maçaneta, pausar por uma respiração, olhar para trás e atravessar a luz do palco com transferência de peso plausível.

## Gate de continuidade de pós-produção

O arquivo `data/ktd/song1-real-v2-identity-manifest.json` tornou-se a fonte operacional do gate. Ele registra as referências de identidade, os critérios de aprovação e os hashes dos arquivos bloqueados. O montador `scripts/assemble_unleash_the_dragon_real_v2.py` agora exige `--identity-manifest` e aborta antes do FFmpeg quando encontra um clipe reprovado, sem registro, com hash divergente ou sem aprovação dos três critérios críticos.

| Critério | Verificação obrigatória |
| --- | --- |
| Rosto | Cabeça raspada, barba cheia longa, formato facial, pele e marcas das sobrancelhas devem permanecer consistentes em todos os quadros visíveis. |
| Heterocromia | Olho esquerdo mel/âmbar e olho direito azul-pálido, com aparência natural; qualquer troca, uniformização ou brilho neon reprova o clipe. |
| Tatuagens | Sete marcas de garra com pontas de diamante descendo do esterno, coluna central de escamas terminando no umbigo, samurai no braço esquerdo, koi no direito e cerejeiras integradas; o Dragão Diamante de sete cabeças permanece nas costas. |
| Movimento | Gestos, respiração, articulação da boca, mãos, passos, tecido, fumaça e câmera devem ser físicos e contínuos; Ken Burns, morphing ou identidade variável reprova. |
| Exclusões | Sem homem genérico, pessoas extras, membros duplicados, chuva, corredor industrial, cadeados, azul neon, mesa doméstica ou velas. |

O teste de regressão executado com o clipe 2 reprovado falhou como esperado com `Clipe bloqueado pelo manifesto de identidade`, demonstrando que o material incorreto não volta silenciosamente à produção.

## Clipe real 3 e sequência v2 de 24 segundos

A geração do clipe 3 foi preparada com o keyframe `song1-fullmv-scene-c3-hook-perf.png`, a master visual e o turnaround como referências. O movimento planejado é uma performance física no microfone vintage: respiração, articulação natural da boca, gesto controlado da mão livre, deslocamento do paletó, fumaça e leve órbita de câmera sob luzes âmbar. A tentativa de geração foi bloqueada pelo limite diário do plano gratuito; por isso, o arquivo final ainda não existe e não foi simulado.

Assim que os dois clipes pendentes forem gerados e aprovados individualmente, a ordem obrigatória da montagem será:

| Ordem | Cena | Duração alvo | Gate |
| ---: | --- | ---: | --- |
| 1 | Camarote — preparação e olhar | 8 s | identidade anterior revisada |
| 2 | Porta — decisão e travessia | 8 s | novo vídeo deve passar o manifesto |
| 3 | Palco — hook e performance | 8 s | novo vídeo deve passar o manifesto |

A saída desejada será `assets/video/promos/unleash-the-dragon-real-v2-24s.mp4`, 720×1280 a 24 fps, H.264/yuv420p, corte seco entre clipes, sem áudio e com duração exata de 24,000 s. Até a geração dos clipes 2 e 3 corrigidos, o pipeline deve permanecer bloqueado.

## Handoff para os demais desenvolvedores

O próximo dev deve gerar primeiro o clipe 2 usando o keyframe `ktd-lock-v2`, a master e o turnaround; depois deve gerar o clipe 3 de performance com as mesmas referências. Cada arquivo deve ser verificado tecnicamente com `ffprobe`, ter qualquer faixa AAC silenciosa removida, receber hash no manifesto e passar por revisão visual humana dos três critérios críticos. Somente depois o montador deve ser executado com o manifesto atualizado e a sequência v2 de 24 segundos pode ser criada.

Não usar como referência de identidade o clipe 2 quarentenado, a prévia v2 anterior ou o clipe aprovado de outra faixa. A mixagem oficial continua fora do pipeline de montagem até que seja aprovada editorialmente.

## Referências internas

1. `assets/persona/ktd-visual-master.png` — fonte visual principal de identidade.
2. `assets/persona/ktd-physical-turnaround-sheet.png` — frente, costas e perfis.
3. `docs/ktd-chest-tattoo-official-map-audit.md` — mapa imutável de tatuagens.
4. `docs/unleash-the-dragon-music-video-v2-full-script.md` — roteiro e critérios do clipe real.
5. `data/ktd/song1-real-v2-identity-manifest.json` — gate operacional de continuidade.

## Atualização — prova v2 de 24 segundos

Foi montada uma **sequência v2 de prova** com três blocos de oito segundos: camarote real existente, prova da travessia com a imagem aprovada de KTD e prova de performance baseada no keyframe de palco. A saída tem duração exata de 24,000 segundos, 720×1280, 24 fps, H.264/yuv420p e ausência de áudio.

A performance recebeu tratamento de pós-produção de prova com contraste ligeiramente reforçado, saturação controlada, preservação do âmbar/bronze/vermelho queimado, estabilização de enquadramento e movimento de câmera lento. O tratamento não redesenha rosto, olhos ou tatuagens: a heterocromia permanece com o olho esquerdo mel/âmbar e o direito azul-pálido; o mapa de tatuagens central, samurai no braço esquerdo, koi no direito e cerejeiras são preservados pela referência visual, sem afirmar continuidade de movimento gerado.

| Novo ativo | Status | Observação |
| --- | --- | --- |
| Prova da porta — 8 s | `proof_identity_pass_keyframe` | Movimento de câmera de validação; não é travessia física gerada. |
| Prova de performance — 8 s | `proof_identity_pass_keyframe` | Tratamento de cor e câmera aplicados; não é performance vocal gerada. |
| Sequência v2 de prova — 24 s | `proof-only; real motion video pending` | Aprovável para revisão de identidade, enquadramento e ritmo; não para promoção final. |

O montador agora possui o modo `--proof`, que aceita apenas registros `proof_identity_pass_keyframe` e grava `proof_only: true` no manifesto de saída. A montagem final continua exigindo clipes reais com movimento físico aprovado e não aceita os ativos de prova como substitutos promocionais.

## Decisão editorial posterior — prova v2 reprovada

A revisão da produção rejeitou a sequência v2 de 24 segundos porque apenas o primeiro bloco, o camarote, segue o padrão audiovisual estabelecido. Os blocos de porta e performance são imagens estáticas com movimento de câmera aplicado em pós-produção; isso não constitui movimento físico de personagem nem atende ao protocolo de qualidade criativa.

A decisão substitui o status anterior da prova: os dois blocos estáticos e a montagem composta foram **retirados da rota de produção, movidos para quarentena e marcados como `rejected_static_proof`**. Eles não podem ser usados como clipes, referências promocionais ou base de aprovação de movimento.

A primeira cena real permanece preservada como único ativo elegível do conjunto atual. A sequência v2 de 24 segundos deve ser reconstruída somente quando houver dois novos takes com movimento audiovisual real: a travessia de KTD da porta e a performance de KTD no palco. Cada take deverá passar por revisão quadro a quadro de identidade, heterocromia, tatuagens, boca, mãos, peso corporal, continuidade de luz e interação com o cenário.

> **Regra de retomada:** não usar Ken Burns, zoom, pan ou qualquer deslocamento aplicado sobre imagem estática como substituto de geração de vídeo. A próxima tentativa deve entregar mudança corporal e espacial observável em cada trecho, com KTD preservado em todo o movimento.
