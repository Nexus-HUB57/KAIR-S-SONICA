# Álbum de lançamento — plano visual sem repetição

## Decisão editorial

As imagens usadas no vídeo aprovado da música 3, **GOLDEN SCARS**, ficam reservadas exclusivamente para essa faixa. Os vídeos das músicas 1 e 2 não devem reutilizar o sujeito, o corredor industrial, a porta metálica, a rua chuvosa, o brilho azul nos olhos, a silhueta central ou a gramática de planos do vídeo KTD aprovado.

A nova regra é que cada faixa deve ser reconhecida pela letra antes mesmo de qualquer texto de identificação. O vídeo deve traduzir objetos, espaços e ações presentes no texto da música, e não apenas repetir uma atmosfera sombria genérica.

## Música 1 — UNLEASH THE DRAGON

A letra trabalha transformação, portas trancadas, ferro, fogo convertido em propósito, cabos, palco, família e a passagem de uma cela simbólica para uma plataforma de performance. A referência visual criada para essa faixa usa uma mão abrindo uma porta pesada para um palco com luz vermelho-âmbar, tênis gastos, microfone e textura de metal.

O vídeo deve começar com o gesto da maçaneta, cortar para a porta cedendo, revelar o palco e acelerar com cabos, pedal, sola do tênis e luzes acendendo. O hook pode usar a resposta “Who are you? — KTD.” como cortes de presença, mas sem inserir texto gerado no vídeo. A paleta deve ser carvão, ferrugem, âmbar e vermelho queimado; não usar chuva, água, olhos azuis, corredor industrial ou porta de prisão como nos ativos da música 3.

## Música 2 — SIX NAMES

A letra trabalha seis nomes, seis pratos, uma casa que segurou a tempestade, a avó protegendo a vela, o aluguel, a comida compartilhada, seis luzes no escuro e a ascensão coletiva. A referência visual criada para essa faixa usa uma mesa doméstica com seis pratos, velas, uma mão protegendo a chama e uma sequência de pontos de luz conduzindo ao corredor da casa.

O vídeo deve começar em detalhe com a chama e a mão, abrir para os seis lugares à mesa, atravessar a casa em direção às seis luzes e finalizar com a mesa cheia de calor e espaço para a promessa coletiva. O movimento pode ser um travelling lento de mesa para corredor, com cortes rítmicos em objetos domésticos: prato, talher, vela, sapato de trabalho, porta da cozinha e mãos se encontrando. A paleta deve ser âmbar de vela, madeira escura, creme envelhecido e violeta suave; não usar performer, palco, porta metálica, rua molhada, chuva, água, olhos azuis ou estética industrial da música 3.

## Matriz de não repetição

| Elemento | Música 1 — Unleash the Dragon | Música 2 — Six Names | Música 3 — Golden Scars |
|---|---|---|---|
| Espaço | Bastidor / palco abrindo | Casa / cozinha / corredor doméstico | Corredor industrial / rua chuvosa |
| Ação central | Abrir a porta e entrar na performance | Reunir a casa ao redor de seis lugares | Enfrentar o ambiente hostil e avançar |
| Objeto-símbolo | Maçaneta, cabos, microfone, tênis | Seis pratos, vela, mesa, mãos | Cadeado, porta metálica, água, chuva |
| Paleta | Carvão, ferrugem, âmbar, vermelho | Âmbar de vela, madeira, creme, violeta | Cinza frio, preto, azul metálico |
| Presença humana | Mão, tênis, microfone; performer apenas em fragmentos | Mãos e memória familiar; sem performer | Sujeito central com presença física e olhar direto |
| Proibições | Sem chuva, olhos azuis ou corredor industrial | Sem palco, metal, água, chuva ou olhos azuis | Reservado; não reutilizar nos demais vídeos |

## Estado dos ativos

As referências de letra para as músicas 1 e 2 foram criadas em arquivos separados:

- `assets/video/references/lyrics/song1-unleash-the-dragon-lyrics-reference.png`
- `assets/video/references/lyrics/song2-six-names-lyrics-reference.png`

Essas imagens são referências de direção para futuros vídeos dinâmicos, não substitutos do vídeo final. A geração dos MP4 deve ser feita com movimento real — travelling, cortes, gesto e mudança de luz — e não como slideshow de imagens estáticas.

## Próxima produção

Quando a cota de geração de vídeo estiver disponível, produzir primeiro a música 1 com a sequência da porta abrindo para o palco e depois a música 2 com a casa dos seis lugares. Cada MP4 deve ser gerado separadamente, validado com `ffprobe`, comparado contra a matriz de não repetição e versionado em commit próprio.
