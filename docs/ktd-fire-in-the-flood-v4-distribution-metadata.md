# FIRE IN THE FLOOD — pacote final de distribuição v4

## Estado do lançamento

A versão v4 de **FIRE IN THE FLOOD** foi aprovada pelo usuário e revisada tecnicamente pelo DJ Káiros. Ela é o master oficial de distribuição desta etapa. A v3 permanece preservada no repositório apenas como rollback histórico.

> **Importante sobre o ISRC:** este documento não fabrica um código. O ISRC oficial deve ser atribuído pelo titular/registrante autorizado ou pelo distribuidor que opere em nome dele. O código precisa ser registrado junto aos metadados da gravação e mantido de forma consistente em todas as plataformas.

## Metadados editoriais e de plataforma

| Campo | Valor de entrega | Observação |
| --- | --- | --- |
| Título | `FIRE IN THE FLOOD` | Título principal do single |
| Artista principal | `Kháirus the Dragon` | Nome artístico |
| Alias | `KTD` | Pode ser usado em créditos secundários e materiais promocionais |
| Tipo de lançamento | `Single` | Faixa individual |
| Versão | `v4 — official distribution master` | Não exibir necessariamente “v4” no título público |
| Idioma | `English (en-US)` | Letra e performance em inglês |
| Gênero | `Hip-Hop / Rap` | Direção: rap cinematográfico, boom bap swung e textura harmônica escura |
| Conteúdo explícito | `Yes — confirmar no distribuidor` | A letra contém uma ocorrência explícita; revisar a política da plataforma antes do envio |
| Duração WAV | `168.000 s` | 2:48 |
| Duração MP3 | `168.046 s` | Diferença causada pelo codec MP3 |
| BPM de produção | `94 BPM` | Grade temporal da V1 preservada |
| Tonalidade de produção | `D minor / Ré menor` | Informação de direção musical; confirmar se o distribuidor solicitar tonalidade |
| Data de lançamento | `A definir pelo titular/distribuidor` | Não inventar uma data de publicação |
| P-line / C-line | `A preencher pelo titular` | Requer nome legal e ano definidos pelo titular |
| Label / selo | `KAIR-S-SONICA — confirmar como selo de distribuição` | Campo operacional, não substitui a entidade legal |
| Territórios | `A definir pelo titular/distribuidor` | Preencher conforme contrato de distribuição |
| UPC/EAN | `Pendente de atribuição` | Código do produto/lançamento, independente do ISRC da gravação |
| ISRC oficial | `Pendente de atribuição pelo registrante` | Não usar placeholder como código real |
| Identificador interno | `KAIR-KTD-FITF-V4-2026` | Não é ISRC e não deve ser enviado no campo ISRC |

## Créditos a confirmar antes do envio

| Função | Crédito operacional | Pendência |
| --- | --- | --- |
| Artista principal | Kháirus the Dragon (KTD) | Confirmar grafia legal/artística no distribuidor |
| Letra | KTD / Kháirus the Dragon | Confirmar nome legal dos compositores/autores |
| Composição | Titular da obra FIRE IN THE FLOOD | Confirmar split sheet e cadastro editorial |
| Produção | DJ Káiros / Agente Káiros | Confirmar forma pública do crédito |
| Arranjo de groove | DJ Káiros / KAIR-S-SONICA | Crédito técnico do acompanhamento aprovado |
| Tratamento vocal e mix | DJ Káiros / KAIR-S-SONICA | Crédito técnico |
| Masterização | DJ Káiros / KAIR-S-SONICA | Crédito técnico da revisão v4 |
| Selo | KAIR-S-SONICA | Confirmar entidade legal ou distribuir como independente |
| Editora | A preencher | Não inventar editora |
| Direitos fonográficos | A preencher pelo titular | Confirmar proprietário do master |

## Especificações técnicas do master

| Arquivo | Uso | Codec | Resolução | Sample rate | Canais | Loudness medido | True peak medido |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | Master principal | PCM s16le | 16-bit | 44.100 Hz | 2 | −13,94 LUFS | −1,43 dBTP |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.mp3` | Escuta / distribuição compatível | MP3 LAME | 320 kbps | 44.100 Hz | 2 | −13,94 LUFS | −1,29 dBTP |

A faixa apresenta **LRA de 4,10 LU**. A v4 é matematicamente a v3 com ganho global de −0,9 dB, sem alteração de conteúdo musical, duração, panorama ou dinâmica relativa. O relatório completo está em [`docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md`](ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md).

## Checksums dos arquivos oficiais

| Arquivo | SHA-256 |
| --- | --- |
| WAV v4 | `a8668295687effed989121e58cead63fa00d951aff9a8335ff2065f0edd44229` |
| MP3 v4 | `29c97dc68f487d945c6d0de02a88988ac41bd8fe3a9f56efaea6f743ab9ca208` |

## Checklist de envio

Antes do upload, o titular ou distribuidor deve confirmar a grafia do artista, o título público, a marcação explicit/clean, a data de lançamento, os créditos legais, os splits de composição, o titular do master, o selo, o UPC/EAN, o ISRC e a política territorial. O arquivo WAV deve ser o master principal; o MP3 serve para conferência e para plataformas que o aceitarem como formato de entrega.

O ISRC não deve ser derivado do hash, do identificador interno ou do nome do arquivo. Segundo o IFPI, o ISRC possui 12 caracteres alfanuméricos, é atribuído ao registro específico por um registrante e deve manter metadados de referência como artista principal, título, duração, tipo de conteúdo e data de publicação [1] [2]. A escolha entre reutilizar um ISRC existente ou solicitar um novo para uma versão remasterizada deve ser confirmada pelo titular/registrante e pelo distribuidor, de acordo com a política aplicável à gravação final.

## Referências

[1]: https://isrc.ifpi.org/isrc-standard/isrc-structure "IFPI — ISRC Structure"

[2]: https://isrc.ifpi.org/why-use-isrc/using-isrc "IFPI — Using ISRC"

[3]: https://www.ifpi.org/wp-content/uploads/2021/02/ISRC_Handbook.pdf "IFPI — International Standard Recording Code Handbook"
