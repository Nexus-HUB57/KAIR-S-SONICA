# KTD — Migração batch-002: letras e traduções do Lote 1

**Data:** 22 de agosto de 2026
**Origem:** `Nexus-HUB57/KAIR-S-SONICA`
**Destino:** `Nexus-HUB57/khairus_KTD`
**Estratégia:** cópia não destrutiva com revisão linha a linha

## Escopo

Este lote aplica a diretriz v2 de armazenamento e organiza no repositório audiovisual os pares de letra original em inglês e tradução PT-BR de referência dos Singles 4, 5, 7, 8, 9 e 10. As fontes de produção permanecem preservadas no `KAIR-S-SONICA`.

O repositório de destino contém uma cópia do original inglês v1, a tradução PT-BR v1 preservada em `archive/`, a tradução PT-BR v2 revisada e o ledger correspondente de comparação linha a linha.

## Mapa do lote

| Single | Original inglês | PT-BR v1 arquivada | PT-BR v2 revisada | Ledger |
|---:|---|---|---|---|
| 4 | `lyrics/singles/single-4-pressure-speaks/original-en/single-4-pressure-speaks-lyrics-essence-v1.md` | `lyrics/singles/single-4-pressure-speaks/pt-BR-reference/archive/single-4-pressure-speaks-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-4-pressure-speaks/pt-BR-reference/single-4-pressure-speaks-lyrics-pt-br-v2.md` | `lyrics/singles/single-4-pressure-speaks/reviews/line-review-v2.md` |
| 5 | `lyrics/singles/single-5-no-more-quiet-cries/original-en/single-5-no-more-quiet-cries-lyrics-v1.md` | `lyrics/singles/single-5-no-more-quiet-cries/pt-BR-reference/archive/single-5-no-more-quiet-cries-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-5-no-more-quiet-cries/pt-BR-reference/single-5-no-more-quiet-cries-lyrics-pt-br-v2.md` | `lyrics/singles/single-5-no-more-quiet-cries/reviews/line-review-v2.md` |
| 7 | `lyrics/singles/single-7-no-one-saved-me-a-seat/original-en/single-7-no-one-saved-me-a-seat-lyrics-v1.md` | `lyrics/singles/single-7-no-one-saved-me-a-seat/pt-BR-reference/archive/single-7-no-one-saved-me-a-seat-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-7-no-one-saved-me-a-seat/pt-BR-reference/single-7-no-one-saved-me-a-seat-lyrics-pt-br-v2.md` | `lyrics/singles/single-7-no-one-saved-me-a-seat/reviews/line-review-v2.md` |
| 8 | `lyrics/singles/single-8-build-the-door-behind-me/original-en/single-8-build-the-door-behind-me-lyrics-v1.md` | `lyrics/singles/single-8-build-the-door-behind-me/pt-BR-reference/archive/single-8-build-the-door-behind-me-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-8-build-the-door-behind-me/pt-BR-reference/single-8-build-the-door-behind-me-lyrics-pt-br-v2.md` | `lyrics/singles/single-8-build-the-door-behind-me/reviews/line-review-v2.md` |
| 9 | `lyrics/singles/single-9-you-came-back-when-i-won/original-en/single-9-you-came-back-when-i-won-lyrics-v1.md` | `lyrics/singles/single-9-you-came-back-when-i-won/pt-BR-reference/archive/single-9-you-came-back-when-i-won-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-9-you-came-back-when-i-won/pt-BR-reference/single-9-you-came-back-when-i-won-lyrics-pt-br-v2.md` | `lyrics/singles/single-9-you-came-back-when-i-won/reviews/line-review-v2.md` |
| 10 | `lyrics/singles/single-10-the-dragon-sleeps/original-en/single-10-the-dragon-sleeps-lyrics-v1.md` | `lyrics/singles/single-10-the-dragon-sleeps/pt-BR-reference/archive/single-10-the-dragon-sleeps-lyrics-pt-br-v1-archived.md` | `lyrics/singles/single-10-the-dragon-sleeps/pt-BR-reference/single-10-the-dragon-sleeps-lyrics-pt-br-v2.md` | `lyrics/singles/single-10-the-dragon-sleeps/reviews/line-review-v2.md` |

## Resultado da revisão

Foram conferidas **475 linhas líricas pareadas**: 63 do Single 4, 82 do Single 5, 72 do Single 7, 88 do Single 8, 88 do Single 9 e 82 do Single 10. Nenhum original inglês foi alterado.

As correções registradas nas traduções v2 foram limitadas a referências linguísticas e estruturais:

| Single | Correção |
|---:|---|
| 4 | `encontrar uma fala` → `encontrar voz`, preservando o sentido de `found a speech` com formulação mais natural |
| 5 | Nenhuma alteração semântica; estrutura e conteúdo foram confirmados |
| 7 | `passagem` → `portão` nos trechos correspondentes a `gate` |
| 8 | Nenhuma alteração semântica; estrutura e conteúdo foram confirmados |
| 9 | `já tinha partido` → `já tinha ido embora` e `pelo meio` → `pelos círculos sociais`, preservando ambiguidade e inteligibilidade |
| 10 | Restauração da linha `Você pode amar os números, pode adorar o brilho.` no segundo refrão e correção da observação de status |

## Status e segurança

As seis fontes inglesas estão registradas como `approved_official` conforme os documentos de origem. As traduções v2 estão registradas como `approved_reference`, isto é, revisadas como tradução de referência, nunca como nova composição oficial. As traduções v1 permanecem como `archived_reference`.

O lote não inclui áudio novo, vídeo novo, provas, demos, stems, candidatos, material reprovado, tokens OAuth, App Secrets, Client Secrets, refresh tokens, contratos, dados administrativos privados ou dados de fãs. A Prova 2 Old School do Single 11 continua fora deste lote e permanece pendente de avaliação humana.

## Commits

| Repositório | Commit |
|---|---|
| `khairus_KTD` | `4351a7090dfcac0bdcd3c299b07aaa2854b504fe` |
| `KAIR-S-SONICA` | será preenchido após o registro desta migração |

A cópia é não destrutiva. Qualquer remoção ou transformação de duplicatas deve ocorrer em alteração posterior, após verificar links, manifests, consumidores e rollback.
