# SIX NAMES (Rebuilt Soul) — pack de produção do clipe de 10 segundos

Este documento consolida o roteiro visual completo e as instruções exatas de prompt para a geração do clipe real de 10 segundos da música 2, em conformidade com o cânone aprovado (`assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4`) e com a auditoria oficial do mapa de tatuagens de KTD (`docs/ktd-chest-tattoo-official-map-audit.md`). Autor: Manus AI. Data: 2026-08-20.

## 1. Verificação da keyframe no repositório

A keyframe da cena foi verificada no working tree e confirmada localmente (não versionada até o comit, por regra de comitar somente após aprovação humana). O arquivo `assets/video/references/lyrics/song2-six-names-table-candles-v2.png` possui hash SHA-256 `f4a58db3fa55...ffee6`, dimensões 1440x2560 (9:16) e foi inspecionado em recortes de rosto, peito e composição geral. A verificação confirmou os elementos oficiais: sete garras com pontas de diamante descendo verticalmente do esterno, coluna de escamas simétrica pela linha do abdômen até a cabeça do dragão junto ao umbigo, samurai de armadura no braço esquerdo, koi no braço direito e flores de cerejeira integradas, **sem barras horizontais de garra** (a divergência reprovada na geração da música 1). A cena mostra KTD à cabeceira de uma mesa de madeira com seis lugares vazios, seis pratos e seis velas acesas, com um porta-velas central apagado nas mãos — composição aprovada em workflow, derivada do plano da mesa do teaser v2.

| Item | Valor verificado |
| --- | --- |
| Arquivo | `assets/video/references/lyrics/song2-six-names-table-candles-v2.png` |
| Hash SHA-256 (prefixo) | `f4a58db3fa55...ffee6` |
| Dimensões | 1440x2560 (9:16) |
| Mapa de tatuagens | Conforme master oficial (auditoria aprovada) |
| Cena | Mesa familiar com seis lugares, velas acesas, vela central apagada |
| Status | Gerada, verificada, pendente de comit pós-aprovação |

## 2. Roteiro visual completo (10 segundos)

A cena é contínua e realista, sem cortes (single take), seguindo o padrão do cânone: câmera steadicam com dolly-in lento, chiaroscuro com pretos densos, paleta restrita de carvão, âmbar e laranja queimado, sem texto sobreposto. A narrativa encaixa literalmente no refrão "six flames in one heart": KTD acende as velas dos seis lugares vazios, reunindo simbolicamente os seis nomes da família.

| Tempo | Ação visual (movimento físico contínuo) |
| --- | --- |
| 0,0–2,0 s | KTD acende a vela central com um fósforo; a chama cresce suavemente; dolly-in lento da câmera |
| 2,0–6,0 s | Estende a chama e reacende as velas menores uma a uma, com movimentos lentos e naturais das mãos; reflexos quentes nos pratos escuros e na madeira polida |
| 6,0–8,5 s | Volta à posição inicial, junta as mãos sobre a mesa, respira; as chamas tremulam organicamente e uma fumaça sutil sobe |
| 8,5–10,0 s | Ergue a cabeça lentamente e fixa o olhar diretamente na câmera com dignidade silenciosa; reflexo das chamas nos olhos heterocromáticos |

## 3. Instruções de prompt para a geração de vídeo

O prompt a seguir é o **texto final aprovado para a chamada de geração** e deve ser usado sem alterações, com a keyframe `song2-six-names-table-candles-v2.png` como primeiro frame.

> Photorealistic cinematic music video shot in a dark family dining room at night, lit only by warm candlelight. A muscular Black man with a shaved head, long full dark beard, heterochromia eyes (left honey-amber, right pale blue), shirtless with an immutable tattoo map on his chest: seven diamond-tipped claw marks arranged vertically down the upper chest from the sternum, a symmetrical serpent dragon-scale column running down the center of his abdomen ending in a dragon head at the navel, samurai armor tattoo on his left arm, koi fish on his right arm, cherry blossoms integrated. He sits at the head of a long wooden dining table set with six empty places, six plates and six lit candles, symbolizing the six names of his family. In ten continuous seconds: he lights the unlit central candle with a match, the flame growing softly; then he reaches out and gently re-ignites the other small candles one by one with slow, natural finger movements; the warm candlelight flickers organically, reflections shimmering on the dark plates and polished wood; subtle smoke rises; his chest rises with each breath. Camera performs a slow, smooth, steady steadicam dolly-in toward his face. He finishes by slowly raising his head and staring directly into the camera with quiet dignity, a faint flame reflection in his mismatched eyes. Chiaroscuro lighting with dense blacks, restricted palette of charcoal, amber and burnt orange. No text, no logos, no watermarks. Continuous realistic physical motion, never a static-image pan or zoom.

**Parâmetros técnicos da chamada** (modelo Gemini Omni Flash Preview, única geração permitida por dia): aspecto `portrait`, resolução `720p`, duração `10` segundos, áudio desativado, keyframe inicial fornecida como `first frame`. O modelo aceita 3–10 segundos em incrementos de 1 segundo em 720p, portanto os 10 segundos estão dentro das capacidades documentadas.

**Regra de regeneração**: se a IA introduzir qualquer divergência do mapa de tatuagens (barras horizontais, número de garras diferente) ou perder continuidade (movimento estático estilo Ken Burns), a geração deve ser refeita no próximo reset do limite diário, sem muxagem, até a aprovação humana da keyframe e do clipe.

## 4. Muxagem aprovada

A muxagem usa o trecho **60,0–70,0 s** da master definitiva `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` (165,198 s, 96 BPM) — o pico de energia RMS da faixa (0,244, maior janela de 10 s) e o refrão literal: *"Every winter, now we light the dark. If I rise, we rise, let the whole block know... Six inches in my chest, six flames in one heart."* A operação é feita com ffmpeg: extração da janela com fade-in de 0,3 s e fade-out de 0,5 s, vídeo reencodado para 720x1280 @24fps H264 CRF18, áudio AAC 192k, duração final exata de 10,000 s. Saídas: `assets/video/promos/six-names-ktd-clip-table-candles-10s.mp4` (mídia) e `...-with-audio.mp4` (mux definitivo). Comando completo:

```bash
ffmpeg -y -v error -i assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav \
  -i assets/video/promos/six-names-ktd-clip-table-candles-10s.mp4 \
  -filter_complex "[0:a]atrim=start=60:end=70,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,afade=t=out:st=9.5:d=0.5[fa];[1:v]fps=24,scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2[v]" \
  -map "[v]" -map "[fa]" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -t 10.000 assets/video/promos/six-names-ktd-clip-table-candles-10s-with-audio.mp4
```

## 5. Critérios de aprovação do clipe gerado

O clipe só é muxado e comitado após a revisão humana confirmar: movimento físico contínuo e natural (respiração, mãos, chamas) em todos os 10 s; dolly-in estável sem cortes; mapa de tatuagens do peito fiel à master oficial; olhos heterocromáticos e barba longa preservados; paleta carvão/âmbar/laranja queimado sem introdução de cores estranhas; zero texto, logo ou marca d'água; zero elementos de UNLEASH THE DRAGON ou GOLDEN SCARS (palco, microfone vintage, corredor industrial); e sincronia de mood com o refrão selecionado.
