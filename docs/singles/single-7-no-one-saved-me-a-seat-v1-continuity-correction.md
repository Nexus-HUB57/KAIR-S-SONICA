# No One Saved Me a Seat — correção de continuidade do refrão v4

**Artista:** KTD / Kháirus the Dragon  
**Single:** 7  
**Status:** candidato para nova aprovação auditiva  
**Correção:** fusão do ciclo completo do refrão gospel v4 com a faixa-base v1.

## Problema corrigido

A montagem anterior fazia uma concatenação seca em `01:02,36`. Esse corte removia a cauda do pré-refrão no instante de maior impulso e fazia a abertura do refrão v4 — que começa com uma frase lead mais espaçada — parecer uma queda de força.

A nova versão não é uma nova geração musical. Ela usa os mesmos dois arquivos enviados pelo usuário e altera somente a integração nas bordas dos refrões.

## Método aplicado

Cada refrão v4 continua usando o ciclo completo `00:00,00–00:48,60` da prévia aprovada. Para evitar a queda, foram aplicadas as seguintes operações exclusivamente nas janelas de transição:

| Operação | Aplicação |
|---|---|
| Overlap musical | 1,5 s entre a cauda da v1 e a entrada do v4; e entre a saída do v4 e a seção seguinte |
| Fades complementares | A cauda da v1 desaparece progressivamente enquanto o v4 cresce, sem corte seco |
| Ganho do refrão v4 | +2 dB aproximadamente, somente nos segmentos do refrão |
| Limitação de segurança | Limitador apenas no áudio do refrão para evitar clipping durante a soma |
| Normalização global | Não aplicada |
| Regeneração da música | Não aplicada |
| Alteração dos versos e da batida | Não aplicada |

A montagem determinística por segmentos preserva a duração dos trechos e evita o encurtamento causado por uma cadeia de concatenações internas.

## Mapa temporal da correção

| Região | Tratamento |
|---|---|
| `00:00,00–01:00,86` | Faixa v1 preservada |
| `01:00,86–01:02,36` | Overlap da cauda do pré-refrão v1 com a abertura do v4 |
| `01:02,36–01:49,46` | Corpo do refrão v4 completo |
| `01:49,46–01:50,96` | Overlap da saída do v4 com a entrada da seção seguinte |
| `01:50,96–02:32,66` | Faixa v1 preservada, com as bordas de transição previstas |
| `02:32,66–03:21,26` | Segundo refrão v4 completo, com as mesmas transições |
| `03:21,26–03:36,08` | Ponte e segmentos da v1 preservados, com bordas de transição |
| `03:36,08–04:24,68` | Terceiro refrão v4 completo, com saída natural para o outro |
| `04:15,68–04:18,09` | Outro v1 preservado; a diferença em relação ao relógio ideal decorre da sobreposição das seis bordas de transição |

A duração medida do master WAV é **258,092 s**, aproximadamente **4min18s**. O valor decorre da substituição dos três refrões e da sobreposição das bordas, sem duplicação temporal. O mapa de segmentos do manifesto é a referência exata para os limites de áudio; timestamps exibidos por contêineres MP3 podem arredondar alguns milissegundos.

## Validação

Os corpos não envolvidos nas transições foram comparados após a mesma decodificação PCM:

| Região preservada | Hash da fonte | Hash da saída | Resultado |
|---|---|---|---|
| Antes do refrão 1 | `c5572027946f54634786dff1b40e55eb1933e341ae143555a8258e57446b3b2e` | igual | Aprovado |
| Corpo entre refrões 1 e 2 | `2cf9c640321913b1545e48af7479017ad195a39cc476bceefb5a20c2cb3b09e2` | igual | Aprovado |
| Corpo da ponte | `8cd135ac101d68613a470c4a6516397082ac4431746cf173a39cbca32263e92c` | igual | Aprovado |

A medição do master indicou **−11,8 LUFS integrado**, **+0,2 dBTP de pico verdadeiro** e **5,5 LU de loudness range**. Esses valores são somente medição; não foi aplicada normalização global.

## Arquivos finais

| Arquivo | Especificação | SHA-256 |
|---|---|---|
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-continuity-corrected-master.wav` | WAV PCM 24-bit, 44,1 kHz, estéreo | `e9405e5da0331765281a874fabf3ce9ca7f58837be64b55bd56b7304a8bfc2fa` |
| `outputs/single_7/no-one-saved-me-a-seat-v1-synced-chorus-v4-continuity-corrected-master.mp3` | MP3 320 kbps, 44,1 kHz, estéreo | `1e756f059320bf9a19d922dcd04fe780880f2558aba7a808c0197ae85482d215` |

A faixa-base v1 original e a versão anterior permanecem preservadas separadamente.
