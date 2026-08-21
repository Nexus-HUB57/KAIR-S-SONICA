# FIRE IN THE FLOOD — geração audiovisual desacoplada

## Objetivo

A geração das cenas foi separada da preparação editorial e técnica para que o desenvolvimento do clipe continue sem produzir uma versão falsa, estática ou incompleta. O repositório agora contém o roteiro de 168 segundos, a fila de prompts, os keyframes 16:9, o script de normalização/montagem e as referências oficiais.

## Estrutura temporal

A música é tratada como 16 cenas de 10 segundos, entre 00:00 e 02:40, mais uma cena final de 8 segundos, entre 02:40 e 02:48. A soma é exatamente 168 segundos.

| Componente | Arquivo | Estado |
|---|---|---|
| Roteiro de cenas | `docs/ktd-fire-in-the-flood-10s-scene-script-v1.md` | Consolidado |
| Manifest de cenas | `data/releases/fire-in-the-flood-10s-scene-manifest-v1.json` | 17 cenas / 168 s |
| Fila de prompts | `data/releases/fire-in-the-flood-10s-generation-queue-v1.json` | Pronta para execução posterior |
| Gerador da fila | `scripts/build_fire_in_the_flood_10s_queue.py` | Validado |
| Montagem e mux | `scripts/assemble_fire_in_the_flood_10s.py` | Validado sintaticamente |
| Master de áudio | `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav` | 168 s / 44,1 kHz / estéreo |

## Regra de execução posterior

A fila permanece em estado de gate porque a transcrição da master v4 não coincide com a letra canônica usada no roteiro. O fato está registrado em [`docs/ktd-fire-in-the-flood-manifest-lyric-alignment-audit-v1.md`](ktd-fire-in-the-flood-manifest-lyric-alignment-audit-v1.md) e no campo `alignment_review` do manifest. Os planos podem ser gerados como testes visuais, mas não devem ser promovidos a montagem lyric-locked até que KTD confirme a master correta ou a letra correspondente.

Cada entrada da fila deve gerar um vídeo contínuo, sem áudio embutido, em portrait 9:16, 720×1280 e 24 fps, exatamente como os assets oficiais aprovados. A master v4 somente entra na etapa final, depois que os 17 vídeos forem verificados individualmente. O script de montagem recusa a execução quando existe cena ausente, duração divergente ou soma temporal diferente de 168 segundos.

A fila é um artefato reprodutível de preparação; ela não executa chamadas de geração de vídeo de forma autônoma enquanto a sessão estiver inativa. Quando a geração estiver disponível, os arquivos deverão ser produzidos nos caminhos definidos no manifest e a montagem poderá ser iniciada com:

```bash
python3 scripts/assemble_fire_in_the_flood_10s.py
```

O resultado esperado é `artifacts/video/ktd-fire-in-the-flood-full-dynamic-10s-v1.mp4`, com vídeo normalizado para 720×1280 a 24 fps e áudio AAC derivado da master v4.

## Critério de aceite

Nenhum PNG deve ser tratado como plano final. Um plano somente entra no clipe quando KTD age, a câmera se desloca, o cenário reage e existe movimento temporal observável durante todo o bloco. Qualquer saída que pareça uma fotografia com zoom deve retornar à fila para nova geração.

## Referências

A gramática dinâmica e o formato vertical seguem os assets da pasta oficial `assets/video/aprovados`, começando pelo reel aprovado de Fire in the Flood [1] e pela referência aprovada de ação ritual de Six Names [2]. A duração e as decisões de áudio seguem a revisão da master v4 [3].

[1]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/assets/video/promos/tiktok/fire-in-the-flood-ktd-approved-dynamic-8s.mp4 "Fire in the Flood — approved dynamic reel"

[2]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/assets/video/promos/six-names-ktd-clip-table-candles-10s-with-audio.mp4 "Six Names — approved dynamic reel with audio"

[3]: https://github.com/Nexus-HUB57/KAIR-S-SONICA/blob/main/docs/ktd-fire-in-the-flood-v1-reference-aligned-mix-v4-pre-release-review.md "Fire in the Flood — v4 pre-release review"
