# Roteiro de slides — UNLEASH THE DRAGON: status PHD/GPU

**Público:** produção executiva, direção artística e engenharia audiovisual.

**Tom:** factual, direto e orientado a decisão.
**Mensagem central:** o Single 1 passou pela auditoria de metadados, mas a GPU local ainda não está pronta; qualquer renderização cloud deve permanecer opt-in, auditada e humanamente autorizada.

## Cover

**Título:** UNLEASH THE DRAGON — Status PHD / GPU

**Subtítulo:** Preflight aprovado, renderização local bloqueada, fallback cloud sob guardrails
**Apresentação:** KAIR-S-SONICA · StudioMaster

## Slide 1

**Título:** O gate PHD passou; a renderização ainda não

**Ideia central:** separar aprovação de metadados da capacidade de executar inferência.

**Conteúdo:**

- O Preflight PHD do Single 1 retornou `READY_FOR_APPROVAL` com `hard_gate_passed=true`.
- A decisão é sobre a conformidade do pedido e das referências, não sobre uma autorização automática de publicação.
- A fila de vídeo não foi acionada; não houve `POST /v1/video/generate`.
- O próximo bloqueio é infraestrutura: a GPU local não está provisionada.

**Mensagem do apresentador:** “Temos um pedido tecnicamente coerente e auditado, mas ainda não temos um backend de renderização pronto. Essas duas coisas precisam permanecer separadas.”

## Slide 2

**Título:** Identidade, voz e live-action ficaram travados no cânone

**Ideia central:** o resultado aprovado preserva as âncoras imutáveis de Kháirus.

**Conteúdo:**

- Artista: `kairos.khairus_the_dragon`.
- Perfil físico, perfil visual e mapa de tatuagens permanecem canônicos e imutáveis.
- A voz usa somente a referência oficial, sem override, clonagem ou troca de timbre/sotaque.
- A política audiovisual exige performance live-action contínua, ação física observável, câmera motivada e zero still, overlay ou pan/zoom sobre foto [1] [2].

**Mensagem do apresentador:** “O gate não está apenas conferindo campos administrativos. Ele impede que a produção remota ou local altere a pessoa, as tatuagens, a voz ou a gramática visual aprovada.”

## Slide 3

**Título:** A simulação CPU reproduziu o preflight sem renderizar

**Ideia central:** a auditoria pôde ser testada no host atual sem fingir que CPU é uma GPU.

**Conteúdo:**

- Declaração canônica lida: `UNLEASH THE DRAGON`, 102 BPM, Fá menor e referência vocal oficial [3].
- Asset aprovado conferido com `ffprobe`: vídeo H.264 + áudio AAC, 720×1280, 24 fps e 10,0 s.
- Duas passagens foram executadas: `auto_repair=false` e `auto_repair=true`; ambas retornaram `READY_FOR_APPROVAL` e nenhum reparo foi aplicado.
- O relatório registra `CPU_METADATA_ONLY`, `render_started=false` e `cloud_call_started=false` [4].

**Mensagem do apresentador:** “A CPU comprovou o contrato de metadados e a determinismo do gate. Ela não produziu frames novos, não substituiu o backend e não é apresentada como renderização.”

## Slide 4

**Título:** A GPU local está BLOCKED por ausência de runtime real

**Ideia central:** o bloqueio é mensurável e não será contornado por fallback silencioso.

**Conteúdo:**

| Verificação | Estado atual |
|---|---|
| `nvidia-smi` / GPU NVIDIA exposta | ausente |
| CUDA compiler e Docker/Compose | ausentes |
| PyTorch, Diffusers, Transformers, Accelerate | ausentes |
| `/models` ou `/opt/models` com checkpoint | ausentes |
| FFmpeg e FFprobe | disponíveis |
| Resultado do backend native | `enabled=false`, `ready=false` |

**Mensagem do apresentador:** “O fato de FFmpeg estar disponível só permite inspeção e montagem. Não autoriza inferência SkyReels. Para mudar esse status, precisamos de driver, runtime CUDA, dependências compatíveis, checkpoint e teste de readiness.”

**Fonte técnica:** os requisitos de driver/runtime, build compatível de PyTorch e instalação de Diffusers são descritos pelas fontes oficiais [5] [6] [7].

## Slide 5

**Título:** Cloud é uma rota explícita, não um fallback silencioso

**Ideia central:** a nova integração pode existir sem estar autorizada a gastar, enviar dados ou gerar mídia.

**Conteúdo:**

- `DISABLED`: estado padrão; nenhuma chamada externa é possível.
- `NOT_CONFIGURED`: provider ou endpoint ausente; nenhuma chamada externa é possível.
- `FALLBACK_ONLY`: configuração parcial, sem credencial, allowlist, licença, retenção ou orçamento válidos.
- `READY`: todos os gates técnicos satisfeitos, mas cada request ainda exige confirmação humana, preflight aprovado e contrato `t2v` sem upload de referências.

**Mensagem do apresentador:** “Configurar o adapter não significa ligar o provider. O sistema foi desenhado para tornar a ausência de autorização visível e impedir que uma falha local envie um take para a nuvem por conta própria.”

## Slide 6

**Título:** A decisão de infraestrutura continua aberta

**Ideia central:** há duas rotas viáveis, com perfis de controle e esforço diferentes.

**Conteúdo:**

| Rota | Vantagem principal | Risco ou trabalho pendente |
|---|---|---|
| API gerenciada de vídeo | início mais rápido e sem manutenção de GPU | validar retenção, licença, custo por geração, limites e qualidade live-action |
| GPU/worker remoto controlado pela equipe | maior controle de checkpoint, dados e observabilidade | provisionar driver, CUDA, modelo, segurança de rede e manutenção |

**Mensagem do apresentador:** “A API gerenciada é a opção mais leve para um teste controlado, mas só depois de escolher um provider. O repositório não inventa esse provider nem grava credenciais. A alternativa dedicada oferece mais controle, ao custo de maior operação.”

## Slide 7

**Título:** O fluxo seguro tem quatro barreiras antes do provider

**Ideia central:** nenhuma chamada cloud nasce de planejamento ou de uma falha local.

**Conteúdo:**

1. **Brief e identidade:** artista, perfil físico, tatuagens, voz, política live-action e manifesto de origem.
2. **Preflight PHD:** `media_kind=multimedia`, bloqueio de divergências e decisão `READY_FOR_APPROVAL`.
3. **Governança:** provider na allowlist, HTTPS, licença e retenção aceitas, orçamento positivo e credencial somente no ambiente.
4. **Ação humana explícita:** `POST /v1/video/cloud-submit` com `confirm_cloud_submit=true` e `human_approved=true`; sem retry automático e sem publicação automática.

**Mensagem do apresentador:** “O botão de submissão é deliberadamente diferente do endpoint local. Assim, observamos no log e no contrato quando houve uma decisão humana de incorrer em custo e transferir um pedido.”

## Slide 8

**Título:** Próxima decisão: provisionar GPU ou autorizar um provider

**Ideia central:** o pipeline está pronto para a próxima etapa, mas a autorização ainda é humana.

**Conteúdo:**

- **Opção A:** provisionar a GPU local e só então revalidar readiness, checkpoint e backend native.
- **Opção B:** escolher um provider cloud oficial, aprovar licença/retenção/orçamento e preencher a allowlist; manter `t2v` sem upload até validar o contrato.
- Em qualquer opção, conservar o Preflight PHD, a revisão de frames, a aprovação humana e a identidade imutável.
- Estado recomendado agora: `READY_FOR_APPROVAL` para metadados, `GPU=BLOCKED`, `CLOUD=DISABLED`.

**Mensagem do apresentador:** “A decisão não é ‘renderizar a qualquer custo’. É escolher conscientemente o ambiente que consegue preservar a qualidade, a identidade e a governança de Kháirus.”

## Referências

[1]: ./song1-audiovisual-quality-protocol-v3.md "Protocolo de qualidade audiovisual do Single 1"
[2]: ./ktd-approved-reference-audit-v2.md "Auditoria de referências aprovadas do KTD"
[3]: ./ktd-debut-single-lyrics.md "Declaração canônica do Single 1"
[4]: ../../single1-cpu-preflight-report.json "Relatório da simulação CPU e do preflight HTTP local"
[5]: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html "NVIDIA Container Toolkit Installation Guide"
[6]: https://pytorch.org/get-started/locally/ "PyTorch — Get Started Locally"
[7]: https://huggingface.co/docs/diffusers/en/installation "Hugging Face Diffusers — Installation"
