# KTD — mapa de migração audiovisual batch 001

## Estado do lote

| Campo | Valor |
|---|---|
| Repositório de origem | `Nexus-HUB57/KAIR-S-SONICA` |
| Repositório de destino | `Nexus-HUB57/khairus_KTD` |
| Commit de origem auditado | `cd03cb42791e8d0ccd57ab549a7e5453d0f9dac7` |
| Commit de destino | `364c40b23b62eee81c3221841013871fde1decdd` |
| Data da transição | 2026-08-22 |
| Estratégia | Cópia não destrutiva, com Git LFS para WAV e MP4 |
| Verificação | SHA-256 de cada arquivo de origem igual ao arquivo de destino |

O primeiro lote foi publicado no repositório audiovisual sem remover ou alterar os arquivos do repositório de produção. Os arquivos de origem continuam sendo preservados para rastreabilidade até uma futura etapa explícita de desduplicação.

## Arquivos de áudio

| Origem em `KAIR-S-SONICA` | Destino em `khairus_KTD` | SHA-256 |
|---|---|---|
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | `audio/singles/single-1-fire-in-the-flood/master/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | `a8668295687effed989121e58cead63fa00d951aff9a8335ff2065f0edd44229` |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | `audio/singles/single-1-fire-in-the-flood/master/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | `29c97dc68f487d945c6d0de02a88988ac41bd8fe3a9f56efaea6f743ab9ca208` |
| `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` | `audio/singles/single-2-six-names/master/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.wav` | `4f0b53930b29361ba23c765a4f6df3a22f684918335d3568df7cd5eb329408d5` |
| `assets/audio/releases/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.mp3` | `audio/singles/single-2-six-names/master/ktd-second-single-six-names-rebuilt-soul-pre-release-v2.mp3` | `ffa5aa9198cd7d19f2323fa4c3d5f2a30fb8e5cae9e90aadad2f0779996b1751` |
| `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.wav` | `audio/singles/single-3-golden-scars/master/ktd-third-single-golden-scars-trend-pre-release-v1.wav` | `8ff81301c8728e35ba228084825b3ee5c8c5d64f6a2ba5a8131e84dd1df617b8` |
| `assets/audio/releases/ktd-third-single-golden-scars-trend-pre-release-v1.mp3` | `audio/singles/single-3-golden-scars/master/ktd-third-single-golden-scars-trend-pre-release-v1.mp3` | `eed1257ee42cff1ec5ec507b709eda2eaa1b5c92977ad76b2820ce33d2242230` |
| `outputs/single_4/pressure-speaks-ktd-essence-v1-master.wav` | `audio/singles/single-4-pressure-speaks/master/pressure-speaks-ktd-essence-v1-master.wav` | `de997c004fe8e22e97dbf7e4a4d2e99c17f7f7b716af2230ec0406ed08816743` |
| `outputs/single_4/pressure-speaks-ktd-essence-v1-master.mp3` | `audio/singles/single-4-pressure-speaks/master/pressure-speaks-ktd-essence-v1-master.mp3` | `0b757691bd739acb88ec335cffe7ab96777149f0e2b4424d0521e3d4ed624254` |
| `outputs/single_5/single_5_no_more_quiet_cries_v1-master.wav` | `audio/singles/single-5-no-more-quiet-cries/master/single_5_no_more_quiet_cries_v1-master.wav` | `a89a976887fc8389cffa3b04379fc6a9737f4f5b062d1670b6a6607c6911f91f` |
| `outputs/single_5/single_5_no_more_quiet_cries_v1-master.mp3` | `audio/singles/single-5-no-more-quiet-cries/master/single_5_no_more_quiet_cries_v1-master.mp3` | `2401507017abeaf5eb01dec06ee3f4f53960c9b7657a26338095b7975641f214` |

## Arquivos de vídeo

| Origem em `KAIR-S-SONICA` | Destino em `khairus_KTD` | SHA-256 |
|---|---|---|
| `assets/video/promos/tiktok/fire-in-the-flood-ktd-approved-dynamic-8s.mp4` | `video/shorts/single-1-fire-in-the-flood/approved/fire-in-the-flood-ktd-approved-dynamic-8s.mp4` | `7a25ddeadda187b4cfdfb595d8b847ad2d9fa56740946de9b3844920b69c636b` |
| `assets/video/promos/golden-scars-v1-frame-the-whole-picture.mp4` | `video/singles/single-3-golden-scars/approved/golden-scars-v1-frame-the-whole-picture.mp4` | `0b5d4f2b996c96c17d92b0c718ec4c14f241e795587f7bcf9eb47c5720aba21a` |
| `assets/video/promos/unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4` | `video/singles/single-1-unleash-the-dragon/approved-clips/unleash-the-dragon-realgclip-01-dressing-room-10s-with-audio.mp4` | `1b518db13ca7eba75a9dcdc365bfa4c2d975278a922b59471f67877439b8eeed` |

## Itens deliberadamente não migrados

A pasta de identidade visual canônica continua em `KAIR-S-SONICA` porque os arquivos encontrados são referências de produção, não artes finais de entrega. Provas, demos, stems, beds, takes, previews e arquivos reprovados também permanecem no repositório de produção.

A Prova 2 Old School do Single 11 está pendente de avaliação humana e não foi migrada. A Prova 8 Funk é uma referência aprovada de ciclo, mas não foi tratada como lançamento audiovisual final neste lote. A versão 1 do videoclipe de `UNLEASH THE DRAGON` continua rejeitada e não foi copiada.

O teaser `assets/video/promos/fire-in-the-flood-v4-teaser-8s-vertical.mp4` não foi incluído porque o path não existe no checkout auditado; nenhum arquivo semelhante foi promovido por aproximação de nome.

## Próxima etapa

Cada novo lote deve repetir a auditoria do catálogo, conferência de aprovação, cópia a partir do path canônico, hash antes/depois, atualização de `MANIFEST.json`, validação de LFS e commit separado no destino. A remoção de duplicatas no repositório de produção exige uma decisão posterior e não faz parte do batch 001.
