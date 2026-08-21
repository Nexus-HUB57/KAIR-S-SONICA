# FIRE IN THE FLOOD — gate de fidelidade visual de KTD v1

## Regra de identidade

Cada plano deve representar o mesmo KTD original e fictício definido na bíblia visual. A variação permitida está na atuação, no enquadramento, na iluminação e no ambiente; **não** está no rosto, nos olhos, na anatomia, nas tatuagens ou na presença corporal.

> Se o espectador precisa perguntar se é KTD, o plano falha — mesmo que a fotografia e o lip-sync estejam bons.

## Checklist obrigatório antes da promoção

| Área | Conferência | Falha quando |
|---|---|---|
| Rosto | Mesma estrutura facial, cabeça raspada e barba longa/cheia | O rosto se transforma, rejuvenesce, envelhece ou assume outra pessoa |
| Olhos | Esquerdo âmbar/mel; direito azul-claro | As cores são trocadas, homogeneizadas ou perdem a heterocromia em close |
| Sobrancelhas | Dois riscos dourados discretos e alinhados | Os riscos desaparecem sem causa de enquadramento ou viram desenho diferente |
| Corpo | Homem negro adulto, atlético compacto, proporções estáveis | Mãos, braços, ombros, torso ou postura deformam entre quadros |
| Peito e abdômen | Sete garras verticais no esterno; coluna central de escamas terminando em cabeça de dragão no umbigo | Tatuagens viram letras, carpas, armadura digital, símbolos aleatórios ou quantidade diferente |
| Braço esquerdo | Sistema de carpas, ondas e cerejeiras | Elementos somem ou são substituídos por samurai/máscara |
| Braço direito | Samurai e máscara/armadura estilizada, com nuvens orientais | Elementos somem ou são substituídos por carpas |
| Pele e tinta | Tatuagens parecem tinta real sobre pele, com poros e relevo | A pele parece plástico ou a tattoo vira overlay brilhante/fantástico |
| Roupa | Guarda-roupa molhado, preto e funcional, coerente com a cena | A roupa muda sem transição, revela anatomia incoerente ou adiciona adereços não previstos |
| Performance | Boca e rosto mantêm a identidade durante o canto | Lip-sync cria boca, dentes ou mandíbula de outro personagem |
| Continuidade | Plano começa e termina com identidade estável | Face morph, flicker, olho mudando de cor ou tatuagem reconfigurada |

## Método de referência

Usar sempre uma referência portrait 9:16 aprovada e, quando disponível, um keyframe de performance com a mesma iluminação e roupa do plano. A referência guia identidade e continuidade; ela não deve ser inserida como quadro final, nem convertida em zoom ou slideshow.

O prompt de geração deve repetir as âncoras de identidade, exigir preservação do mapa imutável de tatuagens e proibir face morph, troca de olhos, anatomia instável, tatuagens inventadas, personagens adicionais e logos. Quando uma região do corpo não estiver visível, o prompt deve pedir apenas continuidade plausível, nunca completar a área com um desenho novo.

## Gate de revisão temporal

Revisar pelo menos o primeiro, o meio e o último segundo do plano. Conferir olhos, barba, mandíbula, boca, mãos e tatuagens nos três pontos. Em close, conferir a heterocromia e o formato do rosto; em plano médio ou aberto, conferir proporções, roupa e continuidade do sistema de tatuagens.

O plano deve ser rejeitado e regenerado se houver qualquer mudança de identidade, ainda que breve. Não corrigir uma geração defeituosa com still, congelamento, crop que esconda o defeito ou sobreposição gráfica; a solução é uma nova geração temporal com referência melhor.
