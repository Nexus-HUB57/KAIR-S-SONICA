# Auditoria de povoamento de imagens e áudios de KTD

## Resultado

A auditoria de 18 de agosto de 2026 foi atualizada após a revisão final do DJ Káiros. Foram encontrados **8 arquivos de imagem** em `assets/persona` e **40 arquivos de áudio** em `assets/audio`, totalizando **48 ativos canônicos** no bundle do persona. A mix `v1-reference-aligned-mix-v4.wav/.mp3` é a master oficial de distribuição; a v3 permanece aprovada como rollback histórico; as provas `official-vocal-arrangement-proof-v1.wav/.mp3` permanecem versionadas, mas marcadas como reprovadas históricas. Não há arquivos de imagem ou áudio pendentes dentro das pastas oficiais, e `main` será sincronizada com `origin/main` após a publicação desta atualização.

Nenhum ativo histórico foi apagado ou substituído na fonte canônica. Para atender à organização solicitada em `personas/artist-principal`, os mesmos 48 ativos foram copiados sem alteração de conteúdo para `personas/artist-principal/media`, com índice em `personas/artist-principal/media-manifest.json`; como os blobs são idênticos, o Git reutiliza o conteúdo por hash. Os ativos rejeitados e históricos continuam no catálogo com status separado, para impedir que sejam promovidos acidentalmente como referências oficiais.

## Imagens rastreadas

| Arquivo | Dimensão | Status |
| --- | --- | --- |
| `assets/persona/artista-principal-diamante.png` | 1664 × 2080 | oficial / referência histórica |
| `assets/persona/kairos-persona.png` | 1664 × 2080 | apoio de Káiros |
| `assets/persona/ktd-expression-rooftop.png` | 1536 × 2304 | oficial / expressão |
| `assets/persona/ktd-expression-stage.png` | 1536 × 2304 | oficial / performance |
| `assets/persona/ktd-expression-street.png` | 1536 × 2304 | oficial / expressão |
| `assets/persona/ktd-expression-studio.png` | 1536 × 2304 | oficial / expressão |
| `assets/persona/ktd-physical-turnaround-sheet.png` | 2560 × 1440 | oficial / ficha técnica |
| `assets/persona/ktd-visual-master.png` | 1664 × 2080 | oficial / imagem-mestre |

## Áudios rastreados

A referência vocal oficial permanece `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3`, com aproximadamente 137,72 segundos, estéreo, 44,1 kHz. A tomada `assets/audio/ktd-vocal-rough-take-v2.wav` permanece rejeitada e não deve ser usada como identidade vocal.

| Grupo | Conteúdo |
| --- | --- |
| Vozes e referências | `artista-principal-voz-demo.wav`, `kairos-rapid-rap-flow-demo-en-v3.mp3`, `kairos-voice-direction-demo-en-v2.mp3`, `kairos-voice-direction-demo-en.mp3`, `ktd-vocal-rough-take-v2.wav` |
| Bases boom bap | `ktd-boom-bap-trial-route-1-bed-v2.wav`, `ktd-boom-bap-trial-route-2-bed-v2.wav`, `ktd-boom-bap-trial-route-3-bed-v2.wav`, `ktd-old-school-boom-bap-beat-v1.mp3` |
| Bases trap | `ktd-modern-trap-comparison-bed-v1.wav`, `ktd-conscious-aggressive-trap-proof-bed-v1.wav` |
| Mixes candidatos | Arquivos em `assets/audio/releases/`, incluindo boom bap, trap moderno, FIRE IN THE FLOOD original e reference-fit |
| FIRE IN THE FLOOD master oficial | `ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav/.mp3`, com margem de pico revisada; letra e melodia de fundo preservadas |
| FIRE IN THE FLOOD rollback | `ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v3.wav/.mp3`, aprovado anteriormente e preservado para comparação |
| FIRE IN THE FLOOD reprovado histórico | `official-vocal-arrangement-proof-v1.wav/.mp3` e `v1-rebeat-v1.wav/.mp3`; mantidos apenas para auditoria |
| Mixes históricos | Arquivos em `assets/audio/trials/`, produzidos em rotas anteriores e mantidos apenas para auditoria |

## Política de povoamento

Novos ativos devem ser colocados em `assets/persona` ou `assets/audio`, receber status no catálogo e ser incluídos no inventário JSON. A promoção para oficial exige aprovação humana de KTD. A cópia de arquivos existentes, alteração de nomes sem necessidade e envio de ativos de referência externa — como a imagem de exemplo usada para a ficha física — não fazem parte do povoamento oficial do persona.

## Referências internas

- Catálogo semântico: [`docs/ktd-asset-catalog.md`](ktd-asset-catalog.md)
- Inventário técnico com hashes: [`data/ktd/asset-inventory.json`](../data/ktd/asset-inventory.json)
- Script de inventário: [`scripts/build_ktd_asset_inventory.py`](../scripts/build_ktd_asset_inventory.py)
- Manifesto de KTD: [`personas/artist-principal/manifest.json`](../personas/artist-principal/manifest.json)
- Bundle de mídia do persona: [`personas/artist-principal/media-manifest.json`](../personas/artist-principal/media-manifest.json)
