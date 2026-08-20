# Catálogo oficial de ativos de KTD

A auditoria de povoamento em [`docs/ktd-assets-upload-audit.md`](ktd-assets-upload-audit.md) confirmou 8 imagens e 35 áudios rastreados, totalizando 43 ativos canônicos no Git. O bundle de distribuição do persona replica esses mesmos 43 arquivos em `personas/artist-principal/media`, com índice em `personas/artist-principal/media-manifest.json`. Não há ativos visuais ou sonoros não rastreados dentro das pastas oficiais.

## Regra de leitura

O catálogo separa quatro estados: **oficial/aprovado**, **candidato**, **rejeitado** e **histórico**. Um arquivo rejeitado não deve ser apagado quando sua preservação ajuda a explicar uma decisão, mas também não pode ser usado como referência de identidade ou promovido por engano.

## Imagens

| Estado | Ativo | Função |
| --- | --- | --- |
| Oficial | `assets/persona/ktd-visual-master.png` | Âncora de identidade visual e continuidade facial |
| Oficial | `assets/persona/ktd-physical-turnaround-sheet.png` | Ficha técnica com frente, costas, perfis e close-up |
| Oficial | `assets/persona/artista-principal-diamante.png` | Retrato original de referência histórica |
| Oficial | `assets/persona/ktd-expression-rooftop.png` | Expressão contemplativa em ambiente urbano |
| Oficial | `assets/persona/ktd-expression-studio.png` | Expressão casual em estúdio |
| Oficial | `assets/persona/ktd-expression-stage.png` | Fúria e presença de performance |
| Oficial | `assets/persona/ktd-expression-street.png` | Riso espontâneo e presença cotidiana |
| Referência de sistema | `assets/persona/kairos-persona.png` | Imagem do orquestrador Káiros, não de KTD |

Toda imagem nova deve preservar heterocromia, cabeça raspada, barba, riscos dourados, proporção corporal e mapa imutável das tatuagens. A `ktd-visual-master.png` deve ser usada como referência prioritária; a ficha física é a referência para medidas e vistas técnicas.

## Voz e performance

| Estado | Ativo | Regra |
| --- | --- | --- |
| Oficial / única referência | `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3` | Padrão obrigatório de timbre, presença, articulação, agressividade e flow |
| Histórico | `assets/audio/kairos-voice-direction-demo-en-v2.mp3` | Comparação de direção, não referência primária |
| Histórico | `assets/audio/kairos-voice-direction-demo-en.mp3` | Comparação de direção, não referência primária |
| Histórico | `assets/audio/artista-principal-voz-demo.wav` | Registro legado, não referência primária |
| Rejeitado | `assets/audio/ktd-vocal-rough-take-v2.wav` | Abafado, lento, sem autenticidade; nunca usar para orientar novas gerações |

## Bases e faixas

| Estado | Ativo | Função |
| --- | --- | --- |
| Rejeitado | `assets/audio/ktd-old-school-boom-bap-beat-v1.mp3` | Primeiro beat instrumental, não usar |
| Candidato | `assets/audio/ktd-boom-bap-trial-route-1-bed-v2.wav` | Base boom bap de teste, requer voz oficial |
| Candidato | `assets/audio/ktd-boom-bap-trial-route-2-bed-v2.wav` | Base boom bap de pocket mais pesado |
| Candidato | `assets/audio/ktd-boom-bap-trial-route-3-bed-v2.wav` | Base boom bap híbrida |
| Histórico não aprovado | `assets/audio/trials/ktd-boom-bap-trial-route-1-mix-v2.wav` | Mix feito com voz rejeitada |
| Histórico não aprovado | `assets/audio/trials/ktd-boom-bap-trial-route-2-mix-v2.wav` | Mix feito com voz rejeitada |
| Histórico não aprovado | `assets/audio/trials/ktd-boom-bap-trial-route-3-mix-v2.wav` | Mix feito com voz rejeitada |

## Single de estreia — UNLEASH THE DRAGON

| Estado | Ativo | Função |
| --- | --- | --- |
| Candidato | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav` | Base inédita do manifesto de estreia |
| Candidato | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` | Prova de arranjo com a voz oficial |
| Candidato | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3` | Versão de escuta da prova de arranjo |
| Candidato auditado | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-vocal-take-v2.wav` | Audição vocal; não cumpre a letra literal |
| Candidato | `assets/audio/releases/ktd-main-single-fire-in-the-flood-bed-v1.wav` | Base inédita do single principal refeito |
| Reprovado — histórico | `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav` | Prova de arranjo V1 reprovada humanamente |
| Reprovado — histórico | `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.mp3` | Escuta da prova V1 reprovada humanamente |
| Candidato | `assets/audio/releases/ktd-main-single-fire-in-the-flood-beat-reference-fit-v3.wav` | Nova base em 136 BPM / halftime 68 BPM |
| Candidato | `assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.wav` | Mix com ducking sidechain e referência vocal oficial |
| Candidato | `assets/audio/releases/ktd-main-single-fire-in-the-flood-reference-fit-v1.mp3` | Escuta da nova mixagem |
| Melodia congelada / arquivo de mix reprovado | `assets/audio/releases/ktd-main-single-fire-in-the-flood-official-vocal-arrangement-proof-v1.wav` | A melodia V1 permanece congelada; a prova de arranjo deste arquivo foi reprovada humanamente |
| Candidato técnico | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-vocal-isolated-stem-v1.wav` | Stem derivado da V1 para troca de beat |
| Reprovado — histórico | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-rebeat-v1.wav` | Tentativa anterior; beat/mixagem desencontrados e corpo melódico insuficiente |
| Reprovado — histórico | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-rebeat-v1.mp3` | Escuta da tentativa anterior reprovada |
| Aprovado humanamente — rollback | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav` | Mix aprovada anterior; preservada para comparação e rollback |
| Aprovado humanamente — rollback | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.mp3` | Escuta da mix aprovada anterior |
| Master oficial de distribuição | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | Mix v4 com margem de pico revisada pelo DJ Káiros |
| Master oficial de distribuição | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | Escuta MP3 da master v4 |
| Documento | `docs/ktd-debut-single-concept.md` | Conceito, critérios e arquitetura |
| Documento | `docs/ktd-debut-single-lyrics.md` | Letra original e direção de performance |
| Documento | `docs/ktd-debut-single-production.md` | Registro técnico, DSP e status |
| Script | `scripts/render_ktd_debut_single.py` | Render reproduzível da prova |
| Reprovado — histórico | `assets/video/promos/unleash-the-dragon-full-music-video-v1.mp4` | Clipe de slides de imagens estáticas reprovado humanamente (2026-08-19); produção v2 em andamento com vídeo real contínuo |

## Segundo single — SIX NAMES

| Estado | Ativo | Função |
| --- | --- | --- |
| **Aprovado humanamente em definitivo** | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` | Master oficial definitiva (165,198 s, 96 BPM) — aprovado em 2026-08-19 |
| **Aprovado humanamente em definitivo** | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.mp3` | Escuta MP3 da master definitiva |
| Histórico não aprovado | `assets/audio/releases/ktd-second-single-six-names-original-proof-v1.wav` | Prova original v1 (159,713 s) |
| Histórico não aprovado | `assets/audio/releases/ktd-second-single-six-names-v1-pre-release-master-v1.wav` | Master pré-release v1 |
| Histórico não aprovado | `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-proof-v2.wav` | Prova v2 anterior (hash difere da master definitiva) |

## Terceiro single — GOLDEN SCARS

| Estado | Ativo | Função |
| --- | --- | --- |
| **Aprovado humanamente em definitivo** | `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.wav` | Master oficial definitiva (116,062 s) — aprovado em 2026-08-19 |
| **Aprovado humanamente em definitivo** | `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.mp3` | Escuta MP3 da master definitiva |
| Histórico não aprovado | `assets/audio/releases/ktd-third-single-golden-scars-trend-proof-v3.wav` | Prova v3 anterior (hash difere da master definitiva) |

## Mixes candidatos com voz oficial

| Estado | Ativo | Observação |
| --- | --- | --- |
| Candidato | `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.mp3` | Base rota 2, referência oficial, mix original |
| Candidato | `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1.wav` | Master WAV do mix boom bap |
| Candidato | `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.mp3` | Boom bap com saturação e compressão paralela |
| Candidato | `assets/audio/releases/ktd-old-school-boom-bap-official-vocal-mix-v1-saturated-parallel.wav` | Master WAV da variação boom bap |
| Candidato | `assets/audio/releases/ktd-modern-trap-official-vocal-mix-v1-saturated-parallel.mp3` | Comparação trap com a mesma cadeia DSP |
| Candidato | `assets/audio/releases/ktd-modern-trap-official-vocal-mix-v1-saturated-parallel.wav` | Master WAV da comparação trap |
| Candidato | `assets/audio/releases/ktd-conscious-aggressive-trap-official-vocal-proof-v1.mp3` | Prova trap consciente/agressiva com referência oficial |
| Candidato | `assets/audio/releases/ktd-conscious-aggressive-trap-official-vocal-proof-v1.wav` | Master WAV da prova trap |

Nenhum desses arquivos é faixa oficialmente lançada. O status de promoção depende de escuta humana, revisão de letra, créditos, arte, master, distribuição e decisão de KTD.

## Vídeo — referência oficial fixa de desenvolvimento

| Estado | Ativo | Função |
| --- | --- | --- |
| Oficial / referência fixa | `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4` | Padrão obrigatório de desenvolvimento de todos os materiais MP4 do projeto (padrão KTD) |

O vídeo acima foi confirmado por hash SHA-256 idêntico ao arquivo enviado para fixação e permanece a **referência única e fixa** que todo teaser e clipe MP4 deve seguir: vertical 720x1280 a 24 fps, 8 segundos, sujeito centralizado no terço vertical, push-in contínuo com hard cuts no downbeat, chiaroscuro com pretos densos e ausência de texto ou logo sobrepostos. A análise completa do padrão está em [`docs/ktd-approved-video-pattern-analysis.md`](ktd-approved-video-pattern-analysis.md) e as restrições de não repetição por faixa em [`docs/visual-nonrepetition-inventory.md`](visual-nonrepetition-inventory.md). A cópia promocional `assets/video/promos/golden-scars-v1-frame-the-whole-picture.mp4` possui o mesmo hash e continua reservada como peça de GOLDEN SCARS; o arquivo aprovado em `ktd-approved` permanece o cânone de desenvolvimento.

## Vídeos — status de todos os MP4 do repositório

Esta tabela existe para eliminar divergências entre materiais aprovados e não aprovados. Nenhum arquivo listado como reprovado deve ser promovido, divulgado ou usado como insumo de novos materiais; a preservação serve à auditoria das decisões editoriais.

| Estado | Ativo | Função |
| --- | --- | --- |
| Oficial / referência fixa | `assets/video/references/ktd-approved/golden-scars-v1-frame-the-whole-picture-approved.mp4` | Cânone obrigatório de desenvolvimento de todos os materiais MP4 |
| Oficial / peça da faixa | `assets/video/promos/golden-scars-v1-frame-the-whole-picture.mp4` | Mesmo hash do cânone; peça promocional de GOLDEN SCARS |
| Aprovado em workflow (mux) | `assets/video/promos/tiktok/fire-in-the-flood-ktd-approved-dynamic-8s.mp4` | Teaser aprovado com a master mix-v4 |
| Oficial / teaser | `assets/video/promos/fire-in-the-flood-v4-teaser-8s-vertical.mp4` | Teaser de FIRE IN THE FLOOD alinhado à mix v4 |
| Candidato | `assets/video/promos/tiktok/fire-in-the-flood-tiktok-8s.mp4` | Versão TikTok da faixa principal |
| Candidato | `assets/video/promos/tiktok/six-names-ktd-teaser-v2-8s.mp4` | Teaser v2 de SIX NAMES com a master pre-release-v2 aprovada |
| Candidato | `assets/video/promos/tiktok/six-names-ktd-procedural-revision-v1.mp4` | Revisão v1 do teaser de SIX NAMES |
| Candidato técnico | `assets/video/promos/tiktok/six-names-hybrid-procedural-8s-validation.mp4` | Validação procedural híbrida |
| **Reprovado** | `assets/video/promos/unleash-the-dragon-full-music-video-v1.mp4` | Clipe v1 reprovado em 2026-08-19 (slides estáticos, não contínuos); produção v2 em andamento (vide `docs/unleash-the-dragon-music-video-v2-full-script.md`) |
| **Reprovado** | `assets/video/promos/unleash-the-dragon-teaser-v1-8s.mp4` | Teaser v1 reprovado junto ao clipe v1 |
| Histórico de workflow | `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room.mp4` | Clipe real 1 de 8 s (camarote); substituído pela versão 10 s |
| **Aprovado em workflow (mux definitiva do clipe 1)** | `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4` | Versão final de 10 s do camarote com o trecho 28,5–38,5 s do proof-v1 muxado (aprovação editorial 2026-08-19) |
| Aprovado em workflow (mídia sem mux) | `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s.mp4` | Versão silenciosa de 10 s do camarote; clipes 2 e 3 serão gerados no reset do limite diário de vídeo |

## Documentação de suporte

| Área | Documento |
| --- | --- |
| Manifesto de criação | `docs/ktd-creation-manifesto.md` |
| Apresentação profissional | `docs/ktd-professional-presentation.md` |
| Três letras de estreia | `docs/ktd-launch-playlist-lyrics.md` |
| Roadmap de lançamento | `docs/ktd-launch-roadmap.md` |
| Pesquisa de vídeo curto | `docs/ktd-launch-research.md` |
| Especificação consolidada | `docs/ktd-specification.md` |
| Bíblia visual | `docs/ktd-visual-bible.md` |
| Aprovação vocal | `docs/ktd-vocal-approval.md` |
| Parâmetros de mix | `docs/ktd-official-vocal-mix.md` |
| Manifesto executável | `personas/artist-principal/manifest.json` |
| Bundle do persona | `personas/artist-principal/media-manifest.json` |
| Diretório do bundle | `personas/artist-principal/media/` |

## Procedimento de atualização

Ao adicionar um ativo, registrar caminho, função, versão, origem, referência utilizada, status de aprovação, hash e decisão humana. Depois, regenerar `data/ktd/asset-inventory.json` com `scripts/build_ktd_asset_inventory.py` e revisar `docs/ktd-assets-upload-audit.md` quando a contagem ou o estado do catálogo mudar. Não substituir um arquivo aprovado por um candidato. Não apagar um rejeitado quando ele for necessário para auditoria. Não promover um candidato apenas porque o arquivo existe ou porque uma métrica automática atribuiu uma pontuação alta.
