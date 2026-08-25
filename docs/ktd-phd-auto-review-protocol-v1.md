# Protocolo PHD de Auto-Review e Auto-Reprovação Audiovisual — Kháirus

**Versão:** 1.0.0  
**Estado:** aplicado no gateway e no StudioMaster  
**Escopo:** solicitações de áudio, multimídia, vídeo e preflight de imagem  
**Princípio:** nenhuma solicitação de produção entra no worker sem passar pelo gate determinístico de **Preflight, Handoff e Determinism — PHD**.

## 1. Objetivo operacional

O Auto-Review transforma cada solicitação em um objeto auditável antes de iniciar geração, gravação processada, edição ou entrega. O motor compara a solicitação com o cânone de Kháirus, registra findings, cria um roadmap de correção e aplica somente normalizações técnicas seguras. Ele não substitui a decisão artística humana, não reescreve identidade, não baixa modelos, não publica materiais e não altera assets existentes.

A política é deliberadamente conservadora: uma divergência explícita de artista, voz, identidade física, tatuagens ou política audiovisual de live-action resulta em **REJECTED**. A ausência de alguns metadados técnicos pode receber reparo automático rastreável, mas a aprovação final, a proveniência e a publicação continuam humanas.

> **Regra de produção:** `READY_FOR_APPROVAL` significa que o pedido passou pelo hard gate e pode ser encaminhado ao próximo estágio técnico. Não significa aprovação artística final nem autorização de publicação.

## 2. Âncoras canônicas imutáveis

| Área | Âncora aplicada | Regra |
|---|---|---|
| Artista | `kairos.khairus_the_dragon` | Outro `artist_id` bloqueia o pedido; ausência pode ser normalizada para o projeto Kháirus. |
| Perfil físico | `ktd-physical-spec-v1` | Não pode ser substituído por outro perfil. |
| Tatuagens | `dragon-diamond-v1` | O mapa canônico deve permanecer intacto e contínuo. |
| Perfil visual | `ktd-visual-canon-v1` | Atributos de identidade não podem ser improvisados. |
| Voz | `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3` | Timbre, sotaque, articulação, registro e assinatura vocal permanecem vinculados à referência oficial. |
| Vídeo | `live-action-only-no-static-no-overlay` | Não aceita slideshow, still, foto com pan/zoom, imagem estática ou imagem sobreposta em live-action. |

Qualquer solicitação que inclua `identity_modification_requested`, `modify_identity`, `voice_identity_override` ou `voice_clone` como verdadeiro é bloqueada e encaminhada para autorização humana. O motor não tenta “corrigir” uma modificação de identidade, pois isso ocultaria uma decisão artística e de consentimento.

## 3. Fluxo obrigatório

```text
Solicitação
   ↓
Auto-Review determinístico
   ├── Identidade, físico e tatuagens
   ├── Voz e assinatura de performance
   ├── Política de vídeo e movimento real
   ├── Proveniência, direitos e consentimento
   └── Normalização técnica segura
   ↓
REJECTED ──→ roadmap P0/P1 ──→ correção humana ou nova submissão
   │
   └── READY_FOR_APPROVAL ──→ handoff explícito ──→ worker
                                      ↓
                              QA + aprovação KTD
                                      ↓
                          entrega/publicação separada
```

A auditoria é persistida de forma atômica em `data/studio-master/preflight/<audit_id>.json`, configurável por `KAIROS_STUDIO_MASTER_PREFLIGHT_DIR`. A persistência é auxiliar: se o diretório não puder ser escrito, a decisão HTTP ainda é devolvida, mas a equipe deve corrigir a infraestrutura antes de considerar o lote pronto para lançamento.

## 4. Decisões e severidade

| Estado | Significado | Ação |
|---|---|---|
| `READY_FOR_APPROVAL` | Nenhum blocker foi encontrado. | Pode seguir para o estágio técnico seguinte, mantendo aprovação humana final. |
| `REJECTED` | Pelo menos um blocker de identidade, voz ou política audiovisual foi encontrado. | Não enfileirar; corrigir conforme roadmap e submeter novamente. |
| `PASS` | Regra satisfeita ou normalização segura realizada. | Registrar no relatório da auditoria. |
| `FLAGGED` | Informação incompleta ou risco não fatal. | Completar antes da aprovação final. |
| `BLOCKED` | Regra crítica falhou. | Interromper imediatamente. |

Os códigos críticos principais são `ID-LOCK-02` para artista divergente, `ID-*` para perfil físico/tatuagem/visual divergente, `IMG-IMMUTABLE-01` para modificação da identidade, `AUD-VOICE-01` para referência vocal divergente, `AUD-VOICE-02` para override/clonagem vocal e `VID-POLICY-01` para still, imagem estática, overlay ou movimento falso.

## 5. Reparos automáticos permitidos

Os reparos abaixo são determinísticos, ficam listados em `repairs_applied` e não mudam o conteúdo criativo essencial do prompt.

| Reparo | Quando ocorre | Limite |
|---|---|---|
| `identity-lock-artist-id` | `artist_id` ausente em um projeto Kháirus. | Não substitui explicitamente outro artista. |
| `identity-physical-profile`, `identity-tattoo-map`, `identity-visual-profile` | Âncoras não foram declaradas. | Divergência explícita continua bloqueada. |
| `audio-lock-reference` | A referência vocal não foi declarada. | Referência divergente ou override é blocker. |
| `video-live-action-constraint` | O brief não declara ação física e continuidade suficientes. | Não converte imagem estática em vídeo; termos proibidos bloqueiam. |
| metadados técnicos | Perfil de vídeo recebe defaults de 24 fps, 9:16 e revisão por frame. | Valores criativos fora do schema continuam sujeitos ao contrato da API. |

O modo `auto_repair=false` faz uma auditoria sem mutar o payload. Esse modo é útil para revisão cirúrgica e comparação de mudanças antes do envio.

## 6. Gates por mídia

### 6.1 Imagens

Toda solicitação de imagem deve declarar o perfil físico, o mapa de tatuagens e a identidade visual canônica. A auditoria aceita apenas continuidade integral dos atributos. Não há reparo automático para mudança de rosto, cabeça, barba, heterocromia, anatomia, tatuagens, roupa identitária ou qualquer outro marcador físico. Esses casos exigem aprovação prévia de KTD e nova submissão.

### 6.2 Vídeos

Os briefs devem descrever performance live-action, ação física observável, câmera contínua motivada, reação temporal do cenário e revisão de frames. São proibidos stills, slideshow, foto com pan/zoom, “foto animada”, imagem sobreposta e qualquer tentativa de substituir filmagem real por movimento cosmético. O worker não deve ser chamado quando `VID-POLICY-01` estiver presente.

### 6.3 Áudios e voz

Toda solicitação de voz deve permanecer vinculada à referência oficial, ao perfil `medium-low-front-clear-controlled-aggression` e ao padrão de performance `syncopated-double-time-half-time`. O Auto-Review pode registrar esses metadados quando ausentes, mas não faz conversão de timbre, sotaque ou identidade. A aprovação final da tomada, mix e master continua com o produtor e KTD.

### 6.4 Proveniência e aprovação

A ausência de `source_manifest` produz `GOV-MANIFEST-01` e um item P1 no roadmap. Esse warning não libera publicação: origem, licença, consentimento, versão e hash devem estar completos antes da entrega. A decisão final de publicação permanece separada do worker e do Auto-Review.

## 7. Contratos HTTP

### Auditoria manual

`POST /v1/studio-master/preflight`

```json
{
  "media_kind": "video",
  "auto_repair": true,
  "payload": {
    "artist_id": "kairos.khairus_the_dragon",
    "prompt": "Kháirus performs in a continuous live-action night scene",
    "source_manifest": "manifest/project-001.json"
  }
}
```

A resposta contém `audit_id`, `decision`, `hard_gate_passed`, `identity_lock`, `findings`, `roadmap`, `normalized_payload`, `repairs_applied`, `final_approval_required` e `auto_publish=false`.

### Rotas protegidas

O gate é executado antes de enfileirar `/v1/generate`, `/v1/orchestrate`, `/v1/video/generate`, `/v1/studio/handoff` e antes de construir o plano de `/v1/plan`. Quando bloqueado, o gateway devolve HTTP 422 com `detail.code= AUTO_REVIEW_BLOCKED` e o relatório completo da auditoria. Quando aprovado, as respostas de tarefa incluem `preflight_id`, `preflight_decision` e `repairs_applied`.

## 8. Operação no StudioMaster

O painel **AUTO-REVIEW / PHD GATE** aparece acima dos compositores. Depois de cada solicitação, ele mostra o ID da auditoria, a decisão, a quantidade de reparos e os principais findings e itens do roadmap. O operador deve tratar `BLOQUEADO` como parada de produção, não como sugestão estética.

A configuração padrão é ativa:

```dotenv
KAIROS_STUDIO_MASTER_AUTO_REVIEW_ENABLED=true
KAIROS_STUDIO_MASTER_PREFLIGHT_DIR=data/studio-master/preflight
```

A flag pode ser desligada apenas para diagnóstico controlado. Não é recomendável desativá-la em produção, porque as rotas de geração deixam de receber a barreira anterior ao worker.

## 9. Critérios de aceite

Uma solicitação só deve ser considerada apta quando o relatório apresenta `hard_gate_passed=true`, ausência de findings `BLOCKER`, identidade canônica íntegra, referência vocal oficial, brief de vídeo compatível quando aplicável, manifesto de origem preenchido, consentimento verificável e aprovação humana registrada. Mesmo nesse estado, `auto_publish` deve permanecer `false`.

O conjunto de regressão cobre normalização de áudio, divergência vocal, alteração de identidade, vídeo estático/overlay, reparo do brief live-action, modo audit-only, endpoint de preflight e bloqueio de geração para outro artista.

## 10. Fontes canônicas internas

1. `docs/ktd-phd-audiovisual-production-protocol-v1.md`
2. `docs/artist-principal.md`
3. `docs/ktd-physical-spec.md`
4. `docs/kairos-vocal-references.md`
5. `docs/ktd-vocal-approval.md`
6. `docs/song1-audiovisual-quality-protocol-v3.md`
7. `docs/ktd-approved-reference-audit-v2.md`
8. `packages/kairos_core/studio_master/frontier.py`
9. `packages/kairos_core/studio_master/perceptual_validator.py`
