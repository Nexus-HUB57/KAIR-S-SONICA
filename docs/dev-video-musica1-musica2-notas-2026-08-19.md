# Notas de desenvolvimento — videoclipes Músicas 1 e 2 (2026-08-19)

## Estado do repositório
- HEAD: `f168fdb` fix: reposiciona KTD como protagonista em six names
- Vídeo de referência aprovado: `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4` (8s, 720x1280, 24fps) — padrão KTD oficial.
- Promo GOLDEN SCARS já existe: `assets/video/promos/golden-scars-v1-frame-the-whole-picture.mp4` (idêntica à aprovada).
- Música 1 (UNLEASH THE DRAGON): docs/unleash-the-dragon-procedural-visual-script.md define roteiro 8s; referências líricas em assets/video/references/lyrics/song1-unleash-the-dragon-lyrics-reference.png. NÃO há vídeo teaser ainda. Sem renderizador de vídeo para música 1.
- Música 2 (SIX NAMES): six-names-hybrid-procedural-8s-validation.mp4 REPROVADA (não tinha KTD, repetia referência). Revisão V1 (six-names-ktd-procedural-revision-v1.mp4) é rascunho técnico pendente de aprovação editorial. 4 novos shots com KTD: shot-01-table-performance, shot-02-candle-memory, shot-03-shared-meal, shot-04-six-lights (em assets/video/promos/tiktok/).
- Roteiro SIX NAMES V1: push_in (canta na mesa), pan_right (protege vela), tilt_up (compartilha refeição), push_out (caminha com lanterna), 2s por plano.
- Script renderer: scripts/render_ktd_six_names_hybrid.py (720x1280, 24fps, H264/AAC, motion procedural, forbidden hashes GOLDEN_SCARS, mínimo 4 imagens).
- Manifesto de não repetição: docs/visual-nonrepetition-inventory.json gerado por scripts/generate_visual_nonrepetition_inventory.py.

## Padrão KTD aprovado (do doc ktd-approved-video-pattern-analysis.md)
Push-in constante e lento; hard cuts sincronizados ao downbeat; sujeito centralizado (terço central vertical); chiaroscuro; paleta desaturada/fria (GS); deep shadows; 2s iniciais de alto impacto (scroll-stopper); olhos brilhantes (assinatura, mas bloqueados para outras faixas pelo inventário de não repetição); sem texto/gráficos sobrepostos; sem logo.

## Restrições por faixa (inventário de não repetição)
- GOLDEN SCARS: corridor industrial, chuva, porta metálica, cadeados, olhos azuis luminosos.
- UNLEASH THE DRAGON: porta de palco com luz quente, vermelho-âmbar/carvão/bronze, microfone, palco; não usar azul elétrico nem chuva.
- SIX NAMES: mesa de 6 lugares, vela, refeição compartilhada, corredor doméstico com lanterna; sem cenário industrial.

## Áudios oficiais para mux
- Música 1: assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav
- Música 2: assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-proof-v2.wav (verificar versão oficial mais recente em releases)

## Resultado da execução (2026-08-19)
A música 2 (SIX NAMES) recebeu o teaser v2 em `assets/video/promos/tiktok/six-names-ktd-teaser-v2-8s.mp4` (8,000 s, 720x1280, 24 fps, H264/AAC, SHA-256 b175c36690207c7fd9cdab6002014ded87dfda93a314b78c2c2736a496c7d52d), renderizado com as quatro imagens da revisão v1 e muxado com o áudio oficial `ktd-second-single-six-names-rebuilt-soul-proof-v2.wav`. A música 1 (UNLEASH THE DRAGON) recebeu cinco imagens exclusivas em `assets/video/references/lyrics/song1-*` e o teaser v1 em `assets/video/promos/unleash-the-dragon-teaser-v1-8s.mp4` (8,000 s, SHA-256 b46f1dc185b68a6cae13cc418b7d6ec86307b619d1451a8b89fa049456d10898), muxado com `ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` a 102 BPM. Ambos usam o padrão KTD (push-in, cortes secos, sujeito centralizado, chiaroscuro, sem texto sobreposto). O inventário de não repetição foi regenerado com os hashes novos; o script `scripts/render_ktd_unleash_the_dragon.py` replica o pipeline validado da música 2; `scripts/fix_duration.py` garante a duração exata. Os docs de revisão são `docs/unleash-the-dragon-teaser-v1-review.md` e `docs/six-names-teaser-v2-review.md`. Pendente: commit seguro (sem force-push, adição de arquivos apenas) e aprovação editorial humana do usuário antes de uso promocional.

## Avaliação visual da revisão V1 (SIX NAMES)
- shot-01 (mesa): KTD central, heterocromia, tatuagens, olhar direto para câmera, chiaroscuro âmbar — ALTA qualidade, mantém padrão.
- shot-02 (vela): KTD protegendo vela na janela com retrato familiar ao fundo — consistente com KTD.
- shot-04 (lanterna): KTD caminhando com lanterna em corredor doméstico — consistente.
- Conclusão: as 4 imagens da V1 são o melhor material disponível para a música 2. Usá-las no render V2 com áudio oficial proof-v2 e movimentos idênticos aos da revisão (push_in, pan_right, tilt_up, push_out).
- Áudios: música 1 = ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav (BPM 102); música 2 = ktd-second-single-six-names-rebuilt-soul-proof-v2.wav (BPM 96).

## Follow-up do usuário (2026-08-19, segunda solicitação)
O usuário enviou `/home/ubuntu/upload/1e81d8d0-9b6e-11f1-aa68-2f087827a151.mp4` pedindo para "fixar esse vídeo como referência de desenvolvimento dos materiais mp4". Análise técnica: 8,000 s, 720x1280, h264/yuv420p, 24 fps, AAV, SHA-256 0b5d4f2b996c96c17d92b0c718ec4c14f241e795587f7bcf9eb47c5720aba21a — IDÊNTICO ao `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4` e à cópia promocional já no repo. Análise visual (manus-analyze-video) confirma: rapper performando em corredor industrial/prisional com olhos azuis brilhantes e cena final de rua chuvosa — é o clipe GOLDEN SCARS aprovado. Ação: vídeo já está no lugar correto como cânone; não foi regravado nem movido (adicionar duplicata seria redundância). Atualizei `docs/ktd-asset-catalog.md` com nova seção "Vídeo — referência oficial fixa de desenvolvimento" fixando formalmente esse arquivo como padrão obrigatório de todos os MP4. Pendente: comitar edição do catálogo + push seguro, e reportar ao usuário.

## Produção do clipe completo UNLEASH THE DRAGON (2026-08-19, terceira solicitação)
- Roteiro completo: docs/unleash-the-dragon-full-music-video-script.md (150,000 s, 102 BPM, beat 0,588 s, blocos A1-F2).
- Áudio oficial: assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav (exatamente 150,000 s).
- Keyframes geradas (todas 1440x2560, assets/video/references/lyrics/):
  1. song1-fullmv-scene-a1-dressing-room.png (KTD amarrando tênis no camarote, espelho com luzes e 7 garras a giz) — EXCELENTE
  2. song1-fullmv-scene-a2-backstage-wall.png (mão na parede do bastidor com pôsteres) — EXCELENTE
  3. song1-fullmv-scene-b1-pick-grip.png (mão com palheta sobre violão, amplificador ao fundo) — EXCELENTE
  4. song1-fullmv-scene-c1-back-shot.png (KTD de costas sob spotlight, dragão nas costas) — EXCELENTE
  5. song1-fullmv-scene-c2-face-close.png (close do rosto com heterocromia) — EXCELENTE
  6. song1-fullmv-scene-d1-amp-work.png (KTD ajustando amplificador valvulado) — EXCELENTE
  7. song1-fullmv-scene-e1-stage-edge.png (KTD sentado na borda do palco, contemplativo) — EXCELENTE
  8. song1-fullmv-scene-e2-crowd-silhouettes.png (mãos da plateia em silhueta) — EXCELENTE
  9. song1-fullmv-scene-f2-solo-mic.png (microfone solitário sob spotlight, dragão vermelho ao fundo) — EXCELENTE
  10. song1-fullmv-scene-c3-hook-perf.png (performance com luzes em leque) — EXCELENTE
  11. song1-fullmv-scene-d2-family-arms.png (perfil de KTD, silhuetas ao fundo) — EXCELENTE
  12. song1-fullmv-scene-f1-final-perf.png (KTD de braços abertos na luz principal) — EXCELENTE
- Keyframes do teaser v1 reutilizáveis (docs do roteiro: A1..F2 usa as 12 novas + as 5 do teaser: door-to-stage, shoes-cables, mic-grip, stage-lights, ktd-performance).
- Próximo passo: criar scripts/render_ktd_full_video.py (adaptar render_ktd_six_names_hybrid.py; grade por BPM, fade final a preto no bloco F2), renderar, muxar, verificar 150,000 s, comitar e entregar. Output planejado: assets/video/promos/unleash-the-dragon-full-music-video-v1.mp4 + doc de revisão.

## Tarefa atual (2026-08-19 ~19:45): clipe 1 real v2 = 10 s com trecho mais inspirador do áudio
- Áudio de trabalho: assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav (150 s, 102 BPM; NÃO é o definitivo — faixa sem áudio aprovado; mux = preview técnico pendente de aprovação).
- Janela escolhida (RMS máx + hook mais inspirador): 28,500–38,500 s ("A hard truth rising when the soft words die... Kairos on the pulse... Every scar is a charge, every bar is a bid"). Alternativas: 60–70 s (double-time) e 135–150 s (fecho). Doc: docs/unleash-the-dragon-clip1-10s-audio-segment.md.
- Clipe existente 8s: assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4 (camarote, já comitado, commit c53643b).
- Plano: gerar NOVO clipe de 10 s (gemini-omni-flash-preview, portrait, 720p, 10 s, sem áudio, first frame = assets/video/references/lyrics/song1-fullmv-scene-a1-dressing-room.png) com nome assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s.mp4, muxar trecho 28,5–38,5 s com fade-out 0,5 s via ffmpeg, verificar ffprobe, comitar (adição segura), entregar.
- ATENÇÃO: limite diário de geração de vídeo do plano gratuito = 1/dia. Hoje já foi usado 1 (o de 8 s). Se o call falhar por limite, relatar ao usuário.
- Repositório remoto atualizado: últimos commits c53643b (clipe real 1), be26b72 (plano v2), 72da101 (aprovações áudios), ae2bb1d (clipe slides v1). Nunca force-push; pull --ff-only antes de commit.
