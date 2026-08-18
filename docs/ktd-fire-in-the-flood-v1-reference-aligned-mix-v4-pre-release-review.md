# FIRE IN THE FLOOD — revisão final de pré-lançamento v4

## Decisão do DJ Káiros

A mix v3 aprovada foi revisada como master de distribuição. O tratamento vocal, a melodia de fundo, o arranjo, a posição temporal, o groove, a afinação e a imagem estéreo foram preservados. O único ajuste aplicado foi um ganho global de **−0,9 dB**, destinado a aumentar a margem contra picos intersample e não a mudar o caráter da produção.

A comparação PCM confirmou que a v4 é a v3 com apenas ganho global alterado: mesma quantidade de frames e erro máximo de arredondamento de 1 amostra. Não houve time-stretch, pitch-shift, edição vocal, compressão adicional, equalização adicional, alteração de panorama ou mudança de dinâmica relativa.

## Comparação de loudness

As medições foram executadas com FFmpeg `loudnorm=I=-14:TP=-1.0:LRA=7:print_format=json` e `ebur128`.

| Métrica | v3 WAV | v3 MP3 | v4 WAV | v4 MP3 | Leitura técnica |
| --- | ---: | ---: | ---: | ---: | --- |
| Loudness integrado medido | −13,04 LUFS | −13,04 LUFS | −13,94 LUFS | −13,94 LUFS | A v4 reduz o nível em aproximadamente 0,90 dB |
| True peak de entrada | −0,53 dBTP | −0,49 dBTP | −1,43 dBTP | −1,29 dBTP | A v4 cria margem adicional para codificação e distribuição |
| LRA | 4,10 LU | 4,10 LU | 4,10 LU | 4,10 LU | A dinâmica relativa foi preservada |
| Duração | 168,000 s | 168,046 s | 168,000 s | 168,046 s | A diferença MP3 é atraso/enchimento do codec |
| Codec | PCM s16le | MP3 320 kbps | PCM s16le | MP3 320 kbps | Formatos adequados para master e escuta |
| Amostragem | 44.100 Hz | 44.100 Hz | 44.100 Hz | 44.100 Hz | Compatível com a cadeia atual |

O relatório de `loudnorm` estima a saída normalizada em aproximadamente **−13,91 LUFS**, **−1,00 dBTP** e **4,10 LU LRA** para ambas as entradas, sem necessidade de nova normalização dinâmica. A v4 está tecnicamente mais segura que a v3 para distribuição porque seu pico de entrada fica abaixo de −1 dBTP tanto no WAV quanto no MP3.

## Arquivos oficiais

| Arquivo | Estado |
| --- | --- |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | Master oficial WAV de distribuição |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | Master oficial MP3 de escuta/distribuição |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav` | Master anterior preservado para rollback/auditoria |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.mp3` | Master anterior preservado para comparação |

A v4 substitui a v3 como master oficial de distribuição. A v3 não é apagada e continua registrada como versão anterior aprovada.
