# FIRE IN THE FLOOD — registro de produção

## Status

**Candidato a single principal refeito; pendente de aprovação humana.** A nova composição, a base instrumental e o arco de produção são inéditos. A prova de escuta usa a referência vocal oficial de KTD como âncora de presença, mas não deve ser confundida com uma nova gravação da letra inédita.

## Arquivos

| Arquivo | Função | Status |
| --- | --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-bed-v1.wav` | Base inédita, 94 BPM, Ré menor, aproximadamente 167,34 s de material | Candidato |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav` | Prova de arranjo com a referência vocal oficial, 168 s | Candidato / escuta |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.mp3` | Versão de escuta a 320 kbps | Candidato / escuta |
| `docs/ktd-main-single-rework-concept.md` | Conceito, forma e critérios | Documento |
| `docs/ktd-main-single-rework-lyrics.md` | Letra original e direção de performance | Documento |
| `scripts/render_ktd_fire_in_the_flood.py` | Render reproduzível da prova | Script |

## Cadeia DSP

A base recebe `volume=0.52` antes da soma para preservar espaço vocal. A voz oficial passa por high-pass em 65 Hz e low-pass em 12.500 Hz. A compressão principal usa threshold de −19 dB, ratio 2,2:1, attack de 8 ms, release de 90 ms e makeup de 1,08. A camada paralela usa threshold de −32 dB, ratio 8:1, attack de 3 ms, release de 120 ms, makeup de 1,5 e ganho de 0,32. A voz saturada recebe soft clip tanh com threshold 0,82, output 1,02, parâmetro 1,15 e oversampling 4x; a proporção da soma é 1:0,35. O master usa loudness em torno de −14 LUFS, true peak de −1 dB e limiter em 0,95.

## O que mudou em relação à versão anterior

A nova faixa não depende apenas de uma frase de manifesto. Ela usa um arco de densidade: piano e voz próxima na intro, versos com espaço, lift harmônico, hook amplo com cordas, segundo verso mais veloz, bridge sem bateria e retorno final com elevação harmônica. O refrão central é **“Fire in the flood — I keep the flame alive”**, uma imagem nova que apresenta resistência e vulnerabilidade ao mesmo tempo.

## Limite de autenticidade

A tentativa de gerar uma faixa integral com a nova letra não produziu um resultado confiável nesta sessão. A prova entregue combina a nova base com `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`, que continua sendo a única referência vocal oficial aprovada. Uma tomada nova cantando `docs/ktd-main-single-rework-lyrics.md` ainda precisa ser gravada ou aprovada; a prova atual serve para avaliar inspiração, pocket, contraste e direção de produção.

## Aprovação

A música só será promovida quando KTD aprovar a letra, o hook, a performance vocal, o equilíbrio entre intimidade e expansão, a inteligibilidade do double-time, a bridge e o master final. A referência fornecida pelo usuário foi usada somente para extrair atributos abstratos e está documentada em [`docs/ktd-main-single-reference-analysis.md`](ktd-main-single-reference-analysis.md).
