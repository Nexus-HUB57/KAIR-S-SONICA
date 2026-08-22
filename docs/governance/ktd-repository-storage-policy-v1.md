# KTD — Diretriz de armazenamento entre repositórios v1

## 1. Decisão de autoridade

A partir desta diretriz, o ecossistema KTD passa a ter duas fontes de verdade complementares:

| Repositório | Autoridade | Conteúdo principal |
|---|---|---|
| `Nexus-HUB57/KAIR-S-SONICA` | **Produção, co-produção e gestão** | Briefings, conceitos, letras e traduções de referência, decisões editoriais, provas, candidatos, rejeitados, históricos, RAG, agentes, workflows, campanhas, mídias sociais, relações públicas, administração, jurídico, contratos, manifests e referências canônicas de desenvolvimento |
| `Nexus-HUB57/khairus_KTD` | **Entrega audiovisual finalizada** | Masters de áudio aprovados, imagens finais aprovadas, vídeos finais/aprovados para entrega e seus manifests técnicos de checksum, versão e proveniência |

O segundo repositório não substitui a documentação de produção. Ele recebe somente o resultado audiovisual elegível para entrega ou arquivo final. O primeiro continua sendo o local onde decisões, critérios, versões candidatas, provas, rejeições, auditorias e regras operacionais são registrados.

## 2. Regra de status

Nenhum arquivo será migrado apenas porque existe ou contém `master`, `final`, `approved` ou `release` no nome. A elegibilidade depende de decisão humana ou registro editorial explícito no catálogo de assets e nos metadados da obra.

| Estado | KAIR-S-SONICA | khairus_KTD |
|---|---:|---:|
| `candidate` / `draft` | Sim | Não |
| `proof` / `trial` pendente | Sim | Não |
| `rejected` / `historical` | Sim, para auditoria | Não |
| Referência canônica de identidade ou desenvolvimento | Sim | Não, salvo cópia final expressamente aprovada |
| `approved final` / `official distribution master` | Registro e proveniência | Sim |
| Arquivo de entrega derivado de um final aprovado | Registro da relação | Sim, se o derivado estiver validado |

O status de uma faixa ou vídeo deve ser conferido no documento de aprovação correspondente. A Prova 2 do Single 11 permanece no repositório de produção porque ainda está pendente de avaliação humana. O mesmo vale para quaisquer candidatos, demos, stems, beds, takes, previews ou variantes de comparação.

## 3. Estrutura obrigatória do repositório audiovisual

```text
khairus_KTD/
├── README.md
├── MANIFEST.json
├── audio/
│   ├── singles/<single-slug>/master/
│   └── archive-approved/<single-slug>/
├── video/
│   ├── singles/<single-slug>/final/
│   ├── shorts/<single-slug>/approved/
│   └── archive-approved/<single-slug>/
├── images/
│   ├── singles/<single-slug>/final/
│   └── artist/final/
└── checksums/
    └── SHA256SUMS
```

Masters WAV e arquivos de vídeo grandes devem usar Git LFS no repositório audiovisual. MP3, PNG/JPEG e manifests podem usar Git normal quando estiverem dentro dos limites operacionais do GitHub. O `.gitattributes` deve ser versionado antes do primeiro lote grande.

## 4. Primeiro lote elegível

A migração inicial é deliberadamente conservadora e inclui somente arquivos com aprovação ou status oficial inequívoco:

| Obra | Arquivo audiovisual | Status | Ação |
|---|---|---|---|
| `SIX NAMES` | Master WAV/MP3 `ktd-second-single-six-names-rebuilt-soul-pre-release-v2` | Aprovado humanamente em definitivo | Migrar |
| `GOLDEN SCARS` | Master WAV/MP3 `ktd-third-single-golden-scars-trend-pre-release-v1` | Aprovado humanamente em definitivo | Migrar |
| `PRESSURE SPEAKS` | Master WAV/MP3 `pressure-speaks-ktd-essence-v1-master` | Aprovado — “MAGNÍFICO” | Migrar |
| `NO MORE QUIET CRIES` | Master WAV/MP3 `single_5_no_more_quiet_cries_v1-master` | Aprovado — “EXTRAORDINÁRIA” | Migrar |
| `FIRE IN THE FLOOD` | Master WAV/MP3 `...reference-aligned-mix-v4` | Master oficial de distribuição | Migrar |
| `FIRE IN THE FLOOD` | Teaser vertical aprovado `fire-in-the-flood-ktd-approved-dynamic-8s` | Aprovado em workflow | Migrar |
| `GOLDEN SCARS` | Peça `golden-scars-v1-frame-the-whole-picture` | Oficial / peça da faixa | Migrar |
| `UNLEASH THE DRAGON` | Clipe 1 `...dressing-room-10s-with-audio` | Aprovado em workflow, mux definitivo do clipe 1 | Migrar como clipe aprovado, não como videoclipe completo |

O primeiro lote não inclui imagens porque as imagens encontradas são principalmente âncoras de identidade, keyframes ou referências de desenvolvimento. Elas permanecem em `KAIR-S-SONICA` até existir uma aprovação explícita como arte final de entrega.

Também não migra a Prova 8 Funk, a Prova 2 Old School do Single 11, as versões dos Singles 6–9 cujo status não identifica um master final de distribuição, nem qualquer arquivo reprovado, experimental ou pendente.

## 5. Regra de duplicação e remoção

Durante a transição, o arquivo original permanece no repositório de produção para preservar rastreabilidade e permitir revisão. O manifest do segundo repositório deve registrar o path original, o SHA-256, o status, a decisão de aprovação e a data da cópia.

Somente após a verificação de hash, confirmação de que o arquivo foi publicado no segundo repositório e atualização de todas as referências, poderá ser aberta uma alteração separada para transformar uma cópia antiga em ponte histórica ou removê-la. Nenhuma remoção será feita automaticamente nesta primeira migração.

Cópias duplicadas em `personas/artist-principal/media` não são fontes de verdade. Elas devem ser tratadas como bundle derivado; não se deve migrar a partir delas quando existir o path canônico em `assets/` ou `outputs/`.

## 6. Referências cruzadas

O `KAIR-S-SONICA` deve apontar para os arquivos finalizados por meio do repositório audiovisual, do path relativo no manifest e do commit de migração. O `khairus_KTD` deve apontar de volta para o documento de aprovação e para o path de origem, sem incorporar documentos internos desnecessários, dados pessoais, credenciais ou arquivos candidatos.

A publicação social deve consumir somente assets cujo manifest no repositório audiovisual indique `approved final` ou `official distribution master`. O Social Orchestrator não deve publicar arquivos a partir de `outputs/`, `proofs/`, `trials/` ou `promos/` do repositório de produção sem uma entrada final aprovada no manifest audiovisual.

## 7. Segurança e governança

Nenhum token OAuth, App Secret, Client Secret, refresh token, arquivo `.env`, credencial administrativa ou dado privado de fãs será transferido para qualquer um dos repositórios. O repositório audiovisual pode ser público ou privado conforme decisão do titular, mas a visibilidade não altera a obrigação de retirar secrets.

Para cada novo arquivo audiovisual final, registrar título, single/campanha, tipo, status, versão pública, codec, resolução ou sample rate, duração, SHA-256, origem, aprovação, data, créditos e relação com o arquivo de produção. O commit que adiciona o arquivo deve ser reproduzível e não deve substituir silenciosamente um master existente.

## 8. Procedimento de cada lote

1. Auditar o catálogo e os metadados de aprovação no `KAIR-S-SONICA`.
2. Selecionar apenas paths canônicos e calcular SHA-256 antes da cópia.
3. Copiar para o diretório semântico do `khairus_KTD`, usando Git LFS quando aplicável.
4. Gerar ou atualizar `MANIFEST.json` e `checksums/SHA256SUMS`.
5. Validar formato, tamanho, hash e ausência de secrets.
6. Commitar e enviar o segundo repositório sem sobrescrever commits remotos.
7. Registrar no `KAIR-S-SONICA` o mapa de migração e o commit de destino.
8. Somente depois avaliar a remoção ou marcação histórica das cópias antigas.

Esta diretriz é compatível com o catálogo de assets existente em `docs/ktd-asset-catalog.md`, com o inventário técnico em `data/ktd/asset-inventory.json` e com os registros de aprovação de cada single. Quando houver conflito entre nome de arquivo e decisão editorial, a decisão editorial prevalece.
