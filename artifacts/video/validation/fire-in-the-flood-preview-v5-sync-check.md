# FIRE IN THE FLOOD — sync check v5

## Resultado

O preview v5 foi reconstruído sem a terceira fonte duplicada e com os cortes derivados dos inícios de frases da master v4. Como o vídeo final usa 24 fps, os timecodes decimais foram quantizados para frames inteiros; a diferença máxima fica abaixo de um frame.

| Evento | Timecode da master | Frame de vídeo | Timecode efetivo |
|---|---:|---:|---:|
| Abertura / M01 | 00:00.18 | 0 | 00:00.000 |
| Entrada de M02 | 00:07.76 | 186 | 00:07.750 |
| Entrada do plano de chama M03 | 00:17.099 | 410 | 00:17.083 |
| Fim do preview | 00:25.10 | 602 | 00:25.083 |

## Seleção ativa

| Posição | Fonte | Ação |
|---:|---|---|
| M01 | `assets/video/inputs/fire-in-the-flood-entrance-attached-8s.mp4` | Entrada por corredor/porta e passagem para rua chuvosa |
| M02 | `artifacts/video/dynamic-shots/fire-in-the-flood-s01-10s.mp4` | Plano portrait de KTD em corredor molhado |
| M03 | `artifacts/video/dynamic-shots/fire-in-the-flood-v2-D01-walk.mp4` | Caminhada com chama, chuva, vapor e água |

A fonte `assets/video/aprovados/fire-in-the-flood-ktd-approved-dynamic-8s.mp4` foi retirada da posição M03 por duplicar a progressão corredor→rua já presente em M01/M02. A fonte `assets/video/promos/tiktok/fire-in-the-flood-tiktok-8s.mp4` segue excluída por ser visualizer estático.

## Integridade técnica

A saída validada é `artifacts/video/fire-in-the-flood-existing-materials-preview-v5.mp4`, com 720×1280, 24 fps, H.264, AAC estéreo a 44,1 kHz e duração efetiva de aproximadamente 25,083 s. O áudio é uma única faixa recortada da master v4 desde 00:00; os áudios originais dos clipes foram removidos.
