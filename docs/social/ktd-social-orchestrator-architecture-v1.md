# KTD Social Orchestrator — arquitetura híbrida v1

**Projeto:** KAIR-S-SONICA
**Canais-alvo:** Instagram `@khairusktd_ofc` e TikTok `@ktd_oficial`
**Modo:** autonomia híbrida, com execução independente e colaboração opcional com agentes peer/Káiros
**Status:** arquitetura base para implementação

## 1. Objetivo

O KTD Social Orchestrator será o diretor de operações digitais de Kháirus the Dragon. Ele deverá transformar objetivos artísticos e comerciais em campanhas executáveis, produzir pacotes por plataforma, agendar e publicar quando as integrações estiverem autorizadas, acompanhar comentários e mensagens dentro dos limites das APIs, medir resultados, atualizar a memória do projeto e decidir a próxima ação com base em evidência.

O agente não será um gerador indiscriminado de posts. Ele funcionará como uma máquina de decisão com contratos: cada ação recebe contexto, hipótese, risco, evidência, custo, estado e resultado. A autonomia será permitida por política; ações de maior risco poderão ser encaminhadas a um agente peer, ao núcleo Káiros ou a uma aprovação opcional.

## 2. Princípios de operação

| Princípio | Implementação |
|---|---|
| Identidade antes de alcance | Recuperar a bíblia visual, física e musical de KTD antes de criar qualquer copy, roteiro ou asset. |
| Autonomia com limites | Classificar cada ação por risco, confiança, reversibilidade e necessidade de consentimento. |
| Uma fonte de verdade | Manter planos, decisões, assets, resultados e versões no repositório e na memória do projeto. |
| Publicação explícita | Não publicar por acidente; cada publicação recebe `idempotency_key`, validação técnica e registro. |
| LLM como julgamento assistido | O modelo propõe, classifica e explica; código determinístico valida esquema, direitos, formato, frequência e políticas. |
| Aprendizado auditável | Registrar hipótese, ação, métrica e decisão seguinte; não declarar viralização ou causalidade sem evidência. |
| Privacidade e dignidade | Não explorar trauma, crise, autoagressão, violência atual, dados pessoais ou relatos de terceiros para obter alcance. |
| Originalidade | Não imitar artistas reais, vozes, músicas, samples, melodias ou arranjos reconhecíveis. |

## 3. Camadas do sistema

```text
Briefing / evento / métrica
        ↓
Policy Guard + Consent & Safety Gate
        ↓
RAG Router → memória de projeto, cânone, campanhas, assets, histórico e APIs
        ↓
Planner Orchestrator
        ├─ Strategy Agent
        ├─ Audience & PR Agent
        ├─ Trend/Research Agent
        ├─ Copy & Localization Agent
        ├─ Creative Package Agent
        ├─ Platform Adaptation Agent
        ├─ Community Agent
        ├─ Analytics & Experiment Agent
        └─ Peer Delegation Agent
        ↓
Contract Validator + Media QA + Rate Limit Guard
        ↓
Action Router
        ├─ simulate / draft
        ├─ schedule
        ├─ publish Instagram
        ├─ publish TikTok
        ├─ reply / moderate
        └─ escalate to peer or optional human approval
        ↓
Webhook / polling status + metrics ingestion
        ↓
Memory, report, next-best-action
```

## 4. Agentes e responsabilidades

| Agente | Função | Saída contratual |
|---|---|---|
| `orchestrator` | Coordena o ciclo, prioridades, dependências e estado | `SocialRunResult` |
| `brand_guardian` | Protege identidade física, visual, musical, verbal e narrativa de KTD | `BrandReview` |
| `strategy` | Define objetivo, público, funil, hipótese e janela | `CampaignPlan` |
| `research_rag` | Recupera fontes, tendências, histórico e proveniência | `EvidencePack` |
| `audience_pr` | Segmenta públicos, mapeia relações e identifica riscos reputacionais | `AudienceMap`, `PRRiskReview` |
| `copywriter` | Cria captions, hooks, perguntas, CTAs e respostas | `CopyPackage` |
| `creative_director` | Gera briefing para vídeo, imagem, carrossel e live action | `CreativeBrief` |
| `platform_adapter` | Ajusta duração, proporção, hashtags, CTA, texto e publicação por canal | `PlatformPackage` |
| `community_manager` | Classifica comentários, propõe respostas e encaminha casos sensíveis | `CommunityQueue` |
| `analytics` | Ingere métricas, compara hipóteses e identifica próximos testes | `ExperimentReport` |
| `moderation_safety` | Detecta risco, doxxing, discurso de ódio, crise e manipulação | `SafetyDecision` |
| `peer_delegate` | Convoca agentes especializados e reconcilia resultados | `PeerHandoff` |
| `qa_delivery` | Valida asset, metadata, direitos, idempotência e logs | `ReleaseGate` |

O núcleo agentic atual de 12 papéis continuará sendo reutilizado. O módulo social acrescentará papéis de domínio sem duplicar o mecanismo de handoffs e sem remover o gate existente.

## 5. Matriz de autonomia

A autonomia será determinada por quatro dimensões: **risco**, **confiança do resultado**, **reversibilidade** e **dependência de consentimento externo**.

| Ação | Padrão v1 | Escalonamento |
|---|---|---|
| Rascunhar caption, hashtags e variações | Autônoma | Peer se a confiança ficar abaixo do limiar |
| Criar calendário e testes A/B | Autônoma | Peer se houver conflito entre campanhas |
| Gerar roteiro ou prompt de asset | Autônoma | Bloquear se violar cânone de KTD |
| Publicar asset aprovado pelo QA | Autônoma, quando credenciais e política permitirem | Peer/humano opcional para campanha de alto risco |
| Responder comentário positivo ou pergunta factual | Autônoma com templates e limites | Peer se houver ambiguidade |
| Responder relato de trauma, crise, autoagressão ou violência | Não autônoma | Encaminhar a protocolo de segurança; nunca transformar em marketing |
| Excluir, ocultar ou denunciar conteúdo | Autônoma apenas em regras determinísticas | Peer/humano para casos ambíguos |
| Enviar DM proativa | Desativada por padrão | Exige política explícita e consentimento aplicável |
| Alterar posicionamento público ou fazer declaração de crise | Não autônoma | Escalonar para PR peer e aprovação opcional |
| Comprar mídia ou aceitar parceria | Desativada | Exige confirmação explícita e orçamento definido |

O fato de a publicação ser autônoma não elimina os gates técnicos. O sistema deve registrar o motivo da ação, o conteúdo exato, o asset, a versão, a política aplicada e o retorno da plataforma.

## 6. RAG e memória

O RAG será híbrido. A primeira camada será um índice local, reproduzível e versionado, alimentado por Markdown, YAML, JSON, transcrições, manifests e hashes dos assets. A segunda camada será uma memória operacional com decisões, resultados, comentários anonimizados e métricas. A terceira camada será recuperação externa apenas quando a fonte estiver autorizada e houver registro de URL, data, escopo e licença.

### Coleções obrigatórias

| Coleção | Exemplos de conteúdo | Regra |
|---|---|---|
| `ktd_canon` | `ktd-visual-bible`, especificação física, persona, mapa de tattoos | Sempre consultar antes de imagem ou vídeo |
| `music_catalog` | singles, letras aprovadas, provas pendentes, BPM, status | Nunca tratar prova pendente como release final |
| `campaigns` | Modelo A→B, TikTok, Instagram, YouTube, calendário | Respeitar estágio e canal |
| `assets` | hashes, formatos, aprovação, direitos, referências | Bloquear asset sem proveniência |
| `platform_policies` | limites e capabilities das APIs | Atualizar antes de alterar adapters |
| `community_memory` | comentários classificados, consentimentos e respostas | Minimizar dados e anonimizar |
| `analytics` | snapshots, hipóteses, testes e decisões | Separar correlação de causalidade |

A busca deverá combinar lexical/BM25, filtros por metadado e embeddings quando uma implementação vetorial estiver habilitada. Todo resultado terá `source_id`, `path_or_url`, `version`, `retrieved_at`, `confidence` e `provenance`.

## 7. LLM routing

O catálogo live consultado em 22 de agosto de 2026 disponibiliza modelos GPT, Claude e Gemini com ferramentas, visão e saída estruturada. O orquestrador não deve fixar um modelo sem consultar o catálogo na inicialização ou no deploy.

| Tarefa | Rota inicial | Política |
|---|---|---|
| Classificação, tagging, extração e variações em volume | modelo econômico de baixa latência | Saída JSON estrita e validação determinística |
| Copy, estratégia e relações públicas | modelo de raciocínio intermediário | Recuperação de contexto obrigatório |
| Avaliação de risco, crise e reconciliação de peers | modelo forte com reasoning | Nunca executar ação sensível apenas pela pontuação do LLM |
| Análise multimodal de asset | modelo com visão | Comparar com referências canônicas e registrar evidência |

O código usará `response_format` com JSON Schema estrito. Para famílias GPT será usado `max_completion_tokens` quando houver reasoning; para Claude e Gemini serão respeitadas as diferenças de parâmetros do catálogo live. Falhas serão tratadas com retry limitado, fallback de modelo e bloqueio seguro.

## 8. Integrações oficiais

### Instagram

A publicação será implementada via Instagram Platform para conta profissional. O fluxo cria um container em `/<IG_ID>/media`, aguarda status quando necessário e publica com `/<IG_ID>/media_publish`. A mídia precisa estar em servidor publicamente acessível no momento da tentativa. A documentação atual também descreve comentários, respostas, ocultação/exclusão e webhooks `comments`/`live_comments`, além de insights de conta e mídia [1] [2].

O adapter deverá consultar o limite de publicação antes de agendar e usar fila com idempotência. A documentação atual informa limite de 100 posts publicados via API em janela móvel de 24 horas no guia de Content Publishing e 50 no endpoint `media_publish`; por segurança, o sistema deve buscar o limite/capability efetivo da versão configurada, aplicar o menor limite documentado e não assumir que a plataforma aceitará volume elevado [1] [3].

### TikTok

A publicação direta será implementada pelo Content Posting API. O fluxo consulta informações do criador, inicializa `/v2/post/publish/video/init/`, envia arquivo ou URL pública verificada e acompanha `/v2/post/publish/status/fetch/`. O escopo `video.publish`, a autorização do usuário e a aprovação do app são necessários. Clientes não auditados ficam restritos a conteúdo privado, conforme a documentação oficial [4] [5].

O adapter deverá preferir webhooks de status `post.publish.*` quando configurados, validar `TikTok-Signature` com HMAC-SHA256 e manter polling como fallback. A API tem limite documentado de seis inicializações por minuto por access token e trinta consultas de status por minuto; o rate limiter deve ficar abaixo desses limites [5] [6].

A análise e resposta de comentários do TikTok não deve ser presumida como uma capability normal de gerenciamento. A documentação pública encontrada para comentários pertence ao Research API, exige `research.data.basic` e é destinada a acesso de pesquisa; portanto, a v1 deverá tratar comentários TikTok como ingestão somente quando uma capability oficialmente autorizada estiver configurada, sem inventar um endpoint de resposta [7].

## 9. Peer-to-peer

O `peer_delegate` usará handoffs com contrato, não chamadas livres. Cada peer recebe apenas o contexto mínimo necessário e devolve `result`, `evidence`, `confidence`, `risks`, `recommended_action` e `expires_at`. O orquestrador reconcilia respostas por prioridade de fonte, confiança e compatibilidade com o cânone.

Casos de peer: estratégia e PR; análise de tendência; copy em inglês; copy PT-BR de referência; QA visual; segurança/moderação; métricas; produção audiovisual. O peer nunca pode contornar os gates da plataforma ou as políticas de segurança.

## 10. Operação e observabilidade

Cada ação terá `run_id`, `campaign_id`, `platform`, `content_id`, `asset_hash`, `policy_version`, `idempotency_key`, `created_at`, `actor`, `decision`, `status` e `error_code`. Tokens, secrets, URLs assinadas e conteúdo privado nunca entram em logs.

O sistema deverá expor saúde do serviço, estado das filas, idade do último snapshot, falhas por endpoint, latência, retries, taxa de publicação, conversão por CTA, comentários pendentes e ações bloqueadas por segurança. Relatórios devem separar métricas observadas de interpretações do LLM.

## 11. Implantação em duas etapas

**Etapa 1 — núcleo seguro:** módulo social, contratos, RAG local, LLM router, simuladores, calendário, QA, memória, relatórios e adapters sem credenciais. Essa etapa pode ser executada localmente no repositório e validada por testes.

**Etapa 2 — operação autônoma:** serviço persistente, secrets server-side, OAuth/Business Login, webhooks, publicação real, status, comentários e insights. A execução deve ocorrer em ambiente persistente; o sandbox padrão não é adequado para manter processos online. WebDev é a opção gerenciada padrão; uma máquina persistente só será necessária se houver dependência de Docker, ferramentas de sistema ou recursos que ultrapassem os limites do ambiente gerenciado.

## 12. Próximo contrato de implementação

```text
SocialRunRequest
  objective: string
  campaign_id: string
  platforms: [instagram, tiktok]
  autonomy_mode: autonomous | collaborative | simulate
  peer_mode: disabled | optional | required
  content_intent: launch | evergreen | community | pr | analytics
  asset_refs: [AssetRef]
  source_refs: [SourceRef]
  schedule: ScheduleSpec | null

SocialRunResult
  run_id: string
  status: DRAFT | READY | SCHEDULED | PUBLISHED | PARTIAL | BLOCKED
  decisions: [DecisionRecord]
  platform_packages: [PlatformPackage]
  actions: [ActionRecord]
  escalations: [PeerHandoff]
  metrics_plan: MetricsPlan
  memory_writes: [MemoryWrite]
```

## Referências oficiais

[1]: https://developers.facebook.com/docs/instagram-api/guides/content-publishing — Meta for Developers, “Content Publishing”.

[2]: https://developers.facebook.com/docs/instagram-api/guides/comment-moderation — Meta for Developers, “Comment Moderation”.

[3]: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media_publish/ — Meta for Developers, “IG User Media Publish”.

[4]: https://developers.tiktok.com/doc/content-posting-api-get-started — TikTok for Developers, “Get Started — Direct Post”.

[5]: https://developers.tiktok.com/doc/content-posting-api-reference-direct-post — TikTok for Developers, “Direct Post”.

[6]: https://developers.tiktok.com/doc/content-posting-api-reference-get-video-status — TikTok for Developers, “Get Post Status”.

[7]: https://developers.tiktok.com/doc/research-api-specs-query-video-comments — TikTok for Developers, “Query Video Comments”.
