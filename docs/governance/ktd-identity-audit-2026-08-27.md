# Auditoria de identidade KTD — 2026-08-27
Gatilho: capa do Single 1 reprovada pelo titular ("não é KTD e não são as tatuagens dele").

## Achado 0 — CONTRADIÇÃO NA PRÓPRIA DOCUMENTAÇÃO (crítico)
- Texto (bíblia visual + physical spec + manifest): olho ESQUERDO mel/âmbar, DIREITO azul-claro.
- Imagem-mestre e retrato aprovado (assets/persona): o audit visual mostra o olho DIREITO do sujeito em mel/âmbar e o ESQUERDO em azul — o contrário do texto.
- A geração reprovada seguiu o texto; o titular valida a IMAGEM.
- DECISÃO PENDENTE DO TITULAR: qual é a verdade? Recomendação: a imagem aprovada vira a autoridade e o texto é corrigido.

## Divergências da capa reprovada (gerada vs. referências aprovadas)
1. Heterocromia invertida em relação às imagens aprovadas.
2. Riscos dourados: geração pôs um em cada sobrancelha; aprovado = dois na sobrancelha direita do sujeito.
3. Cicatriz inventada acima do olho esquerdo (não existe no master).
4. Peito: geração fez 4 arranhões finos diagonais tipo cicatriz fresca no lado esquerdo; aprovado = sete garras verticais grandes e pesadas, preto carvão com fios dourados, descendo do esterno como entrada do dragão de sete cabeças.
5. Mangas: geração fez floral solto e pouco denso; aprovado = mangas fechadas black-and-gray densas (esq. carpas/ondas/cerejeiras; dir. samurai/armadura/nuvens), quase sem pele nua.

## Regra de correção (a partir desta auditoria)
- A fonte de verdade é a TRÍADE VISUAL: ktd-visual-master.png + retrato aprovado + turnaround sheet — nunca o texto isolado.
- Todo prompt de geração deve descrever a identidade a partir da tríade e proibir explicitamente: inverter heterocromia, dividir os riscos entre as sobrancelhas, adicionar cicatrizes, transformar as garras em arranhões/cicatrizes, afrouxar a densidade das mangas.
- Gate de identidade obrigatório após cada imagem, comparando com a tríade (não com o texto).
- Capa do Single 1: status REPROVADA — regenerar somente após decisão do titular sobre a heterocromia.

## Custo desta sessão
1 imagem gerada (reprovada) + auditoria. Nenhuma outra geração será feita até a decisão do titular.


## DECISÃO DO TITULAR (2026-08-29)
Heterocromia oficial = IMAGENS aprovadas: olho DIREITO de KTD é mel/âmbar, olho ESQUERDO é azul-claro. Documentação corrigida neste commit. A tríade visual é a autoridade final.
