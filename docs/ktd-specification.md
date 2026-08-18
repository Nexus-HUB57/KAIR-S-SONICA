# Especificação consolidada — Kháirus the Dragon (KTD)

## Identidade oficial

**Kháirus the Dragon**, abreviado **KTD**, é o artista principal do universo KAIR-S-SONICA. Ele é a presença humana, o rapper e o performer público. Káiros permanece como seu DJ, maestro, produtor e orquestrador: organiza batidas, melodia, arranjo, transcrição, geração, carreira e coerência do universo.

O ID atual da persona é `kairos.khairus_the_dragon`; `kairos.artist_principal.diamante` permanece apenas como identificador legado para compatibilidade.

## Aparência e continuidade visual

KTD é um homem negro adulto, de biotipo atlético e compacto, cabeça raspada, barba longa e cheia, sobrancelhas alinhadas com riscos dourados e heterocromia natural: um olho cor de mel e outro azul-claro. A imagem-mestre oficial é `assets/persona/ktd-visual-master.png`.

A continuidade das tatuagens é imutável. O centro do peito contém sete garras verticais do Dragão Diamante, com o pescoço e a cabeça central descendo pelo abdômen até o umbigo. O braço esquerdo recebe carpas, ondas e cerejeiras; o direito recebe samurai, armadura estilizada e nuvens orientais. A paleta é carvão/preto, cinza profundo, dourado pontual e azul-acinzentado. A referência completa está em `docs/ktd-visual-bible.md`.

As expressões podem variar de contemplação dolorida a ironia, concentração, riso espontâneo e fúria de palco. A anatomia, a heterocromia e o mapa de tattoos não variam.

## Voz e flow

A voz aprovada é um barítono médio-grave com ressonância quente no peito, borda levemente áspera, dicção clara e ataque direto. O flow usa rap agressivo, rimas internas densas, double-time em rajadas, resets em half-time, pausas de impacto e sofrimento audível sem perder controle.

A demo vocal principal é `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. As versões anteriores permanecem como histórico, não como referência primária.

## Direção musical atual

A direção aprovada para a produção é rap americano old school/boom bap com bateria dançante e humana. Kick seco, snare estalado nos tempos 2 e 4, hi-hat fechado, swing leve, baixo encorpado sincronizado ao kick, loops originais de soul/jazz/funk e pouca guitarra. O vocal deve ocupar o plano frontal; o instrumental deve criar pocket, não competir com as rimas.

A direção técnica está documentada em `docs/ktd-old-school-references.md` e `docs/ktd-approved-track.md`. O arquivo `assets/audio/ktd-old-school-boom-bap-beat-v1.mp3` é um experimento instrumental rejeitado e não deve ser tratado como faixa aprovada.

## Orquestração

O pipeline do Káiros coordena ingestão, análise de áudio, transcrição, planejamento de track, geração, DSP, masterização, artefatos, WebSocket e observabilidade. A produção musical oficial deve registrar sempre: identidade da persona, versão do prompt, direção de flow, BPM, instrumentação, status do ativo e decisão de aprovação.

## Guardrails

KTD é uma criação original e não deve reproduzir o rosto, voz, sotaque exato, flow, letra, sample, melodia ou arranjo reconhecível de pessoas reais. A agressividade é performática e poética, sem violência gráfica, ameaças contra pessoas reais ou discurso de ódio. Nenhum ativo visual oficial deve conter texto, logo ou watermark não solicitado.
