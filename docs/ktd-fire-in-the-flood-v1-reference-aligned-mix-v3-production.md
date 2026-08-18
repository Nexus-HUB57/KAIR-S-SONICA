# FIRE IN THE FLOOD — mix V1 reference-aligned v3

## Status

**Aprovada humanamente por KTD.** Esta é a versão promovida nesta etapa do single principal. A aprovação cobre os arquivos WAV e MP3 da mix `v1-reference-aligned-mix-v3`.

As provas `official-vocal-arrangement-proof-v1.wav/.mp3` foram **reprovadas como mixes** e permanecem no catálogo apenas para auditoria histórica. A decisão de reprovação não altera o bloqueio artístico da letra e da melodia V1; significa que aquele arranjo/mix específico não deve ser promovido.

## Arquivos promovidos

| Arquivo | Função | Estado |
| --- | --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav` | Master PCM da mix aprovada | Aprovado humanamente |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.mp3` | Escuta MP3 a 320 kbps | Aprovado humanamente |

As cópias de distribuição estão em `personas/artist-principal/media/audio/releases/` e foram verificadas byte a byte contra os arquivos canônicos.

## O que foi preservado

A letra aprovada não foi reescrita. A melodia de fundo V1 também não foi recriada, transposta, acelerada ou substituída. A reconstrução usou a separação técnica da prova V1 para conservar o vocal e o stem harmônico/melódico (`other`), mantendo a posição temporal de 168 segundos.

A prova de arranjo V1 reprovada não é usada como ativo promovido. O arquivo continua versionado para auditoria e comparação histórica, conforme a regra do projeto de não apagar criações anteriores.

## O que foi substituído

A bateria e o baixo que causavam desencontro foram removidos da reconstrução. O novo groove foi gerado em `scripts/generate_fire_in_the_flood_reference_aligned_groove.py`, na grade original da V1:

| Parâmetro | Decisão |
| --- | --- |
| Grade temporal | 94 BPM, 4/4, compatível com o arranjo V1 |
| Groove | Síncopa “stepping”, swing microtemporal apenas em hits secundários |
| Kick | Downbeat firme e padrões sincopados curtos, sem antecipar a frase vocal |
| Snare | Âncoras regulares em 2 e 4, com espaço para a voz |
| Baixo | Subgrave curto, colado ao kick e sem contraponto melódico concorrente |
| Harmonia de suporte | Stabs menores curtos, escuros e funcionais, usados como textura rítmica; não são cópia da referência |
| Forma | Variações de densidade em blocos de oito compassos, com retiradas breves antes das reentradas |

A referência externa foi usada somente para atributos abstratos de groove, densidade, textura e relação entre foreground e ritmo. Não foram copiados sample, letra, melodia, performance ou gravação.

## Cadeia de mixagem

O vocal separado recebeu high-pass em 65 Hz, low-pass em 12.500 Hz, compressão principal moderada, soft clip discreto e compressão paralela reduzida. O stem harmônico/melódico recebeu filtragem de limpeza e permaneceu como base musical. O novo groove foi filtrado, colocado abaixo da voz e submetido a ducking sidechain moderado pela presença vocal. A soma final foi normalizada para aproximadamente −14 LUFS, true peak de −1 dB e limiter em 0,95.

Não houve time-stretch, pitch-shift ou nova síntese vocal na mix aprovada.

## Validação

Os arquivos aprovados foram verificados com `ffprobe`:

| Arquivo | Duração | Codec | Amostragem | Canais |
| --- | ---: | --- | ---: | ---: |
| WAV | 168,000 s | PCM s16le | 44.100 Hz | 2 |
| MP3 | 168,046 s | MP3 | 44.100 Hz | 2 |

A aprovação humana de KTD prevalece sobre qualquer classificação automática. O inventário, o catálogo, o README, o manifesto de KTD e o manifesto do bundle apontam a mix v3 como o ativo promovido.
