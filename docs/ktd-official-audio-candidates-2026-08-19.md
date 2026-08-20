# KTD — lista de áudios das 3 músicas para aprovação definitiva

## Objetivo

Estabelecer, com aprovação humana explícita, quais arquivos MP3 e WAV de cada faixa são os **definitivos de trabalho** para todo material futuro (muxagem de vídeo, distribuição, teasers e clipes). Até a aprovação, nenhum material novo usa nenhum destes arquivos como fonte definitiva. Regra adotada: **sempre perguntar ao usuário antes de iniciar o desenvolvimento de novos materiais**.

## Música 1 — UNLEASH THE DRAGON (single de estreia, 102 BPM, Fá menor, ~150 s)

| # | Arquivo | Formato | Duração | Status atual |
| --- | --- | --- | --- | --- |
| 1 | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` | WAV | 150,000 s | Usado no clipe v1; **PROVADO por batidas e mixagem fora de sincronia** |
| 2 | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3` | MP3 | 150,047 s | Mesmo conteúdo do #1 |
| 3 | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav` | WAV | 146,573 s | Base instrumental candidata |
| 4 | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-vocal-take-v2.wav` | WAV | 148,846 s | Tomada vocal v2 (validação apontou repetições; letra não literal) |

## Música 2 — SIX NAMES (segundo single, 96 BPM, ~165 s)

| # | Arquivo | Formato | Duração | Status atual |
| --- | --- | --- | --- | --- |
| 1 | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-proof-v2.wav` | WAV | 165,198 s | Usado no teaser v2 aprovado em workflow (mux) |
| 2 | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-proof-v2.mp3` | MP3 | 165,224 s | Mesmo conteúdo do #1 |
| 3 | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` | WAV | 165,198 s | Versão pré-release (hash difere do proof-v2) |
| 4 | `assets/audio/releases/ktd-second-single-six-names-original-proof-v1.wav` | WAV | 159,713 s | Prova original v1 |
| 5 | `assets/audio/releases/ktd-second-single-six-names-v1-pre-release-master-v1.wav` | WAV | 159,713 s | Master pré-release v1 |

## Música 3 — GOLDEN SCARS (terceiro single, ~116 s)

| # | Arquivo | Formato | Duração | Status atual |
| --- | --- | --- | --- | --- |
| 1 | `assets/audio/releases/ktd-third-single-golden-scars-trend-proof-v3.wav` | WAV | 116,062 s | Prova v3 mais recente |
| 2 | `assets/audio/releases/ktd-third-single-golden-scars-trend-proof-v3.mp3` | MP3 | 116,088 s | Mesmo conteúdo do #1 |
| 3 | `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.wav` | WAV | 116,062 s | Pré-release v1 (hash difere do proof-v3) |

## Notas de contexto

- A reprovação de 19/08/2026 declarou `proof-v1` de UNLEASH THE DRAGON reprovado por **batidas e mixagem fora de sincronia**. A nova mixagem alinhada à referência rítmica deve ser aprovada antes da próxima muxagem de vídeo desta faixa.
- Os hashes SHA-256 completos dos arquivos constam de `docs/audio-metadata-id3-2026-08-19.md` e do inventário `docs/visual-nonrepetition-inventory.json` (ativos de mídia).
- Arquivos em `assets/audio/trials/` e demos vocais são material de experimentação e não entram nesta lista de aprovação definitiva.

## DECISÃO EDITORIAL — APROVAÇÕES DEFINITIVAS (2026-08-19)

Todos os arquivos enviados pelo usuário foram verificados por **hash SHA-256 idêntico** aos que já existem no repositório — nenhum arquivo novo foi criado nem sobrescrito; a aprovação apenas designa arquivos existentes como definitivos.

| Faixa | Arquivo aprovado (WAV) | Arquivo aprovado (MP3) | Hash SHA-256 (prefixo) |
| --- | --- | --- | --- |
| Música principal — FIRE IN THE FLOOD | `ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` (168,000 s) | `...mix-v4.mp3` (168,046 s) | `a8668295687e...` / `29c97dc68f48...` |
| Música 2 — SIX NAMES | `ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` (165,198 s) | `...pre-release-v2.mp3` (165,224 s) | `4f0b53930b29...` / `ffa5aa9198cd...` |
| Música 3 — GOLDEN SCARS | `ktd-third-single-golden-scars-trend-pre-release-v1.wav` (116,062 s) | `...pre-release-v1.mp3` (116,088 s) | `8ff81301c872...` / `eed1257ee42c...` |

O **vídeo de referência oficial fixa** também foi reconfirmado: `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4` (hash `0b5d4f2b996c...`), padrão obrigatório para todos os materiais MP4 do projeto.

**Observação importante**: a música 1 (UNLEASH THE DRAGON) **NÃO teve nenhum áudio aprovado** nesta decisão — a prova `proof-v1` permanece reprovada por batidas/mixagem fora de sincronia. Material de vídeo desta faixa deve aguardar a nova mixagem alinhada e sua aprovação explícita antes de qualquer muxagem definitiva.

### Regra processual adotada

A partir desta data, **nenhum material novo (vídeo, teaser ou muxagem) é desenvolvido sem aprovação explícita prévia do usuário** para cada insumo (áudio, keyframe ou clipe), conforme instrução editorial.

## DECISÃO EDITORIAL COMPLEMENTAR — LIBERAÇÃO DO CLIPE 1 (2026-08-19)

O usuário aprovou oficialmente o clipe real de 10 s do camarote de UNLEASH THE DRAGON (`assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s.mp4`) e autorizou a **muxagem definitiva com o áudio de trabalho `ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav`, trecho 28,5–38,5 s** (hook com maior energia RMS da faixa, verificado por transcrição). O arquivo muxado `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4` é liberado como **versão final do clipe 1**. Fade-in de 0,3 s e fade-out de 0,5 s. A designação desta mixagem é pontual para o clipe 1; a aprovação de uma mixagem definitiva de distribuição da faixa continua pendente.
