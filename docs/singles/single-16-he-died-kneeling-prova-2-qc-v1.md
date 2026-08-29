# Single 16 — HE DIED KNEELING — Prova 2 QC v1

**Data:** 2026-08-29
**Status:** `TECHNICAL_TEST` / `READY_FOR_APPROVAL` somente para escuta humana da versão gain-staged; não é `APPROVED` nem `RELEASED`
**Fonte:** geração musical interna; render bruto preservado, cópia de conferência corrigida por ganho e hook vertical derivados sem alteração de conteúdo

## Artefatos

| Função | Caminho | SHA-256 | Observação |
|---|---|---|---|
| Render bruto gerado | `outputs/single_16/he-died-kneeling-prova-2-v2.mp3` | `763e7232cb4084c7239f50ee00d4bb2de00371f40eecde76d8ed8ff6693e47de` | MP3 estéreo, 44,1 kHz, 192 kbps, 172,120750 s; preservado como origem |
| Cópia de conferência gain-staged | `outputs/single_16/he-died-kneeling-prova-2-v2-gainstaged.mp3` | `da469d7401351c3806d7c7095a8d8750f63a08aa9076476819380fd6ce2bc811` | MP3 estéreo, 44,1 kHz, 320 kbps, 172,146939 s; −1,5 dB aplicado |
| Hook vertical | `outputs/single_16/he-died-kneeling-prova-2-v2-gainstaged-hook-22s.mp3` | `9593f5e48d3931508565add5f19a5bff9a912c29d526cb8b7cd25d2e1d0cba55` | Recorte de 22,047347 s a partir de 00:08; MP3 estéreo, 44,1 kHz, 320 kbps |
| Transcrição plain text | `outputs/single_16/he-died-kneeling-prova-2-v2_transcription_20260829_104136.txt` | `75ee88dfdd3cc734f20b328da5fb4b7e48857f00e5e053aedd52a1ec30749c69` | Transcrição automática para diagnóstico, não letra oficial |
| Transcrição JSON | `outputs/single_16/he-died-kneeling-prova-2-v2_transcription_20260829_104136.json` | `d6c0f737834747039ea17cb579ab2ec614478b9725f5edcf0bc9c0f55eeb112e` | Marcação temporal automática |

## QC técnico

O render bruto decodificou integralmente, sem erro de FFmpeg. Sua medição apresentou **−12,6 LUFS integrado** e **+0,3 dBFS de true peak**, portanto não deve ser usado como cópia de entrega. A cópia gain-staged decodificou integralmente, apresentou **−14,1 LUFS integrado**, **8,1 LU de LRA** e **−1,1 dBFS de true peak**. O hook vertical decodificou integralmente, com **−13,1 LUFS integrado**, **1,2 LU de LRA** e **−1,2 dBFS de true peak**.

A correção por ganho é uma etapa de conferência, não uma masterização final. O MP3 original foi mantido para proveniência; ainda faltam sessão, stems e master WAV PCM produzido pelo pipeline de mix/master. O alvo de 174 segundos não foi atingido exatamente: a geração entregou 172,15 segundos. A diferença é aceitável para prova de ferramenta, mas deve ser decidida antes da aprovação do master.

## Diagnóstico de conteúdo

A transcrição confirma entrada precoce do refrão em aproximadamente 00:09 e preserva os elementos centrais da história: telefonema, saída limpa, Angel, região proibida, praça, anúncio respeitoso à gangue, presença desarmada, alianças, morte ajoelhado, condenação dos covardes e fechamento “rings, not rounds”. O hook é curto, repetível e adequado para um teste de 22 segundos.

A geração não reproduz linha a linha a letra v2 registrada em `docs/singles/single-16-he-died-kneeling-lyrics-v2.md`; ela produziu uma letra vocal própria a partir do briefing. A transcrição contém imagens mais diretas de disparos (“metal rain down”, “You shot a man”) do que a letra editorial v2. Não há descrição gráfica, mas a versão vocal deve passar por decisão humana de tom antes de qualquer uso público. Se o titular exigir aderência textual exata, será necessário novo take vocal ou gravação dirigida; não se deve declarar que a prova é a gravação da letra v2.

## Veredito de prova

| Gate | Resultado | Nota |
|---|---|---|
| Decodificação integral | **PASS** | Render bruto, cópia corrigida e hook decodificaram sem erro |
| Duração | **PASS WITH NOTE** | 172,15 s, abaixo do alvo de 174 s |
| Formato de conferência | **PASS** | MP3 estéreo, 44,1 kHz; cópia principal em 320 kbps |
| Loudness | **PASS WITH NOTE** | Gain-staged em −14,1 LUFS; não é decisão final de master |
| True peak | **PASS** | Cópia principal −1,1 dBFS; bruto reprovado para entrega em +0,3 dBFS |
| Narrativa | **PASS** | História e arco emocional legíveis na transcrição |
| Hook social | **PASS WITH NOTE** | Refrão entra cedo e foi isolado em 22 s; alcance não é garantido |
| Letra oficial v2 | **REVIEW REQUIRED** | Áudio gerado é semanticamente alinhado, não linha a linha |
| Identidade vocal KTD | **HUMAN REVIEW REQUIRED** | Automação não substitui comparação com a âncora vocal oficial |
| Aprovação editorial | **PENDING** | Titular deve aprovar versão, canal e uso exatos |

## Próxima decisão recomendada

Ouvir a cópia gain-staged em fones, monitores, celular e mono, comparando-a com `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. Se a fúria, o refrão melódico e a dicção corresponderem à intenção, a versão pode avançar para masterização e pacote de aprovação. Se a voz permanecer genérica ou a linha de disparos for considerada direta demais, manter o arquivo em `TECHNICAL_TEST` e gerar um take corrigido; não promover o render por aparência viral.
