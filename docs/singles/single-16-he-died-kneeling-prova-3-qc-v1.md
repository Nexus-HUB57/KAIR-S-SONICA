# Single 16 — HE DIED KNEELING — Prova 3 QC v1

**Data:** 2026-08-29
**Status:** `TECHNICAL_TEST` — candidata à escuta humana após reprovação da Prova 2
**Objetivo da correção:** aumentar intensidade, raiva, sofrimento vocal, choro melódico no refrão, agressividade de bateria e impacto do grave, mantendo poesia, história e potencial de hook social.

## Artefatos e métricas

| Arquivo | Duração | Formato | Loudness | True peak | SHA-256 |
|---|---:|---|---:|---:|---|
| Render bruto | 170,971375 s | MP3 estéreo, 44,1 kHz, 192 kbps | −12,4 LUFS | +0,2 dBFS | `e3ec890a2edbe881c9c6d75ae4317cf786ac57636548a353295bbad26112195b` |
| Cópia gain-staged | 170,997551 s | MP3 estéreo, 44,1 kHz, 320 kbps | −13,9 LUFS | −1,2 dBFS | `0337b6fb754127d09fe632241f6511cd5546b0f8c54274b61cd061ca2d7720a6` |
| Hook vertical | 22,047347 s | MP3 estéreo, 44,1 kHz, 320 kbps | −13,2 LUFS | −1,3 dBFS | `e32eadc9fb3f7801bf3a381d30eceeee11efff99e0066ad10061886f20250f24` |

Os três arquivos decodificaram integralmente sem erro. O render bruto é preservado como origem, mas não é cópia de entrega por exceder 0 dBFS. A cópia gain-staged é a versão recomendada para escuta e avaliação. Ela continua sendo prova MP3; master WAV PCM, stems e masterização final permanecem pendentes.

## Diagnóstico narrativo da transcrição

A transcrição automática identifica refrão desde aproximadamente 00:04, com repetição da imagem de morrer sobre um joelho e manter dignidade. Também confirma Angel, a região proibida, a troca de armas por alianças, o anúncio respeitoso de saída, a ligação sobre o terno do padrinho, a praça, a chegada desarmada, a repetição de “cowards” e o fechamento “one knee, one ring, one love”.

A estrutura é mais comercial do que a Prova 2 porque o hook entra nos primeiros segundos e retorna diversas vezes. O texto continua poético e motivado pela tentativa de abandonar o crime. A violência permanece sem descrição gráfica detalhada, embora a transcrição registre a entrega direta do amigo e deve ser submetida à decisão editorial humana.

A transcrição não consegue comprovar sozinha **choro, ódio, timbre, aspereza, intenção ou intensidade vocal**. Esses critérios exigem escuta humana comparativa com a âncora vocal oficial. O novo prompt solicita rachaduras, respiração, soluços e refrão cantado com dor, mas a decisão final não pode ser inferida da especificação.

## Veredito de prova

| Gate | Resultado | Observação |
|---|---|---|
| Decodificação | **PASS** | Sem erro no render, cópia corrigida ou hook |
| True peak da cópia de avaliação | **PASS** | −1,2 dBFS na faixa; −1,3 dBFS no hook |
| Hook precoce | **PASS** | Entrada aproximada em 00:04–00:06 |
| História | **PASS** | Angel, saída, alianças, praça, traição e honra presentes |
| Intensidade vocal | **HUMAN REVIEW REQUIRED** | Transcrição não mede performance emocional |
| Choro no refrão | **HUMAN REVIEW REQUIRED** | Precisa ser julgado por audição direta |
| Grave violento e mix | **HUMAN REVIEW REQUIRED** | Métrica de loudness não substitui teste em fones, celular e mono |
| Aderência à letra v2 | **REVIEW REQUIRED** | A ferramenta gerou wording próprio; não é take linha a linha da letra editorial |
| Publicação | **BLOCKED** | Sem aprovação humana, master final, stems e pacote de direitos |

## Próximo gate

Ouvir a cópia gain-staged em fones, monitores, celular e mono. A pergunta decisiva é: **KTD parece realmente abalado, chorando e furioso, ou apenas está narrando a dor?** Se a resposta ainda for narração controlada, a Prova 3 deve ser reprovada e a próxima geração deve aumentar a quebra vocal e o contraste entre choro no hook e ataque no verso. Se a emoção estiver presente, a faixa pode avançar para edição vocal dirigida, mix/master e pacote de aprovação humana.
