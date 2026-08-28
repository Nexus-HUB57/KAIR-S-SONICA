# Single 3 — Golden Scars — Registro de Produção dos Reels de 8s

**Artista:** KTD — Kháirus the Dragon  
**Single:** 3 — *Golden Scars*  
**Versão:** v1  
**Data:** 2026-08-28  
**Status editorial:** `TECHNICAL_TEST` / `READY_FOR_APPROVAL` somente após revisão humana dos gates de identidade  
**Protocolo:** `docs/ktd-phd-audiovisual-production-protocol-v1.md`

## Objetivo e proveniência

Foi preparado um pacote reprodutível de três reels verticais de oito segundos a partir do vídeo contínuo existente em `assets/video/aprovados/golden-scars-v1-frame-the-whole-picture-approved.mp4`. O vídeo-base foi mantido integralmente para preservar ação física, continuidade temporal e enquadramento. Cada variante recebe um trecho diferente do áudio WAV do single 3, com fade-in de 100 ms e fade-out de 500 ms. A versão limpa não contém áudio, enquanto a versão legendada contém o mesmo plano, áudio AAC e legenda aberta em safe area inferior.

A origem sonora é `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.wav`, e os hooks foram escolhidos a partir da transcrição versionada do projeto. O processo é determinístico e está em `scripts/render_golden_scars_reels_8s.py`.

## Variantes produzidas

| ID | Hook | Entrada de áudio | Arquivos |
|---|---|---:|---|
| `reel01-bring-the-truth` | “Bring the truth. Bring the scars.” | 33,0 s | clean, captioned, thumbnail |
| `reel02-bring-the-night` | “Bring the night into the stars.” | 35,4 s | clean, captioned, thumbnail |
| `reel03-bring-both` | “They want the shine, not the scars. I bring both.” | 37,9 s | clean, captioned, thumbnail |

Todos os vídeos foram renderizados em **720×1280, 9:16, 24 fps, H.264 High Profile, áudio AAC estéreo 44,1 kHz** e duração nominal de **8,000 s**. Os outputs e hashes completos estão em `outputs/single_3/reels_8s/manifest.json`.

## QC técnico

A checagem automatizada confirmou a existência dos nove artefatos principais, duração de oito segundos para todas as versões, resolução vertical correta, frame rate de 24 fps, codec H.264 para vídeo e AAC estéreo 44,1 kHz para as versões com áudio. Também foi executado `git diff --check` sem erros.

## Gates PHD e decisão editorial

O reel-base demonstra movimento corporal e acompanhamento de câmera, portanto não foi tratado como still ou animação de fotografia. Contudo, a revisão visual registrada em `video_golden-scars-v1-frame-the-whole-picture-approved_analysis_20260828_181834.md` observou **brilho ocular azul não natural** e **oscilações sutis no desenho das tatuagens** entre cortes. De acordo com os códigos `ID-02` e `ID-03` do protocolo, essas ocorrências bloqueiam publicação até correção ou ratificação explícita da autoridade artística.

Assim, os renders são entregues como **material de desenvolvimento e teste técnico**, não como `APPROVED` ou `RELEASED`. O próximo gate obrigatório é a revisão humana de identidade contra a tríade canônica (`assets/persona/ktd-visual-master.png`, `assets/persona/artista-principal-diamante.png` e `assets/persona/ktd-physical-turnaround-sheet.png`), seguida de aprovação da versão exata, do canal e do trecho de áudio.

## Pacote mínimo gerado

O diretório de saída contém três vídeos sem legenda, três vídeos com legenda aberta, três thumbnails, três arquivos ASS de legenda e um manifesto JSON com parâmetros, proveniência, probes técnicos e SHA-256. Nenhum arquivo deve ser publicado antes da decisão humana documentada.

## Próxima ação recomendada

Submeter as três variantes à autoridade artística para escolher o hook e validar identidade/continuidade. Se `ID-02` ou `ID-03` forem confirmados, retornar o plano-base para reconstrução visual antes de qualquer nova legenda, distribuição ou agendamento.
