# FIRE IN THE FLOOD — status de produção dinâmica

## Decisão editorial

A direção está corrigida: o videoclipe não será produzido com imagens estáticas animadas. A referência válida passa a ser a linguagem dos reels aprovados do ecossistema KTD, em que o artista atua dentro de um cenário vivo, a câmera se desloca em relação ao corpo, objetos e fenômenos físicos reagem e os planos possuem continuidade temporal observável.

Os arquivos `fire-in-the-flood-ktd-approved-dynamic-8s.mp4` e `six-names-ktd-clip-table-candles-10s-with-audio.mp4` foram baixados, medidos e analisados. Ambos são vídeos verticais em 720×1280 a 24 fps; o primeiro tem 8 s e o segundo 10 s. A análise confirma como requisitos de linguagem: caminhada de poder e dolly-back no caso de Fire in the Flood; ação ritual concreta, mudança de escala e fogo/fumaça vivos no caso de Six Names.

## O que foi invalidado

O render `ktd-fire-in-the-flood-full-v1.mp4` e a prova `ktd-fire-in-the-flood-full-v2.mp4` permanecem no repositório como histórico técnico, mas não atendem ao critério editorial revisado porque derivam de PNGs com movimento simulado. Eles não devem ser apresentados como rough cut criativo aprovado.

## O que foi preparado

A nova decupagem divide os 168 s em 21 planos contínuos de 8 s. O documento `docs/ktd-fire-in-the-flood-v3-dynamic-video-treatment.md` descreve a ação dramática de cada plano, a relação com a letra, o movimento de câmera, a luz, a água, o fogo, a chuva, a performance e as transições.

O manifest `data/releases/fire-in-the-flood-dynamic-shot-manifest-v1.json` registra tempos, ações, keyframes, arquivos de saída e estados de produção. O script `scripts/assemble_fire_in_the_flood_dynamic.py` fará a concatenação dos 21 clipes vivos e o mux final com `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` quando todos os planos estiverem disponíveis.

Foram preparados keyframes 16:9 para caminhada na inundação, booth de estúdio, bridge vulnerável e hook final. Esses arquivos servem como referências de identidade e encenação para geração de vídeo, não como imagens finais do clipe.

## Prova gerada

O plano `artifacts/video/dynamic-shots/fire-in-the-flood-d01-walk-8s.mp4` foi gerado como vídeo contínuo de 8 s, 1280×720, 24 fps, H.264, com áudio silencioso temporário para posterior muxagem. Sua cadeia visual contém KTD caminhando pela água, chuva, respingos, vapor, câmera recuando e chama âmbar refletida no piso.

A segunda geração de vídeo foi bloqueada pelo limite diário disponível do plano gratuito, informado como `1/1`. Assim, os demais 20 planos estão preparados no manifest, mas ainda aguardam a renovação da cota ou uma atualização do plano. Não foi criado um falso clipe completo repetindo o mesmo reel; isso violaria a exigência de narrativa viva e variedade de cenários.

## Próximo passo técnico

Após a liberação da cota, gerar os planos em ordem dramática, priorizando D06 (booth), D08 (primeiro hook), D17 (bridge) e D19 (hook final) para validar quatro estados de performance antes de completar os demais. Cada plano deve ser rejeitado se parecer uma fotografia com zoom, apresentar morphing de rosto/tatuagem ou abandonar a ação descrita no manifest.
