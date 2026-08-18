# FIRE IN THE FLOOD V1 — mix corrigida de beat

## Decisão artística

A melodia V1 foi mantida intacta. Esta versão não reescreve letra, hook, contorno melódico, tonalidade percebida, timing da performance ou arco emocional. A única intervenção é substituir o acompanhamento por uma batida mais compatível com a referência rítmica e corrigir o equilíbrio da mixagem.

## Arquivos

| Arquivo | Função | Estado |
| --- | --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav` | Arranjo V1 congelado | Referência melódica |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-vocal-isolated-stem-v1.wav` | Stem vocal/melódico separado da V1 | Candidato técnico; não é nova gravação |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-beat-reference-fit-v3.wav` | Novo acompanhamento em 136 BPM / halftime 68 BPM | Candidato |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-rebeat-v1.wav` | V1 intacta sobre o novo beat | Candidato / escuta |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-rebeat-v1.mp3` | Versão MP3 de escuta | Candidato / escuta |
| `scripts/render_ktd_fire_in_the_flood_v1_rebeat.py` | Render reproduzível | Script |

## Correções de beat

O novo acompanhamento usa uma grade rígida de 136 BPM com sensação halftime de 68 BPM. O snare/clap permanece como âncora no terceiro tempo, enquanto o kick recebe síncopes controladas. O 808 acompanha os ataques principais do kick e usa poucos slides, somente nas terminações de frase. Os hats ficam reduzidos sob a melodia e os fills aparecem apenas nas transições. A bridge permanece rarefeita para não competir com a V1.

## Correções de mixagem

O beat é atenuado antes da soma para abrir headroom. A V1 passa por high-pass em 65 Hz e low-pass em 12.500 Hz, compressão principal em threshold −19 dB, ratio 2,2:1, attack 8 ms, release 90 ms e makeup 1,08. A compressão paralela usa threshold −32 dB, ratio 8:1, attack 3 ms, release 120 ms, makeup 1,5 e ganho 0,28. A camada principal recebe soft clip tanh com threshold 0,82, output 1,02, parâmetro 1,15 e oversampling 4x.

O instrumental sofre ducking sidechain acionado pela V1, com threshold 0,075, ratio 1,8:1, attack 5 ms, release 140 ms, detecção RMS e link average. O master usa loudnorm em torno de −14 LUFS, true peak −1 dB e limiter 0,95.

## Integridade da V1

A separação de stem foi usada somente para tornar possível a troca do acompanhamento sem deslocar a performance. O stem preserva a mesma duração de 168 segundos e o mesmo posicionamento temporal da V1. A qualidade do isolamento deve ser avaliada por escuta humana; qualquer artefato de separação impede que o arquivo seja promovido a master definitivo.

## Status

A mix está classificada como **candidata de produção**. Ela deve ser comparada diretamente com a V1 original. O critério de aprovação é simples: a melodia deve soar idêntica, mas o beat deve parecer mais contextualizado, mais firme no grid e menos desencontrado com a voz. Nenhuma mudança melódica será aceita nesta etapa.
