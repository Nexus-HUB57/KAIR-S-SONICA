# Validação do pipeline híbrido

## Escopo

A validação cobre `scripts/render_ktd_six_names_hybrid.py`, `scripts/generate_visual_nonrepetition_inventory.py`, o inventário `docs/visual-nonrepetition-inventory.json` e o render procedural de oito segundos da Música 2.

## Resultado do render

Arquivo: `assets/video/promos/tiktok/six-names-hybrid-procedural-8s-validation.mp4`

| Propriedade | Resultado |
|---|---:|
| Duração | 8,000 s |
| Resolução | 720×1280 |
| Aspect ratio | 9:16 |
| Taxa de quadros | 24 fps |
| Vídeo | H.264, yuv420p |
| Áudio | AAC estéreo, 44,1 kHz |
| Quadros renderizados | 192 |
| Planos distintos | 4 imagens líricas de SIX NAMES |
| Música | `ktd-second-single-six-names-rebuilt-soul-proof-v2.mp3` |

## Sequência validada

| Tempo | Movimento | Arquivo |
|---|---|---|
| 00,00–02,50 s | `push_in` | `song2-six-names-lyrics-reference.png` |
| 02,50–05,00 s | `pan_right` | `song2-six-names-candle-hand.png` |
| 05,00–06,25 s | `tilt_up` | `song2-six-names-six-plates.png` |
| 06,25–07,50 s | `push_out` | `song2-six-names-hands-together.png` |
| 07,50–08,00 s | `pan_left` | `song2-six-names-lyrics-reference.png` |

A repetição final da primeira referência é intencional como retorno narrativo; ela recebe outro recorte e movimento e não é reutilizada como plano estático idêntico. A entrada da Música 1 foi removida do render após o primeiro teste, quando o diretório amplo de referências revelou o risco de seleção acidental. O script agora aceita múltiplas ocorrências explícitas de `--image`, o que torna a separação entre faixas verificável.

## Integridade e não repetição

O inventário usa SHA-256 para identificar duplicatas binárias exatas e classifica os arquivos em `GOLDEN_SCARS`, `UNLEASH_THE_DRAGON`, `SIX_NAMES` e `UNASSIGNED`. O render bloqueia somente hashes classificados como `GOLDEN_SCARS`, enquanto exige quatro imagens distintas no conjunto de SIX NAMES. Isso preserva os ativos da música 3 e impede a inclusão acidental de imagens bloqueadas.

SHA-256 detecta duplicata binária exata, não semelhança perceptual. Por isso, a revisão editorial da composição continua obrigatória quando um novo ativo for criado.

## Verificações executadas

- `python3 -m py_compile` passou nos dois scripts.
- `--help` do render foi executado com sucesso.
- `git diff --check` foi executado sem erro.
- `ffprobe` confirmou streams de vídeo e áudio válidos no MP4 de validação.
