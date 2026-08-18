# FIRE IN THE FLOOD — reference-fit beat e mixagem

## Objetivo

Esta versão preserva a **letra e a melodia aprovadas como direção artística**, mas troca a base anterior por um groove moderno em 136 BPM com leitura halftime de 68 BPM. A mudança responde ao problema identificado na versão anterior: kick, 808 e transições ocupavam o espaço da frase e a sensação de tempo não coincidia com a linha vocal.

A nova referência foi usada apenas para atributos abstratos de groove. O resultado não copia letra, melodia, sample, timbre ou performance da obra consultada.

## Arquivos

| Arquivo | Função | Status |
| --- | --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-beat-reference-fit-v3.wav` | Base inédita, 136 BPM, sensação halftime de 68 BPM, 168 s | Candidato |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.wav` | Mix de comparação com a referência vocal oficial, 168 s | Candidato / escuta |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.mp3` | Versão de escuta a 320 kbps | Candidato / escuta |
| `scripts/generate_fire_in_the_flood_reference_fit_bed.py` | Geração procedural reproduzível da base | Script |
| `scripts/render_ktd_fire_in_the_flood_reference_fit.py` | Render reproduzível com ducking e DSP | Script |
| `docs/ktd-fire-in-the-flood-rhythm-reference-analysis.md` | Diagnóstico abstrato de groove e timing | Documento |

## Arquitetura temporal

A sessão usa 136 BPM em 4/4, com a voz sentida em halftime de 68 BPM. O snare/clap funciona como âncora no terceiro tempo; o kick é sincopado, mas não invade todas as sílabas. O 808 acompanha o kick em notas curtas e recebe slides apenas nos finais de frase. Os hi-hats permanecem discretos sob a melodia e abrem rolls somente nas lacunas.

A forma preserva o arco de FIRE IN THE FLOOD: intro curta, verso contido, lift, hook largo, segundo verso mais denso, hook reduzido, bridge rarefeita, hook final e outro. O último evento termina no grid; o áudio final tem 168 segundos exatos em WAV.

## Cadeia de mixagem

A base recebe `volume=0.42` para liberar headroom. A voz oficial passa por high-pass em 65 Hz, low-pass em 12.500 Hz, compressão principal em threshold −19 dB, ratio 2,2:1, attack 8 ms, release 90 ms e makeup 1,08. A camada paralela usa threshold −32 dB, ratio 8:1, attack 3 ms, release 120 ms, makeup 1,5 e ganho 0,32. A saturação vocal usa soft clip tanh com threshold 0,82, output 1,02, parâmetro 1,15 e oversampling 4x.

Antes da soma final, o instrumental sofre ducking sidechain acionado pela voz, com threshold 0,08, ratio 1,6:1, attack 4 ms, release 120 ms, makeup 1, link average e detecção RMS. O objetivo é recuar o instrumental de forma musical quando entram as palavras, especialmente no centro de 1,5–4,5 kHz. O master usa loudnorm em torno de −14 LUFS, true peak −1 dB e limiter 0,95.

## Limite de interpretação

A voz usada na prova continua sendo `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`, a única referência vocal oficial aprovada. Ela serve para verificar presença, pocket e comportamento do mix; não é a nova tomada cantando literalmente toda a letra de FIRE IN THE FLOOD. A aprovação definitiva exige uma gravação vocal nova ou uma tomada autorizada que preserve a letra e a melodia aprovadas.
