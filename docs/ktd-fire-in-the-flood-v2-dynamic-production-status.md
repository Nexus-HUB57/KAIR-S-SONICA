# FIRE IN THE FLOOD — produção dinâmica v2

A versão anterior foi rejeitada porque transformava imagens estáticas em um slideshow. A nova direção segue os vídeos aprovados em `assets/video/aprovados`: cada bloco precisa ser um plano contínuo com ação temporal real, câmera em movimento, cenário reativo e atuação de KTD.

## Estado atual

O plano D01 foi gerado como vídeo contínuo e salvo em `artifacts/video/dynamic-shots/fire-in-the-flood-v2-D01-walk.mp4`. O arquivo foi produzido com KTD caminhando por uma rua industrial alagada, câmera em dolly-back, chuva, respingos, vapor e reflexo âmbar.

A geração do plano D02 foi bloqueada pela cota diária gratuita de vídeo. Os 21 planos e o assembler já estão definidos no repositório; nenhum still será convertido em vídeo por zoom, pan, grão ou dissolvência. A montagem final só deve ser promovida quando os 21 planos contínuos estiverem disponíveis e aprovados individualmente.

## Próxima ação de produção

Aguardar a reposição da cota diária ou liberar a geração de vídeo por upgrade. Após isso, gerar D02–D21 usando `docs/ktd-fire-in-the-flood-dynamic-generation-prompt-pack.md`, validar cada MP4 por duração e continuidade e executar `scripts/assemble_fire_in_the_flood_dynamic.py` para o master de 168 segundos.

## Critério de bloqueio

Não entregar uma montagem de 2min48s composta apenas por repetição de D01 ou por stills animados. A narrativa precisa preservar a progressão janela → enchente → resistência → estúdio → rua → rooftop → performance → reconstrução, com microações concretas em todos os planos.
