# KAIR-S-SONICA — Auditoria de mídias e estado do repositório

## Direção visual
Apresentação editorial musical, escura e cinematográfica, com fundo carvão, acentos âmbar e azul elétrico, tipografia limpa e grande. Usar formas de onda, cartões de metadados e uma linha do tempo Git como elementos gráficos. Evitar sobrecarregar os slides com nomes longos; mostrar nomes completos apenas nos slides de inventário.

## Slide 1 — Capa
**KAIR-S-SONICA**
Auditoria de mídias importadas e estado atual do repositório
19 de agosto de 2026

Subtítulo: Integridade técnica, rastreabilidade e preparação para lançamento.

## Slide 2 — Resumo executivo
A importação foi concluída sem sobrescrever arquivos existentes.

Destaques: 15 mídias novas; aproximadamente 219 MB; 14 arquivos de áudio e 1 vídeo; commit publicado `51fa31e`; branch `main` sincronizada com `origin/main`; working tree limpa.

## Slide 3 — Estado Git e CI/CD
Mostrar a linha do tempo: `cf1e34b` — persistência SQLite; `51fa31e` — mídias pendentes do catálogo KTD.

Estado atual: HEAD local e remoto em `51fa31e`; nenhum workflow GitHub Actions encontrado; nenhuma execução remota registrada; validação local concluída com 19 testes aprovados, Ruff sem erros e `git diff --check` limpo.

Mensagem principal: a mídia não quebrou o código, mas o projeto ainda não possui CI/CD automatizado.

## Slide 4 — Inventário importado
Organizar por coleção:

**FIRE IN THE FLOOD:** 2 arquivos de pré-lançamento V4, WAV e MP3.

**SIX NAMES:** 8 arquivos, incluindo original proof, rebuilt soul proof/pre-release e master V1, em WAV e MP3.

**GOLDEN SCARS:** 4 arquivos de áudio, proof/pre-release V3/V1, em WAV e MP3.

**Vídeo:** 1 MP4 vertical de GOLDEN SCARS, 720×1280, 8 segundos.

## Slide 5 — Validação técnica dos áudios
Todos os arquivos foram reconhecidos por `file` e `ffprobe`.

WAV: PCM estéreo, 44,1 kHz, 16-bit, aproximadamente 1.411 kbps.

MP3: estéreo, 44,1 kHz, aproximadamente 320 kbps.

Durações: FIRE IN THE FLOOD 168 s; SIX NAMES entre 159,7 s e 165,2 s; GOLDEN SCARS aproximadamente 116,1 s.

## Slide 6 — Metadados e tags ID3
Foram analisados 14 arquivos de áudio: 7 MP3 e 7 WAV.

Achado: os MP3 possuem somente `encoder=Lavf60.16.100`; não há tags editoriais completas de título, artista, álbum, faixa, ano, gênero, copyright ou ISRC.

Os WAVs não possuem ID3, como esperado.

Recomendação: preencher metadados em cópias de distribuição, mantendo os masters originais imutáveis e versionados.

## Slide 7 — Rastreabilidade e integridade
Apresentar o manifesto `docs/media-import-audit-2026-08-19.md` e o relatório `docs/audio-metadata-id3-2026-08-19.md`.

Cada arquivo possui tamanho, duração, formato e SHA-256 registrados. Os caminhos foram escolhidos apenas quando não existiam previamente; arquivos já presentes foram preservados.

## Slide 8 — Próximas decisões
1. Criar workflow GitHub Actions com testes, lint e validação de mídia.
2. Adicionar verificação automática de hashes e limites de tamanho.
3. Criar pipeline de metadados de distribuição em cópias, sem editar masters.
4. Desenvolver os vídeos curtos da turnê inicial com versões 9:16, 1:1 e 16:9.
5. Manter commits de mídia separados de mudanças de código.

## Slide 9 — Encerramento
**Estado: pronto para a próxima camada de lançamento.**

Repositório sincronizado, mídia rastreável e integridade técnica confirmada. Próximo marco: automatizar CI/CD e transformar o catálogo em um pacote de distribuição com metadados editoriais completos.
