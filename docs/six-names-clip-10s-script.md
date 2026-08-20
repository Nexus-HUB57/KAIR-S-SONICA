# SIX NAMES (Rebuilt Soul) — roteiro visual do clipe de 10 segundos

## Formato e padrão

O clipe segue exatamente o padrão aprovado da versão de 10 s de UNLEASH THE DRAGON: vídeo real contínuo de **10,000 s**, vertical **720x1280 @24fps**, câmera steadicam/dolly, chiaroscuro com pretos densos, paleta restrita, sem texto ou logotipo sobreposto. A master oficial aprovada da faixa é `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` (165,198 s, 96 BPM).

## Cena escolhida e motivo

A cena é a **mesa familiar com seis lugares vazios**, retomando o plano mais forte do teaser v2 aprovado em workflow (a mesa, a vela e a memória) e conectando-se ao tema da faixa: os seis nomes da família. O clipe de 10 s abre com KTD acendendo a vela no centro da mesa e encerrando com o olhar para a câmera, com a família simbolicamente presente na composição. Essa escolha preserva a continuidade da identidade visual já aprovada da faixa, em vez de introduzir cena nova.

## Cronologia narrativa (10 s)

| Tempo | Ação em vídeo real contínuo |
| --- | --- |
| 0,0–2,0 s | KTD acende a vela no centro da mesa de madeira com seis pratos; a chama cresce; camera dolly-in lenta |
| 2,0–6,0 s | Ele acende as outras velas menores ao redor, uma a uma, com movimento natural de mãos; as luzes quentes refletem nos pratos |
| 6,0–8,5 s | Senta-se na cabeceira, junta as mãos, fecha os olhos um instante e os abre com seriedade |
| 8,5–10,0 s | Olhar direto para a câmera, leve levante de queixo; a chama das seis velas ilumina o rosto; fade-out do áudio |

## Mapa obrigatório de tatuagens (correção aplicada)

O prompt deve descrever literalmente o mapa oficial auditado em `docs/ktd-chest-tattoo-official-map-audit.md`, com **`assets/persona/ktd-visual-master.png` enviada como imagem de referência junto à keyframe**: sete garras com pontas em diamante descendo verticalmente do esterno na parte superior do peito; coluna de escamas simétrica descendo pela linha do abdômen até a cabeça do dragão junto ao umbigo; samurai de armadura no braço e ombro esquerdos; carpa koi no braço direito; flores de cerejeira integradas. É proibido representar o peito com barras horizontais de garra — a divergência detectada na geração anterior da música 1.

## Áudio muxado

Trecho escolhido da master aprovada: **60,0–70,0 s**, o pico de energia da faixa (RMS médio 0,244, o maior da música), contendo o refrão mais inspirador: *"Every winter, now we light the dark. If I rise, we rise, let the whole block know... Six inches in my chest, six flames in one heart."* A janela de acender as seis velas se encaixa literalmente na letra "six flames in one heart". Fade-in de 0,3 s e fade-out de 0,5 s via `scripts/mux_utd_clip_audio.py` (com o arquivo correto de SIX NAMES designado na chamada).

## Estado de produção

| Item | Estado |
| --- | --- |
| Keyframe da cena (mesa com seis lugares) | Existente: `assets/video/promos/tiktok/six-names-ktd-shot-01-table-performance.png` (revisão v1 aprovada em workflow) — pode exigir regeneração se o mapa de tatuagens do peito não estiver correto |
| Geração de vídeo (10 s) | Pendente de reset do limite diário de vídeo (1 geração por dia) |
| Muxagem | Pipeline validado; chamada com `six-names-rebuilt-soul-pre-release-v2.wav`, janela 60,0–70,0 s |
| Aprovação | Pendente de revisão humana após a geração |
