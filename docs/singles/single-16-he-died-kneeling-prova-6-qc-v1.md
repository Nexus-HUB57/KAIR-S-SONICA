# Single 16 — HE DIED KNEELING — Prova 6 QC v1

**Data:** 2026-08-29
**Status:** `TECHNICAL_TEST` — candidata à aprovação humana
**Motivo da iteração:** o titular considerou a Prova 5 próxima da obra final, mas pediu mais intensidade especificamente no refrão.

## Correção aplicada

A Prova 6 mantém o rapper old school, o pocket de boom bap e o grave da Prova 5. A mudança foi concentrada no refrão: entrada antecipada, três níveis de crescimento, ataque de chant, sustentação quebrada em chest voice, lead dobrado, oitava grave, resposta coral áspera, ad-libs e explosão final. Antes de cada refrão, a bateria recua por um instante para que a primeira sílaba volte com mais impacto.

## Diagnóstico de conteúdo

A transcrição confirma hook desde aproximadamente 00:01–00:09, com repetição de “he died with honor”, “rings in his palm, not a gun” e “left the war behind”. Angel aparece explicitamente no verso e na ligação junto à fonte. A narrativa preserva a saída respeitosa, as mãos limpas, a escolha pela vida, a traição, a praça e a condenação dos covardes.

A estrutura do refrão ficou mais forte para uso comercial porque a frase é curta, repetitiva, fácil de legendar e retorna em três intensidades. Ainda é necessário ouvir se as camadas aumentam emoção ou apenas volume; a transcrição confirma a arquitetura, não a qualidade do choro ou da interpretação.

## Artefatos e métricas

| Função | Caminho | Duração | Formato | Loudness | True peak | SHA-256 |
|---|---|---:|---|---:|---:|---|
| Render bruto | `outputs/single_16/he-died-kneeling-prova-6-v6.mp3` | 173,322375 s | MP3 estéreo, 44,1 kHz, 192 kbps | −12,0 LUFS | +0,4 dBFS | `a7b39d7f56b5ad0dc2f88fc381c7907bc16a45532685a6b3b08044db484d5e5e` |
| Cópia gain-staged | `outputs/single_16/he-died-kneeling-prova-6-v6-gainstaged.mp3` | 173,348571 s | MP3 estéreo, 44,1 kHz, 320 kbps | −13,5 LUFS | −1,1 dBFS | `3c0355e0659a77f908dcc0d8f989ab0d0bc4a14abe8b176d500340ede304f627` |
| Hook vertical | `outputs/single_16/he-died-kneeling-prova-6-v6-gainstaged-hook-22s.mp3` | 22,047347 s | MP3 estéreo, 44,1 kHz, 320 kbps | −12,3 LUFS | −1,3 dBFS | `68526359564bb5b3075fb1e752760bbb69d28ccf7db82ef08b1f1e17f9d83d82` |

Todos os arquivos decodificaram integralmente. O bruto permanece preservado como origem e não é cópia de entrega por exceder 0 dBFS. A cópia gain-staged é adequada para escuta de prova, não para lançamento. Master WAV PCM, stems e pacote público continuam pendentes.

## Veredito

| Critério | Resultado | Observação |
|---|---|---|
| Rapper old school | **PASS WITH NOTE** | Mantido o pocket e o ataque da Prova 5 |
| Intensidade progressiva do refrão | **PASS STRUCTURAL / HUMAN LISTENING** | Camadas e níveis foram solicitados e a transcrição confirma repetição |
| Hook comercial | **PASS** | Entra antes de 00:08 e foi recortado em 22 s |
| Presença de Angel | **PASS** | Nome aparece no verso e na ligação |
| Dor vocal | **HUMAN REVIEW REQUIRED** | Ainda é o critério artístico decisivo |
| Grave e punch | **HUMAN REVIEW REQUIRED** | Conferir em fones, celular e mono |
| Integridade técnica | **PASS WITH NOTE** | Cópia segura em −1,1 dBFS; bruto acima do limite |
| Aprovação final | **PENDING** | Aguardando escuta e decisão do titular |

## Escuta recomendada

Comparar primeiro o hook vertical e depois os trechos 00:07–00:24, 01:15–01:35 e 02:32–02:54. O teste é verificar se o refrão agora **cresce emocionalmente** — da indignação para o grito coletivo — e não apenas fica mais alto. Se ainda faltar impacto, o próximo ajuste deve ser de performance vocal dirigida e automação de camadas, não apenas de grave ou loudness.
