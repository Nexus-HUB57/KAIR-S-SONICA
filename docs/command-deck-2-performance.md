# Command Deck Browser 2.0 — teste de estresse e performance

## Objetivo

Validar o command deck do StudioMaster em três camadas: contrato do gateway, canal WebSocket de performance e experiência browser. O teste não habilita adapters reais, não baixa modelos, não persiste áudio e não publica clips.

## Preparação

Inicie a API a partir da raiz do repositório:

```bash
PYTHONPATH=packages python3 -m uvicorn services.api.main:app --host 127.0.0.1 --port 8000
```

Em outro terminal, sirva o cliente conforme o `web-client/package.json`, apontando `VITE_API_BASE=http://127.0.0.1:8000` quando necessário. A API deve retornar `200` em `/health` e `/v1/studio-master/real-adapters/capabilities`, com `gate_enabled=false` por padrão.

## Carga de contrato

O harness [`scripts/load_test_studio_master.py`](../scripts/load_test_studio_master.py) executa, em cada rodada, capabilities, cânone, repertório, adapters reais, analytics, retraining, arranjo, assinatura, clip, plano responsivo, ducking, score técnico e clientes WebSocket. Ele grava percentis por rota e não cria registros históricos.

```bash
make load-studio-master STUDIO_ROUNDS=5 CONCURRENCY=10 STUDIO_WEBSOCKETS=5
```

O relatório padrão fica em `/tmp/studio-master-command-deck-stress.json`. Para uma execução arquivável, forneça um caminho fora de `data/` versionado:

```bash
PYTHONPATH=packages python3 scripts/load_test_studio_master.py \
  --rounds 20 --concurrency 20 --websocket-clients 20 \
  --output /tmp/kair-command-deck-stress-$(date +%Y%m%d-%H%M%S).json
```

O teste deve ter zero timeouts, zero erros HTTP e handshake WebSocket `101` em ambiente local. Os p50/p95/p99 são registrados como baseline; um limite de lançamento deve ser definido pelo ambiente de produção e não inferido a partir de uma única máquina.

## Fluxo browser

No Chromium, valide manualmente e por teclado: carregamento sem erro; catálogo de cânone/repertório; WebSocket em `performance ativa`; análise de take; plano responsivo; proposta de arranjo; Modo Káiros; plano de clip; refresh de preflight; e estado de fallback dos seis adapters.

Para cada ação, registre o tempo entre clique e primeiro estado visual de progresso e entre clique e resultado. A ação não pode bloquear o transporte de gravação, perder foco de teclado, gerar console error ou alterar o estado do worker sem aprovação. Em viewport de 1440×900 e 390×844, confirme que não há overflow horizontal, que os botões permanecem alcançáveis e que o foco é visível.

O painel de adapters deve mostrar `0/6 prontos` ou a contagem real do ambiente, `gate global desligado` quando o default estiver ativo, licença e fallback de cada card. Um pacote Python presente, mas sem allowlist, licença aceita ou manifesto aprovado, deve continuar como `FALLBACK_ONLY`.

## Pipeline completo

A validação de uma branch deve executar:

```bash
make test
make lint
python3 -m compileall -q packages services scripts
python3 scripts/validate_compose_yaml.py
pnpm --dir web-client run build
PYTHONPATH=packages python3 scripts/load_test_studio_master.py
```

A validação com adapters reais deve ser feita em ambiente separado, com manifesto de versão/checksum/licença, assets aprovados fora do Git e saída nova em staging. MoviePy deve gerar um MP4 que passe por `ffprobe`; Demucs deve usar checkpoint já provisionado quando downloads estiverem desligados; MOSNet deve ser reportado como score estimado; FluidSynth deve receber SoundFont com licença própria; Pedalboard deve ser revisado por causa da licença GPLv3 e componentes transitivos.

## Evidência e decisão

O relatório de uma execução deve guardar configuração, número de probes, sucesso/falha, throughput, p50/p95/p99, códigos HTTP, estado WebSocket e limitações do host. Um resultado verde de contrato não significa que o ambiente possui GPU, TensorFlow, Pedalboard, FluidSynth, Demucs, MOSNet ou MoviePy instalados; a capability precisa permanecer explícita.
