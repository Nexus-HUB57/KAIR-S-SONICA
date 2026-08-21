# FIRE IN THE FLOOD — auditoria de alinhamento letra–manifesto

> **Atualização v4:** esta auditoria registrou o bloqueio original entre a letra pré-v4 e a master v4. O bloqueio foi resolvido pela promoção da transcrição temporal da master v4 como nova letra canônica em `docs/ktd-main-single-rework-lyrics.md`. O roteiro lyric-locked vigente está em `docs/ktd-fire-in-the-flood-10s-scene-script-v4.md`; este documento permanece como registro histórico da correção.

## Resultado executivo

O manifesto de cenas forma um arco visual coerente — fechadura, relógio, corredor, pressão, booth, visão, chuva, correntes, levantamento e atmosfera instrumental. A auditoria original encontrou uma incompatibilidade entre a master v4 e a letra pré-v4. Essa incompatibilidade foi resolvida nesta revisão pela promoção da transcrição temporal v4 como letra canônica e pela atualização das descrições de cena.

A letra **pré-v4**, agora arquivada, começava com:

> “Water at the window. / Fire in the chest. / They told me, ‘Pick one.’ / I carried both.”

A letra canônica v4, extraída da master, começa com:

> “I hear the lock click. / I hear the clock tick. / Pressure made a language in, and I talk it.”

A divergência apareceu já no primeiro bloco de dez segundos e se manteve em vários trechos subsequentes. Isso foi uma **incompatibilidade de fonte**, não um problema de transição visual. A fonte foi corrigida: a transcrição temporal da master v4 passou a ser a letra canônica, e o manifesto/roteiro foram atualizados para acompanhar o áudio real.

## Fontes auditadas

| Fonte | Função | Resultado |
|---|---|---|
| `docs/ktd-main-single-rework-lyrics.md` | Letra e arco de performance declarados como canônicos | Define “Water at the window”, “Fire in the flood”, bridge vulnerável e outro |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | Master de áudio usada pelo pipeline | 168,000 s, 44,1 kHz, estéreo; texto transcrito não coincide com a letra canônica |
| `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4_transcription_20260821_110817.txt` | Evidência temporal da escuta automática | Abre com “I hear the lock click” e contém outro conjunto de versos |
| `data/releases/fire-in-the-flood-10s-scene-manifest-v1.json` | Decupagem visual vigente | Coerente com a letra canônica, mas bloqueado contra o áudio v4 atual |
| `assets/video/aprovados` | Formato visual obrigatório | Vertical 9:16, 720×1280, 24 fps, planos vivos de 8–10 s |

## Auditoria das transições

| Região | Intenção da letra canônica | Transição prevista no manifesto | Avaliação |
|---|---|---|---|
| S01 → S02 | A imagem da janela abre a memória da casa pequena e da chuva | Mão no vidro → onda na soleira → cômodo estreito | Visualmente correta; sincronização de áudio bloqueada |
| S02 → S03 | A casa leva à vela da avó e à responsabilidade de segurar a porta | Onda no piso → chama protegida → porta metálica | Dramaturgicamente correta; preservar chama como objeto real |
| S03 → S04 | A resistência doméstica vira o espaço branco de exclusão | Impacto da porta → branco fluorescente | Transição física forte e fiel ao arco de memória → sistema |
| S04 → S05 | O julgamento externo vira resposta escrita em ritmo | Luz branca → traço de carvão no concreto | Correta; manter mão, carvão e parede em movimento |
| S05 → S06 | A pressão e a fome antiga se transformam em fogo disciplinado | Traço → cabo/corredor → âmbar crescente | Correta; o fogo deve aparecer como reflexo/prática, não fantasia |
| S06 → S07 | O fogo interior entra no lift de rio, cidade e voz | Corredor frio → rua com corrente → poste molhado | Correta; o gesto da mão deve carregar o eixo espacial |
| S07 → S08 | “I brought the storm into the booth” exige entrada real no estúdio | Poste → cabo → booth, microfone e chuva no vidro | Correta e diretamente ligada à letra |
| S08 → S09 | O booth abre o primeiro hook e a chama continua viva | Microfone → chama/reflexo → caminhada alagada | Correta; cortar no ataque musical sem interromper a caminhada |
| S09 → S10 | A chama individual vira “whole room rise” | Rua inundada → galpão com silhuetas que se levantam | Correta; evitar transformar resposta coletiva em multidão genérica |
| S10 → S11 | O hook retorna ao trabalho técnico do verso 2 | Luzes do galpão → patchbay e cabos | Correta; usar o blink como match cut físico |
| S11 → S12 | “Cables/code” leva a trabalho, escada e seis futuros | LEDs → escada → ajuda física a uma silhueta | Correta, mas a presença de outra figura deve permanecer anônima e não virar personagem novo |
| S12 → S13 | A responsabilidade familiar abre a recusa da gaiola e a saída | Movimento ascendente → rooftop → porta aberta | Correta; a porta aberta é mais fiel que uma jaula literal |
| S13 → S14 | A verdade nomeada pede performance de maior densidade | Porta → túnel, dolly-back e luzes cortantes | Correta para a aceleração do verso 2 |
| S14 → S15 | O hook curto pede pergunta, porta e resposta “KTD” | Ataque consonantal → porta metálica → luz âmbar | Correta; o impacto da porta deve carregar o corte |
| S15 → S16 | A música desarma na bridge e troca poder por vulnerabilidade | Porta fechada → sala molhada, vidro e respiração | Correta; reduzir movimento de câmera sem congelar o ambiente |
| S16 → S17 | O instrumental final transforma respiração em saída | Vidro/condensação → olhar direto → saída e preto | Correta; não há nova letra vocal a sincronizar após 02:17.22 |

## Gate de aprovação — resolvido pela promoção v4

O manifesto foi anteriormente atualizado com `status: blocked_pending_authoritative_vocal_master` e `audio_lyrics_match: false`. Esse estado foi encerrado pela decisão de usar a transcrição temporal v4 como letra canônica. O manifest vigente registra `status: aligned_to_v4_transcription` e `audio_lyrics_match: true` com base na transcrição disponível. A revisão fonética humana continua sendo um controle de lançamento, não um bloqueio de desenvolvimento:

1. A master v4 permanece a gravação correta e a letra canônica/descrições de cena agora usam o texto detectado no áudio; ou
2. Uma futura escuta de KTD pode corrigir apenas fonemas ambíguos, sem reintroduzir a letra pré-v4; ou
3. Qualquer nova master deve gerar uma nova auditoria antes de alterar o lyric-lock.

A continuidade visual e a sincronização letra–imagem estão agora liberadas contra a transcrição v4. A geração de vídeos pode prosseguir nos timecodes do roteiro v4; qualquer correção lexical futura deve ser registrada como nova revisão.

## Referências

[1]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-main-single-rework-lyrics.md "Letra canônica de Fire in the Flood"

[2]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md "Revisão da master v4"

[3]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/assets/video/aprovados "Formato visual oficial aprovado"
