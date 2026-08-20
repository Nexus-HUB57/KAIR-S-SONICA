# Auditoria do mapa oficial de tatuagens do peito de KTD

## Referência oficial (fonte da verdade)

O mapa imutável de tatuagens está definido em dois ativos oficiais do repositório, que devem ser usados como referência prioritária em qualquer geração visual: `assets/persona/ktd-visual-master.png` (master visual) e `assets/persona/ktd-physical-turnaround-sheet.png` (ficha técnica de referência física, frente/costas/perfis). A descrição textual registrada no catálogo é: **Diamante seven-headed dragon, koi, cherry blossoms, samurai**.

## Mapa do peito (vista frontal, conforme a master visual)

| Elemento | Posição | Características |
| --- | --- | --- |
| Sete garras/garfas do dragão | Centro superior do peito | Sete garras com pontas de diamante, descendo do esterno em direção aos mamilos, com detalhes dourados — o elemento assinado do peito |
| Coluna de escamas do dragão | Centro do esterno até o umbigo | Escamas serpentinas simétricas que descem pela linha do abdômen, terminando na cabeça do dragão junto ao umbigo |
| Dragão Diamante (sete cabeças) | Costas inteiras | O dragão de sete cabeças cobre as costas (vista dorsal da ficha), NÃO o peito |
| Samurai com armadura | Braço e ombro esquerdos | Guerreiro samurai em armadura detalhada |
| Koi (carpa) | Braço direito | Carpa entre flores e ondas |
| Cherry blossoms | Espalhadas nos ombros e braços | Flores de cerejeira integrando o mapa |

## Divergência detectada no clipe real de 10 s (música 1)

Na geração `unleash-the-dragon-realgclip-01-dressing-room-10s.mp4`, o peito apresenta **três marcas horizontais longas** (traços de garra estilizados em barras), que NÃO correspondem ao mapa oficial: a master visual define sete garras com pontas em forma de diamante descendo em padrão vertical/obíquo do esterno, com coluna de escamas central terminando na cabeça do dragão no umbigo. Essa divergência foi introduzida pela IA de vídeo, que reimaginou as marcas como barras de garra.

## Correção obrigatória para futuras gerações

Todo prompt de vídeo ou imagem de KTD com o peito visível deve incluir a descrição literal: "seven diamond-tipped claw marks arranged vertically down the upper chest from the sternum, with a symmetrical dragon-scale spine column running down the center of the abdomen ending in a dragon head at the navel, samurai armor on the left arm and shoulder, koi on the right arm, cherry blossoms integrated, per the immutable tattoo map of assets/persona/ktd-visual-master.png". A `ktd-visual-master.png` deve ser enviada como imagem de referência junto à keyframe em cada geração de vídeo que mostre o peito de KTD.

## Aplicação no clipe da música 2

O roteiro de 10 s de SIX NAMES (Rebuilt Soul) deve gerar cenas cujo peito de KTD siga estritamente este mapa, com a master visual como referência de consistência, antes de qualquer comit ou muxagem.
