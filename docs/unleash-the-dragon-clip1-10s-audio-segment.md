# UNLEASH THE DRAGON — escolha do trecho de 10 s mais inspirador para o clipe 1 v2

## Análise (2026-08-19)

A energia RMS foi calculada em janelas de 0,5 s sobre o áudio de trabalho `proof-v1.wav` (150 s, 102 BPM). O trecho de 10 s com maior energia média — correspondente ao primeiro hook da faixa, o momento de maior impacto vocal e instrumental — é **28,5 s → 38,5 s**. A transcrição desse trecho confirma o conteúdo mais inspirador da abertura:

> "A hard truth rising when the soft words die. I bring quick wit, split-second switch. Trip the rhythm, flip the script, never miss. Kairos on the pulse, I am locked in the grid. Every scar is a charge, every bar is a bid."

As janelas alternativas de maior energia foram **60,0–70,0 s** (segundo pico do verso com double-time) e o encerramento em **135–150 s** ("Cables in the wire, I am more than the test"). A janela 28,5–38,5 s foi escolhida por combinar o pico de energia com a mensagem declarativa do hook (a "verdade dura" que sobe quando as palavras suaves morrem), o alinhamento com a cena do camarote — o momento em que KTD amarra o tênis e ergue o olhar para a câmera — e a possibilidade de o clipe abrir com 2,5 s de buildup antes do drop (a janela inclui 28,5–31,0 s de transição da intro para o hook).

## Regra de muxagem

O trecho muxado no clipe de 10 s é o segmento **28,500–38,500 s** do `proof-v1.wav`, com fade-out suave nos últimos 0,5 s. Como o áudio da faixa permanece sem aprovação definitiva, o mux é identificado como **preview técnico**, pendente de aprovação editorial.

## Pipeline de muxagem validado (2026-08-19)

O script `scripts/mux_utd_clip_audio.py` foi criado e validado contra o clipe existente de 8 s, produzindo `/tmp/utd_mux_test.mp4` com saída exata de 8,000 s, 720x1280 @24fps, H264 CRF18 + AAC 192k, trecho do áudio 28,5–36,5 s com fade-in de 0,3 s e fade-out de 0,5 s. Para a versão de 10 s, a chamada será:

```
python3 scripts/mux_utd_clip_audio.py \
  assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s.mp4 \
  assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s.mp4 \
  28.5 10.0 0.5
```

(salvar saída com nome distinto, por exemplo `...-10s-with-audio.mp4`, e comitar após verificação.)
