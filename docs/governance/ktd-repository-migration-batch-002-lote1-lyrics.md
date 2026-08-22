# KTD — Migração batch-002: letras e traduções do Lote 1

**Data:** 22 de agosto de 2026
**Origem:** `Nexus-HUB57/KAIR-S-SONICA`
**Destino:** `Nexus-HUB57/khairus_KTD`
**Estratégia:** cópia não destrutiva com revisão linha a linha
**Diretriz aplicada:** [ktd-repository-storage-policy-v2.md](ktd-repository-storage-policy-v2.md)

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

## Checksums SHA-256 dos arquivos de destino

Os checksums abaixo correspondem aos 18 registros textuais publicados na matriz central do destino em `164ae5ab4f26d8efc266c5f666174529dc3fe610`.

| Single | Registro | Caminho no destino | SHA-256 |
|---:|---|---|---|
| 4 | Original EN v1 | `lyrics/singles/single-4-pressure-speaks/original-en/single-4-pressure-speaks-lyrics-essence-v1.md` | `a539e170bf1fdb86694fb4788fdda2a135b47a863d9331d71b1b1b4d55850d6d` |
| 4 | PT-BR v1 arquivada | `lyrics/singles/single-4-pressure-speaks/pt-BR-reference/archive/single-4-pressure-speaks-lyrics-pt-br-v1-archived.md` | `f0023648dc43b14d909a34362dc76583ec48d2c7d33ef5fc7c2de65f064675af` |
| 4 | PT-BR v2 revisada | `lyrics/singles/single-4-pressure-speaks/pt-BR-reference/single-4-pressure-speaks-lyrics-pt-br-v2.md` | `71aa75e550a84008f5b5ae0447ae4efaaa097d9d132cda805ad7b409ad5b68b9` |
| 5 | Original EN v1 | `lyrics/singles/single-5-no-more-quiet-cries/original-en/single-5-no-more-quiet-cries-lyrics-v1.md` | `30cb3af2357bb83dff3d09b634fe832c970820f1366b427ef5e56628cee863c2` |
| 5 | PT-BR v1 arquivada | `lyrics/singles/single-5-no-more-quiet-cries/pt-BR-reference/archive/single-5-no-more-quiet-cries-lyrics-pt-br-v1-archived.md` | `98d2d27f274b1f64e39528c147a4fd7dded543d8ed2afe12079ff01ded68a389` |
| 5 | PT-BR v2 revisada | `lyrics/singles/single-5-no-more-quiet-cries/pt-BR-reference/single-5-no-more-quiet-cries-lyrics-pt-br-v2.md` | `4ebda21c1e9d53c04c7f83887f6c9b2601c8a09bb6633b3f7d5d2a97f6febba4` |
| 7 | Original EN v1 | `lyrics/singles/single-7-no-one-saved-me-a-seat/original-en/single-7-no-one-saved-me-a-seat-lyrics-v1.md` | `fb46e4417f78ef6059c3fc97f81e53301ded60f5ad197bada9866e279a4b9cd9` |
| 7 | PT-BR v1 arquivada | `lyrics/singles/single-7-no-one-saved-me-a-seat/pt-BR-reference/archive/single-7-no-one-saved-me-a-seat-lyrics-pt-br-v1-archived.md` | `6279200fd49e5659aef90d23347c5dbcb0630162b5dee8de1abe499ef1a24d8c` |
| 7 | PT-BR v2 revisada | `lyrics/singles/single-7-no-one-saved-me-a-seat/pt-BR-reference/single-7-no-one-saved-me-a-seat-lyrics-pt-br-v2.md` | `ed751d50cffc0395257fa0266e58c22cccfc4a7058d1cb0ee5835ef23ccdf12b` |
| 8 | Original EN v1 | `lyrics/singles/single-8-build-the-door-behind-me/original-en/single-8-build-the-door-behind-me-lyrics-v1.md` | `cb51811d0b1a4d04c51e3c4d1e28daa7960e70140a8e704242c9e8e97df5bdce` |
| 8 | PT-BR v1 arquivada | `lyrics/singles/single-8-build-the-door-behind-me/pt-BR-reference/archive/single-8-build-the-door-behind-me-lyrics-v1-archived.md` | `4f5a8e1eaafee70ecdda98f90151e9f5f789c386cc933c4066a5acc0ee52ba9b` |
| 8 | PT-BR v2 revisada | `lyrics/singles/single-8-build-the-door-behind-me/pt-BR-reference/single-8-build-the-door-behind-me-lyrics-pt-br-v2.md` | `22a53f60afa0a424c518e34104fc79e28bc3abfdecead036fae1c1c0fd37bf87` |
| 9 | Original EN v1 | `lyrics/singles/single-9-you-came-back-when-i-won/original-en/single-9-you-came-back-when-i-won-lyrics-v1.md` | `3550eceedf784de645180e7e443157f121f94f57cbe922e883d511f9ac79f48b` |
| 9 | PT-BR v1 arquivada | `lyrics/singles/single-9-you-came-back-when-i-won/pt-BR-reference/archive/single-9-you-came-back-when-i-won-lyrics-pt-br-v1-archived.md` | `44aafcfdf704bc557f4245e7d3f38b8cc0029edf27b0a3b6de0ab2c311900e06` |
| 9 | PT-BR v2 revisada | `lyrics/singles/single-9-you-came-back-when-i-won/pt-BR-reference/single-9-you-came-back-when-i-won-lyrics-pt-br-v2.md` | `7f2724cc3ddcbb32f3efdd05ae5bde0a994f5b9a5112d98bef47b91feec5db79` |
| 10 | Original EN v1 | `lyrics/singles/single-10-the-dragon-sleeps/original-en/single-10-the-dragon-sleeps-lyrics-v1.md` | `c9210b242ebc403649b0f36d6e3ab5ca818de2f03dca85a6bc5e1133016f5518` |
| 10 | PT-BR v1 arquivada | `lyrics/singles/single-10-the-dragon-sleeps/pt-BR-reference/archive/single-10-the-dragon-sleeps-lyrics-pt-br-v1-archived.md` | `002e44ad37458258e68f5922e74d5bb3ce4bdbbecd839de1e0a59be00513db27` |
| 10 | PT-BR v2 revisada | `lyrics/singles/single-10-the-dragon-sleeps/pt-BR-reference/single-10-the-dragon-sleeps-lyrics-pt-br-v2.md` | `d6f8983e445cc31bcbb9e760b300baa32df91c5bce4a44c4481f032961a5ee0a` |

## Status e segurança

As seis fontes inglesas estão registradas como `approved_official` conforme os documentos de origem. As traduções v2 estão registradas como `approved_reference`, isto é, revisadas como tradução de referência, nunca como nova composição oficial. As traduções v1 permanecem como `archived_reference`.

O lote não inclui áudio novo, vídeo novo, provas, demos, stems, candidatos, material reprovado, tokens OAuth, App Secrets, Client Secrets, refresh tokens, contratos, dados administrativos privados ou dados de fãs. A Prova 2 Old School do Single 11 continua fora deste lote e permanece pendente de avaliação humana.

## Commits

| Repositório | Commit |
|---|---|
| `khairus_KTD` | `164ae5ab4f26d8efc266c5f666174529dc3fe610` |
| `KAIR-S-SONICA` | será preenchido após o registro desta migração |

A cópia é não destrutiva. Qualquer remoção ou transformação de duplicatas deve ocorrer em alteração posterior, após verificar links, manifests, consumidores e rollback.
