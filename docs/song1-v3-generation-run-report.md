# Relatório de execução v3 — porta e palco

## Resultado da execução

O pacote de geração v3 foi executado com o take C02 da travessia da porta usando a referência aprovada de KTD, formato vertical e exigência de movimento físico contínuo. O serviço bloqueou a geração ao retornar o limite diário do plano gratuito: `You've reached today's free plan limit for video generation (1/1) - please upgrade or wait for your quota to reset.`

Por esse motivo, o take C02 real não foi produzido nesta execução e o take C03 real de performance também não foi iniciado. A equipe não deve interpretar arquivos estáticos, provas anteriores ou movimentos de câmera sobre still como substitutos desses takes.

## Parâmetros v3 preparados

| Take | Referência | Duração | Formato | Ação física obrigatória |
| --- | --- | --- | --- | --- |
| C02 porta | `song1-unleash-the-dragon-door-to-stage-ktd-lock-v2.png` | 8 s | vertical 9:16, 720p, sem áudio | respirar, girar maçaneta, abrir porta, transferir peso, dar passo e cruzar limiar |
| C03 palco | `song1-fullmv-scene-c3-hook-perf.png` | 8 s | vertical 9:16, 720p, sem áudio | inspirar, articular boca, mudar peso, mover ombros/mão e interagir com microfone |

A identidade obrigatória permanece: cabeça raspada, barba longa, pele marrom profunda, marcas douradas nas sobrancelhas, olho esquerdo mel/âmbar, olho direito azul-pálido e tatuagens acompanhando a orientação corporal. São proibidos rosto genérico, troca de olhos, neon azul, tatuagem mutante, mãos deformadas, boca imóvel, still image, Ken Burns, pan/zoom sem ação, morphing ou salto de pose.

## Teste de validação do pipeline

O teste de regressão foi executado com os arquivos em `assets/video/promos/reprovados/static_proof/`. O sistema retornou `Clipe bloqueado pelo manifesto de identidade` no primeiro ativo estático e não criou arquivo de saída. Resultado: **`GATE_REGRESSION=PASS`** e **`RENDER_OUTPUT=ABSENT`**.

Isso confirma que a proteção funciona antes do FFmpeg: ativos com `rejected_static_proof`, caminho em quarentena ou hash bloqueado não chegam à montagem, mesmo quando carregados com `--proof`.

## Próxima execução

Depois do reset da quota, executar C02 e C03 como takes independentes. Revisar ambos quadro a quadro antes de qualquer tratamento. Registrar seus hashes como `identity_pass` somente quando movimento físico e identidade forem aprovados. Em seguida, montar 24 segundos sem áudio e submeter a nova revisão editorial.
