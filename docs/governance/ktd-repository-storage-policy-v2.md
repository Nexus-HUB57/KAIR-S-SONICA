# KTD — Diretriz de armazenamento entre repositórios v2

**Data de vigência:** 22 de agosto de 2026
**Substitui:** `ktd-repository-storage-policy-v1.md`

## 1. Decisão de autoridade

O ecossistema KTD possui duas fontes de verdade complementares. A separação é por função e por estágio editorial, não por uma exclusão absoluta de documentos relacionados às obras.

| Repositório | Autoridade | Conteúdo principal |
|---|---|---|
| `Nexus-HUB57/KAIR-S-SONICA` | **Produção, co-produção, gestão e processo** | Briefings, conceitos, produção musical e audiovisual, provas, candidatos, rejeitados, históricos, decisões editoriais, RAG, agentes, workflows, gestão de mídias sociais, relações públicas, contatos, contratos, assuntos administrativos e jurídicos, campanhas em desenvolvimento e referências canônicas |
| `Nexus-HUB57/khairus_KTD` | **Entrega audiovisual e pacote operacional de marketing diretamente vinculado às obras** | Masters audiovisuais, imagens e vídeos aprovados, letras originais em inglês, traduções PT-BR de referência, versões e matriz de controle de letras, roteiros/storyboards aprovados para uma obra, captions, hashtags, thumbnails, metadata, press kits e demais materiais diretamente relacionados a uma produção audiovisual ou campanha de marketing |

O `KAIR-S-SONICA` permanece como a autoridade do processo de criação e das decisões. O `khairus_KTD` passa a ser a autoridade do pacote de entrega e ativação de cada obra: mídia final, texto oficial associado, tradução de referência e materiais de marketing vinculados.

## 2. Regra de inclusão por vínculo

Um arquivo pode entrar no `khairus_KTD` quando cumprir simultaneamente estes critérios:

1. estiver diretamente vinculado a um single, videoclipe, short, peça ou campanha identificada;
2. possuir fonte, versão e proveniência registradas;
3. ter status editorial claro (`approved`, `released`, `campaign_ready` ou equivalente);
4. não conter secrets, dados privados, contratos, informações administrativas internas ou dados pessoais de fãs;
5. não substituir silenciosamente outra versão.

Letras e traduções podem ser armazenadas no repositório audiovisual mesmo quando o áudio ou vídeo final correspondente ainda estiver em campanha, desde que o estado do texto esteja explicitamente registrado. A matriz deve distinguir `approved_official`, `reference_translation`, `candidate`, `campaign_ready` e `archived`.

## 3. Estados editoriais

| Estado | `KAIR-S-SONICA` | `khairus_KTD` |
|---|---:|---:|
| `draft` / `candidate` de produção | Sim | Não, salvo workpack de campanha explicitamente marcado e sem publicação automática |
| `proof` / `trial` pendente | Sim | Não, exceto material de campanha que tenha sido aprovado separadamente como campanha |
| `rejected` / `historical` | Sim, para auditoria | Não, salvo registro histórico mínimo sem o asset rejeitado |
| Letra inglesa oficial aprovada | Registro de origem | Sim, vinculada à obra |
| Tradução PT-BR de referência | Registro de origem | Sim, vinculada à versão inglesa e marcada como não oficial |
| Material de marketing `campaign_ready` | Registro do processo | Sim |
| Master audiovisual final ou oficial de distribuição | Proveniência e decisão | Sim |
| Secret, token, contrato privado, dado de fã | Não | Não |

Uma tradução PT-BR nunca se torna composição oficial apenas por ser copiada para o repositório audiovisual. A composição oficial permanece no idioma inglês, salvo decisão editorial expressa em sentido contrário.

## 4. Estrutura obrigatória do `khairus_KTD`

```text
khairus_KTD/
├── README.md
├── MANIFEST.json
├── LYRICS_TRANSLATIONS_MATRIX.json
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
├── lyrics/
│   └── singles/<single-slug>/
│       ├── original-en/
│       ├── pt-BR-reference/
│       └── reviews/
├── campaigns/
│   └── <single-slug>/
│       ├── common/
│       ├── instagram/
│       ├── tiktok/
│       └── youtube/
└── checksums/
    └── SHA256SUMS
```

As letras originais e as traduções devem permanecer em diretórios separados. O nome do arquivo deve conter idioma, título, versão e natureza editorial quando necessário, por exemplo `lyrics-original-en-v1.md` e `lyrics-pt-br-reference-v1.md`.

## 5. Matriz central de versões

`LYRICS_TRANSLATIONS_MATRIX.json` é a matriz operacional central do repositório audiovisual. Cada registro deve conter, no mínimo:

| Campo | Função |
|---|---|
| `record_id` | Identificador estável do par ou documento |
| `single` / `title` | Vínculo com a obra |
| `language` | `en` ou `pt-BR` |
| `kind` | `original_lyric`, `reference_translation` ou outro tipo controlado |
| `version` | Versão textual |
| `status` | Estado editorial da fonte ou tradução |
| `path` | Path no `khairus_KTD` |
| `source_path` | Path de origem no `KAIR-S-SONICA` |
| `source_record` | Aprovação, brief ou documento de referência |
| `paired_record_id` | Registro correspondente no outro idioma |
| `review_status` | `reviewed`, `needs_editorial_decision` ou `not_reviewed` |
| `line_review_path` | Documento da auditoria linha a linha |
| `sha256` | Integridade do arquivo |
| `updated_at` | Data da última revisão |

A matriz deve apontar para o commit de origem e, quando possível, para o commit de destino. Alterações substanciais geram nova versão; correções de formatação ou de vínculo podem ser registradas em commit separado, sem apagar o histórico.

## 6. Campanhas de marketing

O `khairus_KTD` pode receber os materiais diretamente usados para ativar uma campanha: roteiros, storyboards aprovados, captions, hashtags, thumbnails, press copy, metadata, calendário de publicação, CTAs, versões por plataforma e relatórios de campanha. O `KAIR-S-SONICA` continua sendo a autoridade do planejamento estratégico, da gestão do orquestrador, dos experimentos, das decisões de risco, das credenciais, das integrações e dos históricos de desenvolvimento.

Um pacote de marketing não autoriza publicação por si só. O Social Orchestrator deve respeitar o status e os gates de publicação registrados no manifest e no workflow.

## 7. Migração, duplicação e remoção

A migração é inicialmente não destrutiva. O arquivo de origem permanece no `KAIR-S-SONICA` para preservar o processo, a proveniência e o rollback. O `khairus_KTD` recebe uma cópia organizada, com hash e referência cruzada.

A remoção de uma cópia antiga só pode ser aberta em alteração separada, depois de verificar hash, destino, links e funcionamento dos consumidores. Nenhuma remoção é automática. Bundles em `personas/` e outputs de prova não devem ser usados como fonte quando houver path canônico.

## 8. Segurança

Nenhum token OAuth, App Secret, Client Secret, refresh token, arquivo `.env`, credencial administrativa, contrato privado, dado de fã ou informação pessoal deve ser copiado para qualquer um dos repositórios. A configuração de publicação fica em secret managers, GitHub Environments ou variáveis de runtime.

## 9. Procedimento obrigatório por lote

1. Auditar a fonte e a aprovação no `KAIR-S-SONICA`.
2. Separar original inglês, tradução PT-BR e materiais de campanha por diretório.
3. Revisar estrutura e conteúdo; para letras, registrar a conferência linha a linha.
4. Calcular SHA-256 antes e depois da cópia.
5. Atualizar `MANIFEST.json`, `LYRICS_TRANSLATIONS_MATRIX.json` e checksums.
6. Validar links, idioma, status e ausência de secrets.
7. Commitar e enviar o `khairus_KTD` sem sobrescrever commits remotos.
8. Registrar o commit de destino no `KAIR-S-SONICA`.
9. Abrir eventual limpeza de duplicatas somente em alteração futura e explícita.

Quando houver conflito entre o nome do arquivo e a decisão editorial, a decisão editorial prevalece. Quando houver conflito entre uma tradução e a fonte inglesa, a fonte inglesa prevalece e a tradução deve ser corrigida ou marcada para decisão.
