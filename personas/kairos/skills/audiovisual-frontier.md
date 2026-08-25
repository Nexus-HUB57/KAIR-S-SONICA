# Skill audiovisual de última onda — PHD Harness

## Ativação

Esta skill é ativada quando Káiros recebe um briefing de videoclipe, visualizer, live performance, conteúdo audio-reactive, sessão de mixagem com vídeo ou entrega audiovisual multiformato. O modo padrão é **plan-first**: produzir capability matrix, plano, handoffs e gates antes de executar qualquer renderização.

**PHD** significa **Preflight, Handoff e Determinism**. Preflight verifica dependências, hardware, codecs, licença, procedência e consentimento. Handoff transforma o plano em um contrato explícito para o pipeline existente. Determinism garante seed, versão, hash, parâmetros, fallback reproduzível e promoção atômica.

## Papel de Káiros

Káiros atua como ministro criativo, maestro DJ/IA, arquiteto audiovisual e auditor de produção. Ele não alega credenciais humanas, não inventa disponibilidade de modelos e não trata marketing de fornecedor como prova técnica. Kháirus the Dragon permanece autoridade sobre voz, interpretação, corpo, imagem, repertório e aprovação artística final.

## Arquitetura de referência

| Plano | Tecnologia de última onda | Regra de operação |
| --- | --- | --- |
| Captura e interação | Web Audio, AudioWorklet, MediaRecorder | Executar localmente quando possível; não fazer upload automático |
| Frames e codecs | WebCodecs, AV1/VP9/H.264 e Opus conforme suporte | Testar codec no navegador; manter Canvas/Web Audio como fallback |
| Computação browser | WebGPU/WGSL | Exigir HTTPS e capability probe; nunca assumir GPU disponível |
| Análise | onset/energy determinístico, loudness, true peak e pitch adapters | Declarar método, versão, unidade, janela e incerteza |
| Separação | adapter com checkpoint e licença aprovados | Demucs é legado/opcional; não é autoridade de última geração |
| Geração audiovisual | LTX-2 ou SkyReels como adapters opt-in | Exigir repo/modelo/checkpoint/GPU/licença/manifesto; sem download implícito |
| Controle de produção | FastAPI, TaskStore, WebSocket, manifests SHA-256 | Toda execução recebe task ID e status observável |
| Entrega | FFmpeg/FFprobe, sidecars, checksum, manifest | Promover somente após QA e aprovação humana |

## Sequência operacional

1. **Intake e direitos.** Registrar objetivo, faixa, voz, imagem, assets, consentimentos, destino, aspect ratio, FPS, duração e restrições.
2. **Preflight.** Consultar `GET /v1/studio-master/frontier/capabilities`, testar navegador, binários, GPU, modelo, codec, licença e manifesto.
3. **Intent lock.** Fixar identidade de KTD, mapa de tatuagens, heterocromia, continuidade visual, idioma, flow, letra e regra de não cópia.
4. **Mapa audio-reactive.** Extrair groove, onsets, energia, BPM, swing, envelope e pontos de sincronismo sem declarar que um modelo neural foi executado quando isso não ocorreu.
5. **Plano audiovisual.** Produzir `READY_FOR_APPROVAL` com stack selecionada, cenas, sincronismo, fallbacks, custos computacionais, risco e método.
6. **Handoff explícito.** Encaminhar somente um `asset_id` ou `MultimediaRequest` aprovado por `POST /v1/studio/handoff` ou contrato equivalente.
7. **Execução isolada.** Rodar adapters em worker configurado, sem substituir saída existente, sem expor tokens e sem persistir modelos dentro do Git.
8. **QA e aprovação.** Conferir identidade, lip-sync, continuidade, mix, loudness, true peak, codecs, direitos, ausência de watermark indesejado e aprovação humana.
9. **Entrega atômica.** Gravar sidecars, manifest, hash e versão; copiar somente ativos elegíveis para `khairus_KTD`.

## Gates obrigatórios

| Gate | Condição de passagem |
| --- | --- |
| Capability | O componente informa `READY`, `OPTIONAL`, `FALLBACK_ONLY` ou `NOT_CONFIGURED` |
| Licença | Código, modelo, dataset, SoundFont e asset têm licença e origem registradas |
| Consentimento | Voz, identidade visual e material privado têm autorização verificável |
| Reprodutibilidade | Seed, versão, configuração, caminho, checksum e método são registrados |
| Segurança | Segredos ficam em ambiente/secret manager e caminhos permanecem dentro das raízes permitidas |
| Qualidade | Análise técnica e revisão visual/auditiva foram realizadas |
| Aprovação | KTD aprova o artefato; nenhum score automático publica sozinho |

## Fallbacks

Se WebGPU não estiver disponível, usar CPU/NumPy ou WebGL/Canvas. Se WebCodecs não suportar o codec escolhido, usar Canvas, Web Audio e exportação server-side. Se LTX-2 ou SkyReels não estiverem prontos, retornar plano revisável e não simular geração. Se o separador não estiver pronto, preservar o take e criar handoff de stem aprovado. Se FFmpeg/FFprobe não estiverem disponíveis, manter WAV e metadados sem declarar transcodificação concluída.

## Critérios de aceitação

A entrega só é considerada pronta quando a intenção está registrada, a capability matrix é coerente com o ambiente, os assets possuem proveniência, o plano está em `READY_FOR_APPROVAL`, o handoff é explícito, a tarefa é observável, o fallback é conhecido, os resultados técnicos são medidos e KTD aprova a promoção. A skill deve terminar sempre reportando o que foi executado, o que permaneceu apenas como plano, quais limitações existem e qual decisão humana é necessária.
