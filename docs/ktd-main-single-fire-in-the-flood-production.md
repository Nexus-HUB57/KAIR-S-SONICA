# FIRE IN THE FLOOD — registro de produção

## Status

**Registro de produção vigente.** A master promovida para esta etapa é `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav/.mp3`, com a letra alinhada à transcrição temporal v4 em `docs/ktd-main-single-rework-lyrics.md`. A v3 e as provas de arranjo V1 permanecem no catálogo apenas para auditoria e rollback histórico.

## Arquivos

| Arquivo | Função | Status |
| --- | --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-bed-v1.wav` | Base inédita, 94 BPM, Ré menor, aproximadamente 167,34 s de material | Candidato |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav` | Prova de arranjo com a referência vocal oficial, 168 s | Reprovado humanamente / histórico |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.mp3` | Versão de escuta a 320 kbps | Reprovado humanamente / histórico |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav` | Mix final da etapa anterior, 168 s | Histórico / rollback |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.mp3` | Versão de escuta da etapa anterior | Histórico / rollback |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | Master oficial vigente, 168 s | Promovido para o lyric-lock v4 |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | Versão de escuta oficial vigente | Promovido para o lyric-lock v4 |
| `docs/ktd-main-single-rework-concept.md` | Conceito, forma e critérios | Documento |
| `docs/ktd-main-single-rework-lyrics.md` | Letra v4 alinhada à master e direção de performance | Documento |
| `scripts/render_ktd_fire_in_the_flood.py` | Render reproduzível da prova | Script |

## Cadeia DSP

A base recebe `volume=0.52` antes da soma para preservar espaço vocal. A voz oficial passa por high-pass em 65 Hz e low-pass em 12.500 Hz. A compressão principal usa threshold de −19 dB, ratio 2,2:1, attack de 8 ms, release de 90 ms e makeup de 1,08. A camada paralela usa threshold de −32 dB, ratio 8:1, attack de 3 ms, release de 120 ms, makeup de 1,5 e ganho de 0,32. A voz saturada recebe soft clip tanh com threshold 0,82, output 1,02, parâmetro 1,15 e oversampling 4x; a proporção da soma é 1:0,35. O master usa loudness em torno de −14 LUFS, true peak de −1 dB e limiter em 0,95.

## O que mudou em relação à versão anterior

A faixa usa um arco de densidade alinhado à master v4: abertura próxima com fechadura e relógio, versos de pressão e disciplina, suspensão em “Now”, visão e decisão, alternância halftime/double-time, chuva e correntes, levantamento do silêncio e uma cauda instrumental final. O registro visual não deve reintroduzir o hook da letra pré-v4; a imagem central agora é a transformação de pressão em ritmo, visão e movimento.

## Limite de autenticidade

A master v4 é a autoridade sonora vigente para o videoclipe. A letra de `docs/ktd-main-single-rework-lyrics.md` foi atualizada a partir da transcrição temporal da gravação v4, com o trecho vocal detectado até 137,22 s e cauda instrumental até 168,00 s. A revisão fonética humana permanece recomendada para o lançamento, mas o desenvolvimento visual pode usar o lyric-lock v4.

## Aprovação

A música só será promovida quando KTD aprovar a letra, o hook, a performance vocal, o equilíbrio entre intimidade e expansão, a inteligibilidade do double-time, a bridge e o master final. A referência fornecida pelo usuário foi usada somente para extrair atributos abstratos e está documentada em [`docs/ktd-main-single-reference-analysis.md`](ktd-main-single-reference-analysis.md).
