# Single 16 — HE DIED KNEELING — Prova 4 QC v1

**Data:** 2026-08-29
**Status:** `TECHNICAL_TEST` — candidata à escuta humana; não aprovada
**Motivo da iteração:** Prova 3 rejeitada pelo titular por ainda não transmitir intensidade e dor suficientes na voz.

## O que foi alterado

A Prova 4 abandona a entrega vocal convencional e solicita uma performance em colapso: respiração quebrada desde o início, voz trêmula, falhas de frase, refrão como choro que vira grito, alternância entre quase-sussurro e explosão, e ponte com silêncio e “cowards” repetido. A batida recebeu hard boom bap, sub/808 mais agressivo, kick seco, snare pesada, piano sombrio e cordas tensas.

## Artefatos e métricas

| Função | Caminho | Duração | Formato | Loudness | True peak | SHA-256 |
|---|---|---:|---|---:|---:|---|
| Render bruto | `outputs/single_16/he-died-kneeling-prova-4-v4.mp3` | 166,817917 s | MP3 estéreo, 44,1 kHz, 192 kbps | −12,1 LUFS | +0,4 dBFS | `a03cf23b7020e8c4db4f1e5bb682d86fe20c448c95ade16b44d899e70ad994d3` |
| Cópia gain-staged | `outputs/single_16/he-died-kneeling-prova-4-v4-gainstaged.mp3` | 166,844082 s | MP3 estéreo, 44,1 kHz, 320 kbps | −13,6 LUFS | −1,2 dBFS | `36cc30b941ba6267545d1dc0f4d6b1705cf00952e113c3325b59ca8e762c5638` |
| Hook vertical | `outputs/single_16/he-died-kneeling-prova-4-v4-gainstaged-hook-22s.mp3` | 22,047347 s | MP3 estéreo, 44,1 kHz, 320 kbps | −13,1 LUFS | −1,3 dBFS | `6c61ded866d65518735f7e7567e2404f378f3f0f02f5f15cd14fec0395cbd08b` |

O render bruto decodificou integralmente, mas o pico de +0,4 dBFS impede seu uso como cópia de entrega. A versão gain-staged foi criada com redução de 1,5 dB e decodificou integralmente, com true peak de −1,2 dBFS. O áudio continua sendo uma prova MP3; não é master WAV nem possui stems.

## Diagnóstico da transcrição

A transcrição identifica o hook já em aproximadamente 00:03–00:07, com a pergunta “Why did they shoot when your hands were clean?”, a ligação sobre o terno do padrinho, Angel, a troca do aço por ouro, a praça, a chegada desarmada, “cowards” repetido e o fechamento sobre alianças substituindo armas. A estrutura ficou mais comercial e mais imediatamente dramática.

A transcrição sugere maior vulnerabilidade textual, mas não mede se a voz realmente chora ou se a intensidade chega à essência de KTD. A performance precisa ser julgada por escuta direta. Nenhuma métrica técnica, transcrição ou instrução de prompt substitui esse julgamento.

## Veredito

| Critério | Resultado | Observação |
|---|---|---|
| Hook precoce e comercial | **PASS** | Começa antes de 00:08 e retorna várias vezes |
| Preservação da história | **PASS** | Angel, saída, alianças, praça, traição e honra presentes |
| Agressividade da batida | **HUMAN REVIEW REQUIRED** | Requer teste em fones, celular e mono |
| Grave físico | **HUMAN REVIEW REQUIRED** | True peak seguro na cópia, mas impacto é subjetivo |
| Dor vocal | **HUMAN REVIEW REQUIRED** | O ponto principal desta iteração |
| Choro no refrão | **HUMAN REVIEW REQUIRED** | Não pode ser inferido pela transcrição |
| Integridade técnica | **PASS WITH NOTE** | Decodificação limpa; render bruto acima do pico permitido |
| Duração | **REVIEW REQUIRED** | 166,84 s, abaixo do alvo de 170–174 s |
| Aprovação | **BLOCKED** | Titular ainda não aprovou; master e stems pendentes |

## Gate decisivo

Ouvir primeiro a cópia gain-staged, especialmente o trecho 00:07–00:29 e a ponte 02:00–02:18. A pergunta é simples: **a voz parece realmente prestes a desabar, ou apenas está interpretando uma letra triste?** Se ainda parecer limpa, estável ou genérica, a próxima etapa não deve ser apenas mais grave: deve usar vocal dirigido ou gravação humana aprovada, porque a ferramenta automática não está garantindo a intensidade emocional solicitada.
