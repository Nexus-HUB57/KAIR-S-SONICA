# No One Saved Me a Seat — fusão harmônica do refrão v4

**Artista:** KTD / Kháirus the Dragon  
**Single:** 7  
**Status:** candidato para aprovação auditiva  
**Escopo:** corrigir a percepção de corte na entrada do refrão sem regenerar a faixa.

## Correção aplicada

A montagem anterior fazia a entrada do ciclo gospel v4 por concatenação direta. Como a última frase do pré-refrão v1 tem maior densidade e o início do v4 abre com lead mais espaçado, a transição soava como uma queda.

A nova versão usa os mesmos arquivos de origem e cria uma **fusão harmônica de um compasso**, equivalente a `2,352941 s` em 102 BPM. Em cada troca, a cauda da seção anterior e a abertura da seção seguinte são sobrepostas com curva equal-power; o elemento que sai diminui progressivamente enquanto o elemento que entra cresce. O áudio do refrão v4 mantém o ciclo completo `00:00,00–00:48,60` e recebe somente um ajuste de presença de aproximadamente +2 dB para evitar perda de inspiração na entrada.

> Não houve nova geração musical, reescrita de letra, alteração de versos, mudança da batida, remix da faixa inteira ou normalização global.

## Regiões de transição

| Transição | Material que sai | Material que entra | Tratamento |
|---|---|---|---|
| Refrão 1 | Cauda do pré-refrão v1 | Abertura do ciclo v4 | Overlap harmônico de 1 compasso |
| Refrão 1 → seção seguinte | Saída do ciclo v4 | Cabeça do trecho v1 seguinte | Overlap harmônico de 1 compasso |
| Refrão 2 | Cauda do trecho v1 anterior | Abertura do ciclo v4 | Overlap harmônico de 1 compasso |
| Refrão 2 → ponte | Saída do ciclo v4 | Cabeça da ponte v1 | Overlap harmônico de 1 compasso |
| Refrão final | Cauda da ponte v1 | Abertura do ciclo v4 | Overlap harmônico de 1 compasso |
| Refrão final → outro | Saída do ciclo v4 | Outro v1 | Crossfade curto de segurança |

As regiões centrais dos versos, da ponte e do outro foram mantidas como segmentos da faixa-base e não foram regeneradas.

## Validação técnica

| Item | Resultado |
|---|---|
| Duração WAV | 249,571 s — aproximadamente 4min10s |
| WAV | PCM 24-bit, 44,1 kHz, estéreo |
| MP3 | 320 kbps, 44,1 kHz, estéreo |
| Loudness medido | −12,8 LUFS integrado |
| Pico verdadeiro medido | +0,2 dBTP antes de qualquer normalização hipotética |
| Normalização global | Não aplicada |
| Fonte v1 original | Preservada sem sobrescrita |
| Refrão v4 | Ciclo completo usado nos três pontos |

Os valores de loudness e pico são medições do arquivo; não foi aplicada normalização adicional para produzir a versão.

## Masters

| Arquivo | SHA-256 |
|---|---|
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-harmonic-fusion-master.wav` | `7176da075ab1b46ebfc4794afa4202fbdcf24de1cd3a5648dc41373aa09bf6ce` |
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-harmonic-fusion-master.mp3` | `0b5acd75186fc1028f2f473b469d28f1dde9d63e97b8d788874cf2b47fc120db` |

A versão deve ser considerada **candidata até a audição do usuário**, especialmente no trecho de entrada em torno de `01:02`.
