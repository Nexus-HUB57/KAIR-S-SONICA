# Turnê inicial — desenvolvimento de vídeos curtos

## Estado do pacote

Este documento inicia o pacote de divulgação audiovisual da turnê inicial. A direção visual parte do ativo existente `assets/video/promos/golden-scars-v1-frame-the-whole-picture.mp4` e do frame de referência `assets/video/promos/tour/initial-tour-01-reference.png`. A primeira geração de vídeo foi solicitada em formato vertical, mas a cota diária disponível para geração de vídeo foi atingida; o arquivo MP4 final ainda não foi produzido nesta sessão.

## Direção criativa

A campanha deve apresentar o projeto como uma experiência noturna, física e íntima: palco vazio, silhueta de performer, fumaça, luz âmbar cortando o escuro e reflexos azul-cobalto. O visual deve parecer editorial e musical, com grão analógico controlado, contraste alto e movimentos de câmera lentos. A área inferior deve permanecer limpa para inserção posterior de cidade, data, local e chamada para ingressos.

## Pacote inicial planejado

| Peça | Formato | Duração | Função | Estado |
|---|---|---:|---|---|
| Teaser 01 — Golden Scars / Frame the Whole Picture | 9:16 | 8s | Revelação atmosférica do palco e da silhueta | Frame de referência pronto; vídeo pendente de geração |
| Teaser 02 — Six Names / Signal in the Dark | 9:16 | 8s | Corte rítmico com cabos, luz e equipamento | Roteiro pendente |
| Teaser 03 — Fire in the Flood / Arrival | 9:16 | 8s | Chamada emocional para a chegada da turnê | Roteiro pendente |
| Adaptador horizontal | 16:9 | 8s | YouTube, telas e imprensa | Derivar após aprovação do teaser vertical |
| Adaptador quadrado | 1:1 | 8s | Feed e anúncios | Derivar após aprovação do teaser vertical |

## Shot list do Teaser 01

**0,0–2,0 s — vazio:** palco escuro, cabos e ferragens quase indistintos; uma pequena luz âmbar começa a atravessar a fumaça.

**2,0–5,5 s — aproximação:** câmera avança lentamente em direção à silhueta central; reflexos azul-cobalto aparecem no chão molhado e no equipamento lateral.

**5,5–7,2 s — pulso:** um único pulso de luz revela a profundidade do palco sem mostrar um rosto identificável; a fumaça reage ao pulso.

**7,2–8,0 s — respiro:** imagem desacelera e termina em quadro escuro, preservando espaço para título e datas editáveis.

## Texto de pós-produção

A geração visual deve permanecer sem texto, logotipos ou marcas d’água. Depois da aprovação do vídeo, inserir em camada editorial separada: `KAIR-S-SONICA`, nome da cidade, data, local, URL de ingressos e classificação etária quando aplicável. A edição de texto deve ser feita sobre uma cópia de distribuição, preservando o render limpo.

## Critérios de aprovação

O vídeo deve ter 8 segundos, proporção 9:16, 720p, movimento suave, silhueta não identificável, paleta preta/âmbar/azul-cobalto, ausência de texto gerado pelo modelo e área inferior utilizável. A versão aprovada deverá ser validada com `ffprobe` e receber hash SHA-256 antes de ser adicionada ao catálogo.

## Próxima ação

Quando a cota de vídeo estiver disponível novamente, gerar o Teaser 01 usando `initial-tour-01-reference.png` como referência. Em seguida, revisar o movimento, validar o MP4 e criar Teasers 02 e 03 mantendo o mesmo frame language, sem substituir o ativo existente de GOLDEN SCARS.
