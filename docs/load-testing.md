# Teste de carga do endpoint de orquestração

## Objetivo

O teste verifica o comportamento do `POST /v1/orchestrate` quando múltiplas tarefas de áudio são submetidas em paralelo. O utilitário não simula um benchmark sintético interno: ele usa HTTP contra a API local, acompanha cada `task_id` até um estado terminal e registra latências, throughput, taxa de sucesso e erros individuais.

## Cenário de referência

| Parâmetro | Valor |
| --- | ---: |
| Endpoint | `POST /v1/orchestrate` |
| Tarefas submetidas | 20 |
| Concorrência do cliente | 5 |
| Duração procedural | 1 segundo |
| Sample rate | 8 kHz |
| Formato | WAV |
| Transcrição | Desativada |
| Referência de áudio | WAV existente em `data/output` |
| Ambiente | API local, execução CPU |

A execução reproduzível é feita por `make load`, ou diretamente com `PYTHONPATH=packages python3 scripts/load_test_orchestrate.py --requests 20 --concurrency 5`. O relatório JSON é salvo em `reports/load/`, que é ignorado pelo Git.

## Resultado observado

A rodada com referência WAV concluiu as 20 tarefas sem erro ou timeout. O throughput observado foi de **36,9 tarefas por segundo**, com latência de submissão média de **11,3 ms** e latência fim a fim de **71,3 ms no P50** e **78,8 ms no P95**. Esses números descrevem o cenário local com o gerador procedural e uma referência curta compartilhada para análise concorrente; não devem ser tratados como capacidade de produção, especialmente para modelos neurais, arquivos longos, workers distribuídos ou storage remoto.

| Métrica | Resultado |
| --- | ---: |
| Sucesso | 20/20 — 100% |
| Tempo total | 0,542 s |
| Throughput | 36,9 tarefas/s |
| Submissão média | 11,3 ms |
| Submissão P95 | 15,9 ms |
| Fim a fim P50 | 71,3 ms |
| Fim a fim P95 | 78,8 ms |
| Fim a fim P99 | 106,2 ms |

## Interpretação

O resultado valida três propriedades do MVP: o gateway aceita concorrência sem bloquear a resposta inicial, o `TaskStore` acompanha tarefas independentes e o worker consegue concluir os artefatos em paralelo no cenário curto. O teste também fornece uma linha de base para comparar mudanças no pipeline, no painel de monitoramento ou no backend de geração.

Para uma avaliação de produção, amplie o cenário com arquivos de entrada reais, transcrição Faster-Whisper, MP3 via FFmpeg, durações de minutos, concorrência progressiva, memória, CPU, I/O, filas duráveis e workers separados. Registre p99, erros por classe, consumo de recursos e saturação antes de definir metas de capacidade.

## Referências

[1]: ../scripts/load_test_orchestrate.py "Utilitário de carga do repositório"
[2]: ../docs/api.md "Contrato da API do KAIR-S-SONICA"
[3]: https://www.python-httpx.org/ "HTTPX documentation"
