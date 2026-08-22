# I WON'T WASTE THIS LIFE — especificação de geração para TikTok v1

**Artista:** KTD / Kháirus the Dragon
**Música:** Single 11 — Prova 2 Black Music Rap Old School
**Objetivo:** executar o storyboard vertical com fidelidade visual ao KTD e sincronizar o áudio real na pós-produção
**Status:** especificação de geração; nenhum vídeo novo aprovado

## Decisão técnica principal

O storyboard completo tem aproximadamente **23,5 segundos**, enquanto a geração visual individual deve ser feita em clipes curtos. Não tentar comprimir todos os sete planos em uma única geração. A estratégia mais segura é gerar **três clipes visuais de 8 segundos**, usando a mesma referência vertical oficial de KTD em todos eles, montar os cortes na edição e aparar o conjunto final para 23,5 segundos.

A geração visual deve ser solicitada **sem áudio gerado**. O trecho real do refrão da Prova 2 será inserido depois, preservando exatamente o áudio aprovado para a prova musical. Isso evita que uma trilha gerada substitua o boom bap, altere o andamento ou crie uma sincronia falsa.

| Parâmetro | Valor recomendado |
|---|---|
| Modelo preferencial | Gemini Omni Flash Preview para clipes visuais de 8 s; usar Veo 3.1 apenas se a janela permitir controle de primeiro/último frame |
| Aspect ratio | Portrait 9:16 |
| Duração por clipe | 8 s, 8 s e 8 s; aparar o master final para 23,5 s |
| Resolução | 720p para a geração rápida; upscale/export final em 1080×1920 |
| Áudio na geração | Desativado; substituir na edição pelo recorte real da Prova 2 |
| Referência | `assets/persona/ktd-visual-master.png` adaptada para 9:16; usar a mesma referência nos três clipes |
| Referência vertical preparada | `assets/ktd-official/ktd-visual-master-portrait-reference.png`, se estiver disponível no ambiente de produção |
| Movimento | Natural, firme e controlado; um plano dominante por clipe |
| Texto | Não gerar texto dentro do vídeo; aplicar legendas na pós-produção |
| Fotografia | Editorial realista, azul-noturno, carvão e âmbar de amanhecer |
| Frame rate final | 30 fps constante |
| Export final | H.264, yuv420p, 1080×1920, AAC estéreo 44,1 kHz |

## Identidade visual obrigatória de KTD

Copiar esta descrição integralmente para cada prompt. A consistência da identidade é mais importante do que a quantidade de efeitos:

> Kháirus the Dragon, known as KTD, is the same original fictional performer in every shot: a 34-year-old Black man, approximately 188 cm tall, compact athletic build, shaved head, long full black beard, deep brown skin, golden eyebrow marks, left eye honey-amber and right eye pale blue with clear natural heterochromia. His official tattoos are consistent and unchanged: seven claw marks centered on the chest, a descending diamond-dragon motif on the abdomen, seven-headed dragon imagery across the back, koi and cherry blossoms on the left arm, samurai and cloud motifs on the right arm. He wears unbranded black or charcoal streetwear. Preserve the same face, beard length, eye colors, body proportions, tattoo map and age across the entire shot and across all three clips.

Essa descrição não deve ser resumida para “um rapper negro tatuado”, porque isso permite que o gerador substitua KTD por um personagem genérico. O olho esquerdo deve permanecer mel/âmbar e o direito azul-claro; não inverter os lados.

## Prompt mestre comum

Usar este bloco no início de cada prompt, antes da descrição do plano específico:

```text
Create an original vertical music-video performance clip for KTD / Kháirus the Dragon, using the exact same official KTD identity in every frame. This is a Black Music Rap Old School / soulful boom bap visual, not nu metal, not rap-rock, not pop-rock and not a luxury-fashion commercial. KTD is a rapper first: frontal presence, precise mouth articulation, restrained hand gestures, grounded posture, controlled intensity and human timing with the boom bap pocket. The visual world is editorial urban realism: charcoal concrete, a modest recording studio, a wired dynamic microphone, a notebook, a dim blue night tone transitioning to warm amber dawn, natural skin texture and restrained film grain. No generated audio and no text inside the video; captions and graphics will be added in post-production. Keep the performer recognizable and consistent, preserve the face, beard, heterochromia, golden eyebrow marks, body proportions and official tattoo map. Use realistic camera movement, realistic hands, realistic anatomy and a single coherent visual style.
```

## Prompt negativo comum

Adicionar este bloco ao final de cada prompt. Ele deve ser tratado como parte do prompt principal, não como um campo separado se o gerador não oferecer negative prompt:

```text
Do not change the performer into another person. No generic bald model, no different beard, no clean-shaven face, no hair growth, no swapped eye colors, no reversed heterochromia, no extra eyes, no missing eye, no altered facial structure, no face morphing, no age change, no bodybuilder proportions, no extra fingers, no malformed hands, no duplicated limbs, no extra tattoos, no missing tattoos, no invented tattoo symbols, no shirt logos, no jewelry branding, no sunglasses covering the eyes, no generated captions, no watermarks, no logos, no title cards, no neon cyberpunk, no mansion, no sports car, no nightclub luxury montage, no weapons, no blood, no graphic violence, no crime glamour, no rock-guitar performance, no EDM visuals, no screaming metal vocalist, no celebrity resemblance, no imitation of any real artist, no camera shake, no strobing, no melting background, no sudden wardrobe change, no location jump inside the shot, no time-lapse face changes, no artificial beauty filter, no plastic skin, no cartoon look, no lip-sync exaggeration, no spoken words other than the silent performance gesture, no audio generation.
```

## Prompts por clipe

### Clipe A — “o olhar que voltou”

**Duração:** 8 segundos.
**Função:** executar os Quadros 01 e 02 do storyboard em um único movimento contínuo.
**Referência:** portrait reference oficial 9:16 de KTD.

```text
Use the common master prompt and the common negative prompt. Create one continuous 8-second vertical shot in a modest dark recording studio. Start with a tight frontal close-up of KTD's face, both eyes visible, then make a very slow controlled push-in during the first half. KTD performs silently to the first chorus phrase with restrained, precise mouth articulation and a low, focused expression, never shouting. A wired dynamic microphone is near the left side of his face but does not cover either eye. On the second half, ease back into a medium close-up as KTD raises the microphone slightly and marks one boom bap beat with his free hand. Reveal only the upper chest and the official seven-claw tattoo without inventing or changing any tattoo. Blue light shapes the right side of the frame and warm amber light touches the left side. The background is charcoal concrete and a simple studio wall. Hold the final pose for a clean edit point. No text, no generated audio, no location change, no cut inside the clip.
```

**Edição:** usar o áudio de 00:55,5–01:03,0 da Prova 2. Aplicar o texto na pós: `I WON'T WASTE THIS LIFE` e depois `NOT THIS TIME.`

### Clipe B — “não mais uma noite”

**Duração:** 8 segundos.
**Função:** executar os Quadros 03 e 04, conectando a porta fechada à decisão de avançar.
**Referência:** a mesma portrait reference de KTD, sem trocar de rosto.

```text
Use the common master prompt and the common negative prompt. Create one continuous 8-second vertical tracking shot in a real-looking charcoal concrete corridor before sunrise. KTD walks toward the camera with calm, deliberate rapper presence, wearing the same unbranded black streetwear and the exact same face, beard, heterochromia and body proportions. A closed metal door remains in the background and is left behind; it is only a metaphor for an ended chapter, with no lock close-up and no violence. In the second half, match the movement into a close insert of KTD's hand closing a worn notebook, then let the camera rise with him as warm dawn light begins to appear behind him. Keep his profile and front angle consistent, with no morphing. Use natural walking speed, gentle handheld stability, muted blue shadows and a restrained amber horizon. Hold the upward-looking pose for an edit point. No text, no generated audio, no jump cut inside the clip.
```

**Edição:** usar o áudio de 01:03,0–01:11,0 da Prova 2. Aplicar o texto na pós: `NO MORE NIGHT` e `TURNED EVERY LOSS INTO A REASON TO RISE.`

### Clipe C — “a luz não apaga a cicatriz”

**Duração:** 8 segundos.
**Função:** executar os Quadros 05, 06 e 07; o editor fará os cortes internos na batida.
**Referência:** a mesma portrait reference oficial de KTD.

```text
Use the common master prompt and the common negative prompt. Create one continuous 8-second vertical shot that begins in a medium frontal performance setup inside the same modest recording studio and gradually moves toward warm dawn backlight. KTD performs silently as a rapper with exact, economical hand gestures: one single tap on a plain studio table, then one controlled gesture toward his chest. Keep the official tattoo map visible only where physically appropriate. Anonymous soft silhouettes may remain far in the background as a community response, but they must be blurred and must not resemble KTD. In the final half, transition through a smooth camera move to KTD standing half in blue shadow and half in warm amber light; he takes one deliberate step into the light, breathes visibly, looks into the camera and holds a calm, resolved expression. End on a close frontal pose with both eyes visible, matching the composition of the first shot for a seamless loop. No text, no generated audio, no extra performers in focus, no location change, no distorted face.
```

**Edição:** usar o áudio de 01:11,0–01:19,0 da Prova 2. Aplicar os cortes no kick e na snare; texto na pós: `I WON'T WASTE THIS LIFE`, `THE DARK DIDN'T TAKE EVERYTHING.` e `WHAT ARE YOU DONE WASTING?`

## Fluxo de composição e sincronização

1. Gerar os três clipes visuais separadamente, sempre com a mesma referência vertical e o mesmo bloco de identidade.
2. Não aceitar automaticamente o primeiro resultado. Conferir olhos, barba, rosto, mãos, tatuagens e roupa em cada clipe antes da montagem.
3. Montar A + B + C em uma sequência de 24 segundos e aparar 0,5 segundo da cauda, ou ajustar os pontos de corte para obter exatamente 23,5 segundos.
4. Inserir o trecho real de áudio da Prova 2 a partir de 00:55,5. Não usar áudio gerado pelo vídeo.
5. Cortar visualmente nos ataques de kick e snare, mas não cortar a boca de KTD em meio a uma sílaba importante. Quando a sincronização labial não for perfeita, cobrir a transição com caderno, mão, microfone, perfil ou silhueta.
6. Aplicar texto e legendas na edição, nunca dentro do prompt. A tipografia deve ser condensada, marfim ou âmbar claro, com sombra preta discreta.
7. Fazer o último close retornar visualmente ao primeiro close. O loop deve parecer intencional.

## Zonas seguras e exportação

Manter textos aproximadamente entre 20% e 78% da altura do quadro e entre 10% e 88% da largura. Evitar a faixa inferior, onde ficam legenda, nome do áudio e controles, e evitar a lateral direita, onde ficam os ícones de interação. Nunca cobrir os olhos, a boca ou o peito tatuado de KTD com texto.

| Item | Especificação de entrega |
|---|---|
| Canvas | 1080×1920, 9:16 |
| Codec de vídeo | H.264 High Profile, yuv420p |
| Frame rate | 30 fps constante |
| Bitrate de vídeo | Aproximadamente 12–20 Mbps, conforme tamanho final |
| Áudio | AAC-LC, estéreo, 44,1 kHz, 192–256 kbps |
| Duração | 23,5 s para a versão principal |
| Loudness | Preservar o recorte da Prova 2; evitar normalização destrutiva adicional |
| True peak | Manter abaixo de −1 dBTP na exportação final |
| Texto | Aplicado na pós, com contraste e safe zone |
| Arquivo | MP4, sem watermark e sem elementos de interface |

## Critérios de rejeição visual

Rejeitar o clipe se KTD parecer outro homem, se a heterocromia estiver invertida ou ausente, se a barba mudar de comprimento, se a cabeça deixar de ser raspada, se as tatuagens forem substituídas por desenhos genéricos, se o corpo ficar desproporcional, se surgirem mãos defeituosas, se o vídeo virar publicidade de carros/mansões, se a estética migrar para nu metal/rock, se houver texto gerado ilegível ou se a performance não parecer a de um rapper.

A fidelidade visual tem prioridade sobre efeitos e virtuosismo de câmera. Um plano simples de KTD correto, com boa luz e presença, é preferível a uma sequência visualmente espetacular com um personagem incorreto.

## Critérios de aprovação final

A peça só deve ser considerada pronta quando o espectador reconhecer KTD sem ler o nome, identificar o hook nos primeiros segundos, perceber o swing e a postura de rapper old school, compreender a passagem da sombra para a luz e conseguir responder à pergunta final. A geração visual não aprova o áudio nem a letra; ela apenas acompanha a Prova 2 musical, que continua sujeita à avaliação humana.
