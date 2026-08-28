# Autoridade de referências e resolução de heterocromia — KTD-A/V v1.0

**Código:** KTD-AV-REF-001  
**Status:** norma operacional; lateralidade da heterocromia ratificada pela ficha oficial  
**Aplicação:** toda imagem, vídeo, capa, thumbnail, avatar, storyboard, prompt, render e material promocional de KTD

## 1. Decisão de autoridade

A identidade visual de KTD deve ser verificada pela seguinte ordem de precedência:

| Nível | Referência | Função |
|---|---|---|
| 1 | Imagem-mestre aprovada, retrato aprovado e `ktd-physical-turnaround-sheet.png` | Verdade visual e anatômica do personagem |
| 2 | Manifesto e documentos de persona | Vocabulário, narrativa, atributos e restrições |
| 3 | Prompts, briefs, scripts e descrições de produção | Instrução operacional derivada; nunca fonte superior |

Quando texto e imagem divergirem, a divergência bloqueia a promoção do ativo. A imagem não deve ser “interpretada” pela posição do observador: esquerda e direita devem sempre ser descritas **do ponto de vista anatômico de KTD**.

## 2. Resolução da heterocromia (Ratificado)

Com base na ficha visual oficial `ktd-physical-turnaround-sheet.webp`, a lateralidade anatômica está fixada:
- **Olho Anatômico Esquerdo:** Honey-amber (Mel/Âmbar)
- **Olho Anatômico Direito:** Pale clear-blue (Azul-claro pálido)

Esta definição prevalece sobre qualquer descrição textual anterior. A orientação deve ser sempre anatômica (do ponto de vista do sujeito). Toda geração ou tratamento de imagem que inverta esta ordem será sumariamente rejeitada.

## 3. Detalhes imutáveis após ratificação

Os seguintes atributos são anchors de continuidade e não podem variar sem uma nova decisão humana de canon:

| Domínio | Detalhes fixos |
|---|---|
| Corpo | Homem negro adulto ficcional; cabeça raspada; barba preta longa e cheia; biotipo compacto e atlético; 188 cm e 100 kg como referência técnica |
| Olhos | Heterocromia natural; lado anatômico e cor final conforme decision record ratificado; sem neon, uniformização, troca de lado ou olhos artificiais |
| Sobrancelhas | Dois riscos dourados discretos na posição visual aprovada; não dividir, duplicar ou inventar riscos |
| Tatuagens | Sete garras verticais no esterno/peito; continuidade do Dragão Diamante; braço esquerdo com carpas, ondas e cerejeiras; braço direito com samurai, armadura e nuvens orientais |
| Voz | `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3` como única âncora vocal oficial; rough take rejeitada permanece fora de geração e aprovação |
| Música | Rap em inglês; boom bap/old school com swing humano, kick seco, snare com ataque, baixo encorpado e vocal frontal |
| Autoridade | KTD decide identidade, interpretação e aprovação; Káiros orquestra plano, ritmo, DSP, mix, master, observabilidade e entrega |

## 4. Referências oficiais sincronizadas

A fonte visual oficial é `assets/persona/ktd-physical-turnaround-sheet.png`, em conjunto com `assets/persona/ktd-visual-master.png` e `assets/persona/artista-principal-diamante.png`. A fonte de autoridade de persona é o diretório `personas/artist-principal`, enquanto `personas/kairos` define a orquestração técnica.

A fonte oficial de catálogo de áudio é `assets/audio/albums/ktd-first-album/masters`, contendo os masters numerados do álbum. A pasta não substitui a âncora vocal oficial, que permanece separada em `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`. Provas, trials, rough takes e arquivos históricos não podem ser tratados como masters ou referências de identidade.

## 5. Gate de identidade para produção audiovisual

Antes de qualquer render, o brief deve declarar a referência visual, a orientação anatômica, o status da heterocromia, o canal, a duração, a proporção e o objetivo. Depois do render, cada plano deve passar por revisão quadro a quadro. O revisor deve conferir olhos, barba, cabeça, pele, tatuagens, figurino, escala, direção espacial e continuidade corporal.

O plano é `REJECTED` se a heterocromia trocar de lado, desaparecer ou receber efeito artificial; se a tatuagem mutar, sumir, inverter ou mudar de lateralidade; se KTD virar um homem genérico; ou se o movimento for apenas pan, zoom, Ken Burns ou interpolação sobre still.

O plano é `READY_FOR_APPROVAL` somente quando também demonstra ação corporal real, microexpressões, respiração, transferência de peso, câmera motivada, reação temporal do cenário, sincronismo e formato compatível com o canal. `APPROVED` e `RELEASED` exigem decisão humana para a versão e o uso exatos.

## 6. Controle de mudança

Qualquer alteração nos anchors exige novo decision record, atualização do manifest, incremento de versão do padrão e revalidação dos ativos derivados. Uma correção cosmética não pode reabrir um ativo reprovado por falha de identidade ou movimento.

## Referências

- [Turnaround sheet oficial](https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/assets/persona/ktd-physical-turnaround-sheet.png)
- [Personas oficiais](https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/personas)
- [Masters oficiais do primeiro álbum](https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/assets/audio/albums/ktd-first-album/masters)
- [Protocolo PHD de produção audiovisual](../ktd-phd-audiovisual-production-protocol-v1.md)
