# Estúdio de Gravação e Mixagem — DJ/Produtor Káiros

## Escopo da primeira entrega

O estúdio é uma console complementar integrada ao `web-client` existente. Ele permite iniciar captura de microfone pelo `MediaRecorder`, importar arquivos de áudio locais, organizar takes em camadas, ajustar volume e panorama estéreo, alternar mute/solo, reproduzir um mix local e exportar um bounce WAV pelo `OfflineAudioContext`.

A implementação é deliberadamente local no navegador. Até que seja criada uma rota de upload de stems com autenticação, o áudio não é enviado automaticamente ao backend, não entra no `TaskStore` e não é confundido com um job de geração. Isso preserva o pipeline de áudio existente e mantém a gravação de referência sob controle do operador.

## Fluxo operacional

O operador informa o nome do take, escolhe o formato suportado pelo navegador e autoriza o microfone. Ao iniciar a gravação, o estúdio conecta a entrada ao analisador de nível, mostra a waveform no canvas e atualiza o relógio. Ao parar, o blob é decodificado para um `AudioBuffer` e recebe uma nova camada na sessão.

A importação aceita formatos de áudio reconhecidos pelo navegador. Cada camada mantém seu `AudioBuffer`, duração, taxa de amostragem, volume, panorama, mute, solo e URL local temporária. O mix usa as camadas solo quando qualquer solo está ativo; caso contrário, usa todas as camadas não mutadas.

O bounce cria uma renderização offline estéreo, aplica ganho e panorama de cada camada, converte o resultado para PCM 16-bit WAV e inicia um download com nome determinístico por timestamp. O arquivo exportado não é gravado no repositório nem enviado ao gateway.

## Contrato de segurança

| Operação | Estado atual | Efeito externo |
| --- | --- | --- |
| Capturar microfone | Disponível após permissão do navegador | Nenhum upload automático |
| Importar take | Disponível via `input type=file` | Arquivo fica local na sessão do navegador |
| Reproduzir mix | Disponível via Web Audio API | Nenhuma chamada de rede |
| Exportar bounce | Disponível via download WAV | Nenhuma escrita no `TaskStore` |
| Enviar stem ao pipeline | Próxima etapa | Deve usar endpoint autenticado e job explícito |
| Persistir projeto | Próxima etapa | Deve usar namespace de projeto e armazenamento controlado |

## Integração futura com o núcleo KAIR

A próxima integração deve adicionar um endpoint de upload de stem com limites de tamanho, extensão e duração, armazenar o arquivo em `data/uploads` ou storage autenticado e retornar um `asset_id`. Um comando separado poderá criar um `MultimediaRequest` ou `TrackRequest` no `TaskStore`, mantendo `PENDING`, `RUNNING`, `SUCCEEDED` e `FAILED` e a entrega de artefato já existentes.

O estúdio também pode consumir o contrato de `/v1/agentic/run`: o briefing musical, BPM, tonalidade, swing, letra e takes aprovados podem alimentar o Designer de Som e o `audio_pipeline`. Essa integração deve continuar explícita e exigir aprovação, assim como os handoffs de vídeo; o planner não deve enviar gravações locais automaticamente.

## Testes já executados

O build Vite foi aprovado. A interface local foi aberta no navegador, um WAV estéreo temporário de 1,2 s a 48 kHz foi importado como take e a trilha apareceu com controles de volume, panorama, mute e solo. O bounce WAV foi exportado e apareceu no histórico de downloads do navegador.

## Próximas etapas de produto

A evolução recomendada é adicionar timeline com posicionamento de takes, trim e crossfades; suporte a stems mono/estéreo e ganho por clip; persistência de sessão; upload autenticado; medição LUFS/true peak no backend; exportação MP3 opcional; e roteamento de stems aprovados para o pipeline de áudio existente. Essas etapas devem ser implementadas em commits separados, com limites de recurso e testes determinísticos.
