# Single 17 — Princess, No More — desenvolvimento de Reels v1

**Projeto:** KAIR-S-SONICA  
**Artista:** Kháirus The Dragon (KTD)  
**Status:** `GENERATED_TEST`  
**Data:** 2026-09-02

## Escopo concluído

Foi criado o primeiro pacote visual do Reel do single 17, com três keyframes verticais em 9:16, mantendo a identidade visual do KTD a partir do retrato-mestre e separando o arco em **proteção**, **recuperação/autonomia** e **hook performático**. Os frames foram produzidos sem texto, logotipos ou marcas d’água para preservar a camada editorial posterior.

| Frame | Função narrativa | Arquivo |
|---|---|---|
| A | Proteção sem ameaça: corredor hospitalar, gesto aberto e porta iluminada | `assets/reels/single-17-princess-no-more/single-17-frame-a-protection.png` |
| B | Recuperação e autonomia: KTD dá espaço enquanto a irmã segue em direção à luz | `assets/reels/single-17-princess-no-more/single-17-frame-b-recovery.png` |
| C | Hook: performance com gesto aberto, liberdade em vez de vingança | `assets/reels/single-17-princess-no-more/single-17-frame-c-hook.png` |

## Geração de vídeo

A tentativa de gerar os três clipes de movimento real em `gemini-omni-flash-preview` foi bloqueada pelo acesso do plano atual. Nenhum MP4 foi criado nesta etapa. O pacote está preparado para três clipes independentes de 8 segundos, 720p, portrait 9:16, sem áudio gerado; o áudio deverá ser aplicado posteriormente na edição, após decisão sobre a prova musical.

Não substituir a geração de movimento real por slideshow, zoom procedural ou imagem estática. O padrão de continuidade exigido pelo projeto é ação física contínua, câmera fluida e ausência de violência gráfica ou glamourização da retaliação.

## Áudio de referência

As provas musicais já disponíveis incluem `single-17-princess-come-back-proof-a-melodic-v1.mp3` e `single-17-princess-come-back-proof-b-documentary-v1.mp3`. A seleção do recorte final deve priorizar o hook “Princess, come back — those walls were never love” e a mensagem de liberdade, sem usar a ponte de agressão como gancho principal.

## Próxima ação

Com acesso à geração de vídeo habilitado, gerar os clipes A, B e C usando seus respectivos PNGs como referência inicial. Em seguida, validar cada MP4 com `ffprobe`, montar uma versão de distribuição com o trecho musical aprovado e registrar duração, codec, checksum e status de revisão humana. Os três PNGs e o manifesto JSON permanecem `GENERATED_TEST` até aprovação humana de identidade, composição, continuidade e mensagem.

## Proveniência

O inventário com dimensões e SHA-256 está em [`single-17-princess-no-more-keyframes-manifest-v1.json`](single-17-princess-no-more-keyframes-manifest-v1.json).
