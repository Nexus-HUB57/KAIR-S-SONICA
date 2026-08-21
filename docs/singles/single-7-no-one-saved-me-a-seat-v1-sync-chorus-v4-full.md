# No One Saved Me a Seat — sincronização cirúrgica do refrão v4

**Artista:** KTD / Kháirus the Dragon  
**Single:** 7  
**Status:** candidato para aprovação auditiva  
**Escopo:** substituição exclusiva dos três refrões da faixa v1 pelo ciclo completo do refrão gospel v4.

> Nenhum verso, intro, pré-refrão, ponte, outro ou segmento instrumental fora dos refrões foi regenerado, reescrito, normalizado ou remixado.

## Arquivos de origem congelados

| Arquivo | Duração observada | Especificação | SHA-256 |
|---|---:|---|---|
| `upload/no-one-saved-me-a-seat-v1-master.mp3` | 182,439 s | MP3, 320 kbps, 44,1 kHz, estéreo | `42f210dbafc0118fdde0bdab765ca70d3599491a6c759cf77cd4bf7bbe6a867d` |
| `upload/no-one-saved-me-a-seat-chorus-v4-gospel-preview-ma.mp3` | 77,349 s | MP3, 320 kbps, 44,1 kHz, estéreo | `ac74ec3875d4716e5072652fa38bf0cbe587768f2c8c88bbf34f1fda323ad2d8` |

## Recorte utilizado do refrão v4

Por solicitação do usuário, foi utilizado o **ciclo gospel completo** do refrão v4, correspondente ao intervalo `00:00,00–00:48,60` da prévia. O restante da prévia — repetições posteriores e tag adicional — não foi inserido.

## Mapa de montagem

Os intervalos abaixo usam segundos relativos ao início de cada arquivo. As quatro regiões marcadas como preservadas foram comparadas após a mesma decodificação PCM e produziram hashes idênticos entre a fonte e a saída.

| Ordem | Fonte v1 | Tratamento | Saída sincronizada |
|---:|---:|---|---:|
| 1 | `00:00,00–01:02,36` | Preservado integralmente | `00:00,00–01:02,36` |
| 2 | `01:02,36–01:26,34` | Substituído por `v4 00:00,00–00:48,60` | `01:02,36–01:50,96` |
| 3 | `01:26,34–02:09,54` | Preservado integralmente | `01:50,96–02:34,16` |
| 4 | `02:09,54–02:32,94` | Substituído por `v4 00:00,00–00:48,60` | `02:34,16–03:22,76` |
| 5 | `02:32,94–02:47,76` | Preservado integralmente | `03:22,76–03:37,58` |
| 6 | `02:47,76–03:01,50` | Substituído por `v4 00:00,00–00:48,60` | `03:37,58–04:26,18` |
| 7 | `03:01,50–fim` | Preservado integralmente | `04:26,18–fim` |

A duração final observada é aproximadamente **267,092 s (4min27s)**. O aumento resulta exclusivamente da inserção do ciclo v4 completo nos três pontos de refrão.

## Validação de preservação

| Segmento preservado | Hash PCM da fonte | Hash PCM da saída | Resultado |
|---|---|---|---|
| S0 — antes do refrão 1 | `6a8686a8242d986a5c7f5f040093b489c6d531c42afb9d52508aea18a90a8d93` | igual | Aprovado |
| S2 — entre os refrões 1 e 2 | `685ae2a3549f952cab172d35ba20ec155128f70199f166e1cc335f11f0a376e7` | igual | Aprovado |
| S4 — ponte antes do refrão final | `f791baf4a49272852db12f82b1fa8e9f275ff3d88d782e0ea78e015b2bd80b0c` | igual | Aprovado |
| S6 — outro após o refrão final | `710663e4792d789255f02e7c81eed156d3d6add2019aaace8ac81daad960b975` | igual | Aprovado |

A medição do master final indicou **−12,8 LUFS integrado**, **+0,2 dBTP de pico verdadeiro** e **4,5 LU de loudness range**. Esses valores foram apenas medidos; nenhuma normalização ou limitação adicional foi aplicada.

## Masters

| Arquivo | Especificação | SHA-256 |
|---|---|---|
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-full-master.wav` | WAV PCM 24-bit, 44,1 kHz, estéreo | `535eae5e5020b752bad0e7ba38798dcbb381c53cd20da95cc28759c7d81a2ec` |
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-full-master.mp3` | MP3 320 kbps, 44,1 kHz, estéreo | `769f10526b3e112808b434b9eea6054c04892af7c9e862c306159f39e8b3da80` |

A versão v1 original permanece preservada e não foi sobrescrita. A sincronização deve ser considerada **candidata até a aprovação auditiva do usuário**.
