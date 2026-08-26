# Protocolo de fallback cloud para vídeo — KTD v1

**Status:** implementado como adapter genérico, desabilitado por padrão e sem provider autorizado no ambiente atual. **Objetivo:** permitir uma submissão remota deliberada enquanto a GPU local não foi provisionada, sem mascarar indisponibilidade, degradar a qualidade ou alterar a identidade canônica de Kháirus.

## Decisão operacional

O pipeline local continua sendo a autoridade de produção. A ausência de GPU não ativa uma rota alternativa automaticamente: `POST /v1/video/generate` permanece exclusivamente local e pode falhar de modo explícito quando SkyReels não está pronto. O fallback remoto só pode ser acionado pela rota separada `POST /v1/video/cloud-submit`, com `confirm_cloud_submit=true`, `human_approved=true`, preflight PHD aprovado e configuração completa do provider.

O adapter genérico usa um contrato HTTP JSON fornecido pelo operador. Ele não escolhe serviço, não faz descoberta, não baixa modelos, não faz upload de referências por aproximação, não faz retry automático e não é chamado por `frontier/plan`, `preflight`, catálogo de agentes ou qualquer worker local.

## Estados do fallback

| Estado | Significado | Pode chamar provider? |
|---|---|---:|
| `DISABLED` | Flag global permanece falsa, que é o default do repositório. | Não |
| `NOT_CONFIGURED` | Flag pode estar ligada, mas provider ou `base_url` não foram definidos. | Não |
| `FALLBACK_ONLY` | Há provider/base URL, porém falta credencial, allowlist, aceite de licença, política de retenção ou limite de gasto válido. | Não |
| `READY` | Todos os gates técnicos e de governança estão satisfeitos. Ainda requer confirmação humana por request. | Somente pela rota explícita |

A capacidade exposta em `GET /v1/video/capabilities` mostra esse estado sem convertê-lo em backend padrão. O campo `default_backend` continua apontando para `native` somente quando a GPU local está realmente pronta; caso contrário, permanece `cli`, que falha explicitamente se não houver runtime. Isso impede fallback silencioso de baixa qualidade.

## Gates obrigatórios antes do upload

O preflight deve receber `media_kind=multimedia` e uma declaração de identidade/proveniência. A auditoria rejeita qualquer divergência do artista, perfil físico, mapa de tatuagens, perfil visual ou referência vocal canônica. Também bloqueia stills, imagem estática, slideshow, overlay, foto animada e pan/zoom sobre foto. O pedido precisa declarar ação física live-action contínua, movimento de câmera motivado, continuidade temporal e revisão de frames, conforme o protocolo de qualidade do Single 1 [1] [2].

A rota cloud também exige que o operador confirme os termos do provider, sua política de retenção e um limite positivo de gasto em centavos. A credencial é lida somente do nome de variável configurado em `KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY_ENV`; o valor nunca entra em arquivos, payloads de preflight, logs ou respostas HTTP. O adapter atual aceita apenas `t2v` sem caminhos de mídia. I2V, `extend` e `start_end` ficam bloqueados até existir um contrato aprovado de transferência e retenção de referências.

## Opções de infraestrutura ainda não escolhidas

Como nenhum provider cloud foi autorizado nesta sessão, a implementação não inventa endpoint nem cria conexão externa. As duas alternativas abaixo permanecem abertas para decisão do operador.

| Abordagem | Tradeoffs | Custo | Complexidade de configuração |
|---|---|---|---|
| API gerenciada de vídeo com contrato HTTP JSON | Menor tempo para começar e sem administrar GPU; exige validar política de retenção, licença do modelo, limites, custo por geração e compatibilidade com o contrato de vídeo live-action. | Variável por geração e armazenamento; deve ser limitado pelo orçamento configurado. | Média: provider, endpoint, allowlist, credencial e aceite documental. |
| GPU dedicada ou worker remoto controlado pela equipe | Maior controle sobre checkpoint, retenção, logs e qualidade; exige provisionamento, manutenção, segurança de rede e compatibilidade CUDA/driver. | Infraestrutura contínua mais custo operacional; depende do fornecedor escolhido. | Alta: máquina, runtime, modelo, observabilidade e manutenção. |

A alternativa mais leve é a primeira, mas não é automaticamente melhor: a aprovação deve considerar identidade e voz, jurisdição dos dados, exclusão de uploads, licença do checkpoint e orçamento antes de ligar a flag.

## Configuração segura

Os valores de exemplo estão em `.env.example`. O conjunto mínimo, após a decisão do provider, é equivalente a:

```dotenv
KAIROS_CLOUD_VIDEO_FALLBACK_ENABLED=false
KAIROS_CLOUD_VIDEO_FALLBACK_PROVIDER=NOT_CONFIGURED
KAIROS_CLOUD_VIDEO_FALLBACK_BASE_URL=
KAIROS_CLOUD_VIDEO_FALLBACK_SUBMIT_PATH=/v1/video/generations
KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY_ENV=KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY
KAIROS_CLOUD_VIDEO_FALLBACK_TIMEOUT_SECONDS=1800
KAIROS_CLOUD_VIDEO_FALLBACK_ALLOWED_PROVIDERS=
KAIROS_CLOUD_VIDEO_FALLBACK_LICENSE_ACKNOWLEDGED=false
KAIROS_CLOUD_VIDEO_FALLBACK_RETENTION_ACKNOWLEDGED=false
KAIROS_CLOUD_VIDEO_FALLBACK_SPENDING_LIMIT_CENTS=0
KAIROS_CLOUD_VIDEO_FALLBACK_MAX_UPLOAD_BYTES=104857600
```

O valor real de `KAIROS_CLOUD_VIDEO_FALLBACK_API_KEY` deve ser injetado no ambiente de execução, nunca commitado. A flag só deve ser alterada para `true` depois que um provider específico for escolhido e testado em ambiente controlado. Mesmo em `READY`, cada submissão exige confirmação humana; o estado pronto não equivale a autorização artística.

## Contrato de submissão

A requisição usa o seguinte formato conceitual:

```json
{
  "request": {
    "prompt": "one uninterrupted photorealistic live-action shot with physical action and continuous motivated camera",
    "mode": "t2v",
    "backend": "cli",
    "resolution": "720P",
    "fps": 24,
    "seed": 42
  },
  "identity_metadata": {
    "artist_id": "kairos.khairus_the_dragon",
    "physical_profile": "ktd-physical-spec-v1",
    "tattoo_map": "dragon-diamond-v1",
    "identity_profile": "ktd-visual-canon-v1",
    "voice_reference": "assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3",
    "aspect_ratio": "9:16",
    "source_manifest": {
      "path": "assets/video/aprovados/reference.mp4",
      "sha256": "<sha256>",
      "status": "APPROVED_REFERENCE",
      "license": "<approved-policy>",
      "consent": "<documented-policy>",
      "identity_reference": "ktd-visual-canon-v1"
    },
    "live_action_policy": "live-action-only-no-static-no-overlay",
    "static_image_only": false,
    "image_overlay": false,
    "render_request": true
  },
  "confirm_cloud_submit": true,
  "human_approved": true
}
```

O adapter acrescenta ao payload remoto apenas o `preflight_id`, a decisão `READY_FOR_APPROVAL` e os guardrails de governança. Não envia o segredo como campo JSON. Respostas remotas são normalizadas para `remote_task_id`; o sistema não trata a submissão como aprovação final nem publica o resultado automaticamente.

## Verificação e rollback

A validação local deve cobrir `GET /v1/video/capabilities`, o estado do fallback e uma submissão simulada contra um servidor de teste, sem enviar um take real. Para bloquear novamente a integração, basta retornar `KAIROS_CLOUD_VIDEO_FALLBACK_ENABLED=false`, remover o provider da allowlist e retirar a credencial do ambiente. Nenhuma saída local, asset aprovado, manifesto ou histórico Git é sobrescrito pelo adapter.

## Referências

[1]: ./song1-audiovisual-quality-protocol-v3.md "Protocolo de qualidade audiovisual do Single 1"
[2]: ./ktd-approved-reference-audit-v2.md "Auditoria de referências aprovadas do KTD"
