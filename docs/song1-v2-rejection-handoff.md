# Handoff corrigido — reprovação da prova v2 da música 1

## Estado editorial

A prova v2 de 24 segundos foi **reprovada**. Apenas o primeiro bloco, correspondente ao camarote, segue o padrão audiovisual estabelecido. Os blocos da porta e do palco são imagens estáticas com deslocamento de câmera aplicado em pós-produção; portanto, não demonstram movimento físico de personagem e não podem ser classificados como clipes de qualidade profissional.

A decisão é preservada no manifesto de continuidade. Os ativos estáticos foram movidos para `assets/video/promos/reprovados/static_proof/` e estão bloqueados por caminho, hash e status editorial. A primeira cena real continua preservada como a única cena elegível do conjunto atual.

## Matriz de ativos

| Ativo | Estado | Ação |
| --- | --- | --- |
| Camarote real, 8 s | Aprovado em revisão anterior | Preservar como referência de qualidade e possível primeiro bloco. |
| Porta corrigida, imagem | Aprovada somente como referência de identidade | Usar como input de geração, nunca como vídeo. |
| Performance de palco, imagem | Aprovada somente como referência de identidade | Usar como input de geração, nunca como vídeo. |
| Prova da porta, 8 s | Reprovada: `rejected_static_proof` | Manter em quarentena; não montar. |
| Prova de performance, 8 s | Reprovada: `rejected_static_proof` | Manter em quarentena; não montar. |
| Sequência v2, 24 s | Reprovada: contém dois blocos estáticos | Manter em quarentena; não distribuir como prova audiovisual. |

## Protocolo obrigatório para a retomada

A próxima geração deverá produzir dois clipes independentes de oito segundos com movimento audiovisual real. Na porta, KTD precisa respirar, girar a maçaneta, abrir a porta, transferir peso, dar um passo e atravessar o limiar. No palco, precisa inspirar, articular a boca, mudar o peso corporal, movimentar ombros e mão livre e interagir fisicamente com o microfone.

A câmera pode acompanhar a ação, mas não pode substituí-la. Pan, zoom, Ken Burns, morphing ou simples deslocamento sobre uma imagem estática são motivos de reprovação imediata.

## Gate de identidade e qualidade

Antes da montagem, cada take precisa passar por revisão quadro a quadro. O rosto deve continuar sendo KTD; o olho esquerdo deve permanecer mel/âmbar e o direito azul-pálido; tatuagens devem acompanhar a orientação corporal sem mutação; mãos, boca e peso corporal devem apresentar continuidade; cenário, fumaça e luz devem permanecer coerentes; áudio só entra depois da aprovação da mixagem oficial.

O arquivo só pode receber `identity_pass` quando movimento físico e identidade forem aprovados. O modo `--proof` e qualquer saída `proof_only` estão proibidos para a rota de promoção final.

## Próximo responsável

Gerar o C02 físico e o C03 físico com as referências de KTD no pacote `docs/song1-real-motion-generation-package-v3.md`. Submeter ambos à revisão quadro a quadro. Somente após os dois passes a equipe deve remontar os 24 segundos e reabrir o handoff audiovisual.
