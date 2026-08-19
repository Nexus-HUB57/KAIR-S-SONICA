# UNLEASH THE DRAGON — plano de produção do clipe v2 (vídeo real contínuo)

## Contexto da reprovação

O v1 (slides de imagens estáticas com Ken Burns procedural) foi reprovado. O padrão exigido é o do cânone `golden-scars-v1-frame-the-whole-picture-approved.mp4`: **clipes de vídeo real**, com movimento físico contínuo (andar, braços, cabeça, paralaxe, sombras dinâmicas), câmera steadicam/dolly fluida, cortes secos de 1–2 s entre planos e reconstrução da geometria frame a frame. A prova de mixagem também foi reprovada (batidas fora de sincronia); até nova aprovação de mixagem, o clipe v2 será montado **sem muxagem obrigatória** ou com o áudio de trabalho apenas como referência identificada como não definitiva.

## Método

1. **Clipes gerados por IA de vídeo real** (gemini-omni-flash-preview, 8–10 s, 720p, portrait 9:16) a partir de cada keyframe existente (ou keyframe nova quando necessário), com prompt descrevendo movimento físico contínuo, câmera fluida e comportamento do sujeito KTD.
2. **Consistência do personagem**: todas as gerações usam a mesma keyframe do personagem como first frame, o que trava identidade (rosto, barba, heterocromia, tatuagens) e garante continuidade.
3. **Sequência do clipe**: 3 clipes de 8 s = 24 s, formato teaser/primeira versão do clipe, cobrindo o arco bastidor → palco → performance (primeiro trecho da faixa: intro + pre-hook + início do hook).
4. **Concatenação** com ffmpeg, cortes secos, output 720x1280 24fps H264/AAC (faststart), igual ao cânone.
5. **Áudio**: sem muxagem até aprovação da nova mixagem (a mixagem é responsabilidade humana/editorial conforme manifesto); o vídeo sem áudio ou com áudio placeholder identificado NÃO será muxado. Alternativa: entregar muxado com o áudio atual apenas se o usuário aprovar o mux, registrado no commit.

## Clipes planejados (24 s)

| Clipe | Keyframe (first frame) | Movimento descrito no prompt |
| --- | --- | --- |
| UTD-RV1-C01 | song1-fullmv-scene-a1-dressing-room.png | KTD amarrando o tênis, levanta o rosto lentamente e olha para a câmera; luzes do espelho tremulando; câmera dolly-in lenta |
| UTD-RV1-C02 | song1-unleash-the-dragon-door-to-stage.png | Porta de acesso ao palco abrindo; KTD atravessa o vão; luz quente do palco crescendo; steadicam acompanhando |
| UTD-RV1-C03 | song1-fullmv-scene-c3-hook-perf.png | Performance no palco: KTD rima no microfone, gesticula, luzes pulsando em sincronia, câmera orbitando lentamente |

## Saída

`assets/video/promos/unleash-the-dragon-full-music-video-v2.mp4` (24 s, 720x1280 @24fps) + doc de revisão + registro da reprovação.
