# KTD — Plano Mestre de Produção — 2026-08-24

## Estado da carreira
| Item | Status | Localização |
|------|--------|-------------|
| Singles 1–5 | Masters aprovadas | khairus_KTD/audio/singles/ |
| Single 11 (I Won't Waste This Life) | Prova 2 aprovada, campanha liberada | docs/singles/ |
| Single 12 (Hold the Ladder) | Aprovado, Prova 1 gerada, docs commitados | docs/singles/single-12-* |
| Single 13 (What Happens in Vegas) | Prova 1 gerada, docs commitados, Prova 2 EDM pendente | docs/singles/single-13-* |
| Videoclipe Fire in the Flood | Fila v2 commitada, S02–S17 aguardando render | data/releases/fire-in-the-flood-10s-generation-queue-v2-scene01-contract.json |

## Fila de execução — HANDOFF PARA O PRÓXIMO DEV (atualizado 2026-08-24)

### Concluído nesta sessão
- [x] Prova 2 EDM do Single 13 gerada — https://www.genspark.ai/api/files/s/c166etkN (160.7s)
- [x] Prova 1 boom bap do Single 13 — https://www.genspark.ai/api/files/s/K1uJpu5D (162.3s)
- [x] Single 12 aprovado, Prova 1 — https://www.genspark.ai/api/files/s/kD6tBAFX (155.9s)

### Próximo dev — executar nesta ordem (créditos novos)
1. **DECISÃO HUMANA PRIMEIRO**: titular ouve as 2 provas do Single 13 e escolhe direção (boom bap vs EDM vs colisão) — custo zero
2. **Vídeo Vegas 8s** (Single 13, Seedance 2.0 standard+áudio, ≈760 créditos) — prompt completo no histórico da sessão e nesta fila; referências de identidade já publicadas:
   - master: https://www.genspark.ai/api/files/s/GmONKgUk
   - turnaround: https://www.genspark.ai/api/files/s/t6lPE4rs
   - keyframe final: https://www.genspark.ai/api/files/s/7H5bY6Iv
   - áudio ref (lip-sync): https://www.genspark.ai/api/files/s/K1uJpu5D
   - keyframes por cena do clipe FITF: s01vocal WTxor6ER, s01 A4UPS7sm, s02 kOQNKd74, s03 mGFc4kyZ, s04 ZVq1lOIt, s05 j0VlpvOD, studio QsOTDR8a, bridge z95tLNNK, final 7H5bY6Iv, final-stage dHfd0QCp
3. **Cenas S02–S05 do videoclipe FITF** (Seedance 2.0 fast, 4×~380 = ~1.520 créditos) — prompts completos em data/releases/fire-in-the-flood-10s-generation-queue-v2-scene01-contract.json
4. **Cenas S06–S17** (lotes de 3, gate de identidade entre lotes, ~4.600 créditos restantes)
5. **Montagem final 168s** com master v4 muxado (ffmpeg, gratuito) + commit dos aprovados em khairus_KTD

## Bloqueio atual
Saldo esgotado após geração da Prova 2 EDM (2026-08-24). Próxima sessão de créditos retoma do item 2 acima.

## Ação imediata do titular
1. Recarregar créditos na conta Genspark
2. Revogar tokens GitHub expostos na conversa (os dois tokens colados na conversa do Hub em 2026-08-22 — revogar em GitHub Settings > Developer settings)
3. Definir data de lançamento / ISRC do Single 1
4. Configurar OAuth de @khairusktd_ofc / @ktd_oficial para ativar social orchestrator
