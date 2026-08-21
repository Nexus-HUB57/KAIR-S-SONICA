# FIRE IN THE FLOOD — auditoria de alinhamento letra–manifesto

## Resultado executivo

O manifesto de cenas forma um arco visual coerente — janela, enchente, memória familiar, exclusão, trabalho, booth, resistência, vulnerabilidade e retorno ao fogo. Porém, a revisão não pode declarar que as transições refletem **perfeitamente o áudio atual** porque a master v4 indicada no próprio manifesto não corresponde à letra canônica usada nas descrições de cena.

A letra canônica começa com:

> “Water at the window. / Fire in the chest. / They told me, ‘Pick one.’ / I carried both.”

A transcrição da master v4 começa com:

> “I hear the lock click. / I hear the clock tick. / Pressure made a language in, and I talk it.”

A divergência aparece já no primeiro bloco de dez segundos e se mantém em vários trechos subsequentes. Isso é uma **incompatibilidade de fonte**, não um problema de transição visual. O manifesto foi colocado em estado de gate para impedir que um corte seja sincronizado à letra errada.

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
| S16 → S17 | A vulnerabilidade volta ao fogo, ao hook final e ao outro | Vidro/respiração → olhar direto → saída e preto | Correta como encerramento visual; o texto exato do hook final ainda depende da master confirmada |

## Gate de aprovação

O manifesto foi atualizado com `status: blocked_pending_authoritative_vocal_master` e `audio_lyrics_match: false`. Nenhuma decisão de corte lyric-locked deve ser promovida a final até que uma das seguintes decisões seja tomada pela autoridade artística:

1. Confirmar que a master v4 é a gravação correta e atualizar a letra canônica/descrições de cena para o texto que realmente está no áudio; ou
2. Fornecer/aprovar uma master vocal de 168 segundos cuja letra corresponda a `docs/ktd-main-single-rework-lyrics.md`, mantendo o roteiro visual atual; ou
3. Autorizar expressamente a separação entre áudio v4 e letra canônica, caso em que o manifesto deve deixar de usar frases da letra como marcação temporal.

Até essa decisão, a continuidade visual está aprovada como tratamento, mas a sincronização letra–imagem está **não aprovada**. A geração de vídeos pode continuar somente como testes de atmosfera sem promoção para montagem final.

## Referências

[1]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-main-single-rework-lyrics.md "Letra canônica de Fire in the Flood"

[2]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md "Revisão da master v4"

[3]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/tree/main/assets/video/aprovados "Formato visual oficial aprovado"
