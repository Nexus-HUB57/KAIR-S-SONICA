# Mix boom bap com a voz oficial de KTD

## Identificação

O mix principal é `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.wav`, com distribuição em `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.mp3`. A variação alternativa é `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.wav`, com distribuição em `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.mp3`.

Ambas as versões usam exclusivamente a referência vocal oficial `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3` e a base boom bap `assets/audio/ktd-boom-bap-trial-route-2-bed-v2.wav`. A tomada rejeitada `assets/audio/ktd-vocal-rough-take-v2.wav` não participa de nenhum dos dois renders.

## Parâmetros comuns

| Elemento | Valor exato |
| --- | --- |
| Base | `ktd-boom-bap-trial-route-2-bed-v2.wav` |
| Direção | American old-school swung boom bap |
| Andamento da base | 98 BPM |
| Tonalidade de direção | D minor |
| Duração processada | 137,7175 s |
| Taxa de amostragem de saída | 44.100 Hz |
| Canais de saída | 2, estéreo |
| Ganho da base antes da soma | `volume=0.58` |
| Alinhamento da base | `atrim=duration=137.7175`, loop de entrada até cobrir a voz |
| Voz de entrada | `kairos-rapid-rap-flow-demo-en-v3.mp3` |
| Equalização vocal passa-altas | `highpass=f=65` — corte em 65 Hz |
| Equalização vocal passa-baixas | `lowpass=f=12500` — corte em 12.500 Hz |
| Soma de sinais | `amix=inputs=2:duration=first:normalize=0` |
| Loudness final | `loudnorm=I=-14:TP=-1.0:LRA=7` |
| Limitador final | `alimiter=limit=0.95` |
| Master WAV | PCM signed 16-bit, 44,1 kHz, estéreo |
| Distribuição MP3 | LAME, 320 kbps, 44,1 kHz, estéreo |

## Mix principal — compressão vocal original

A cadeia vocal exata do mix principal é:

```text
highpass=f=65,
lowpass=f=12500,
acompressor=threshold=-19dB:ratio=2.2:attack=8:release=90:makeup=1.08,
volume=1.08
```

O compressor é descendente, com limiar de **−19 dB**, razão **2,2:1**, ataque de **8 ms**, release de **90 ms** e makeup linear de **1,08**. Depois da compressão, o vocal é somado ao beat com `normalize=0`; o bus final recebe loudness normalizado para **−14 LUFS**, true peak de **−1,0 dB** e limiter de segurança em **0,95**.

## Variação alternativa — saturação e compressão paralela

A variação mantém a equalização, a base, o loudness e o limiter do mix principal, mas divide a voz em dois caminhos depois dos filtros de 65 Hz e 12.500 Hz.

| Caminho | Parâmetros exatos |
| --- | --- |
| Vocal principal | `acompressor=threshold=-19dB:ratio=2.2:attack=8:release=90:makeup=1.08` |
| Saturação do vocal principal | `asoftclip=type=tanh:threshold=0.82:output=1.02:param=1.15:oversample=4` |
| Ganho do vocal principal | `volume=1.08` |
| Vocal paralelo | `acompressor=threshold=-32dB:ratio=8:attack=3:release=120:makeup=1.5` |
| Ganho do vocal paralelo | `volume=0.32` |
| Proporção de soma vocal | `amix=inputs=2:duration=first:weights='1 0.35':normalize=0` |
| Master final | `loudnorm=I=-14:TP=-1.0:LRA=7`, seguido de `alimiter=limit=0.95` |

A saturação usa soft clip **tanh**, threshold **0,82**, output **1,02**, parâmetro **1,15** e oversampling **4x**. A compressão paralela usa limiar **−32 dB**, razão **8:1**, ataque de **3 ms**, release de **120 ms**, makeup **1,5**, ganho de caminho **0,32** e peso de soma **0,35** em relação ao vocal principal. O objetivo é adicionar densidade e presença sem substituir a referência oficial nem descaracterizar sua articulação.

## Status e aprovação

As duas versões são **candidatas pendentes de aprovação humana**. O processamento está fixado e reproduzível, mas a promoção para faixa oficial depende de escuta crítica do equilíbrio entre vocal, kick, snare, baixo, swing, saturação, inteligibilidade e autenticidade de KTD.

A referência oficial continua sendo apenas `kairos-rapid-rap-flow-demo-en-v3.mp3`. A existência da variação saturada não altera a decisão de que `ktd-vocal-rough-take-v2.wav` é rejeitada e não deve ser reutilizada.
