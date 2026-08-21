# Ilha de Produção Artística do DJ Káiros

## Princípio de integração

A Ilha de Produção Artística é um núcleo complementar do KAIR-S-SONICA. Ela não substitui o `MultimediaOrchestrator`, o `AudioPipeline`, o `TaskStore`, o worker persistente, o backend SkyReels ou o estúdio browser já existente. Sua primeira responsabilidade é transformar a intenção musical em um plano de processamento explícito, revisável e rastreável.

> **Regra operacional:** planejar é seguro por padrão; executar DSP, carregar plugins, acessar bibliotecas externas ou submeter jobs exige uma etapa explícita posterior.

## Camadas

| Camada | Responsabilidade | Estado inicial |
| --- | --- | --- |
| Atlas de instrumentos | Perfis psicoacústicos, EQ inicial, dinâmica, espaço e tags | YAML versionado, 18 perfis starter |
| Registro de algoritmos | Contratos de Dynamic EQ, multiband compression, transient, exciter, de-esser, pitch, formant, reverb, width, delay e HRTF | 12 specs, adapters opcionais |
| Skill Generator | Converte instrumento + contexto em cadeia de 5–15 etapas | Ativo, determinístico |
| NumpyChainExecutor | Preview local limitado para arrays mono/estéreo | Ativo, sem plugins |
| Adapters profissionais | Pedalboard, SciPy, Demucs, FluidSynth, VST3/AU/LV2 ou GPU | Não instalados nem acionados automaticamente |
| RAG de presets/IRs | Referências e proveniência por `reference_id` | Slot explícito, sem busca automática |
| Interface | Painel Skill Chain dentro do Recording/Mixing Studio | Ativo via API local |

## Atlas

O arquivo `config/instrument_atlas.yaml` é a fonte de perfis iniciais. As chaves incluem `family`, `roles`, `tags`, `eq_presets`, `compression`, `space` e, quando aplicável, `vocal`. O loader normaliza nomes textuais e numéricos, informa `source_status` e possui fallback embutido para imagens mínimas de runtime sem PyYAML.

O Atlas starter não pretende declarar que existem mais de cem perfis completos neste commit. Ele estabelece o schema e uma base de 18 perfis, que pode crescer por commits de dados revisáveis. Nenhuma biblioteca de samples, IR, checkpoint ou preset proprietário deve ser incluída sem licença, checksum, origem e revisão separados.

## API

`GET /v1/artistic-island/capabilities` retorna o schema, a origem do Atlas, o número de instrumentos, os algoritmos registrados, o modo `plan-first` e a indicação de que plugins externos não são executados.

`GET /v1/artistic-island/instruments` retorna os perfis normalizados para seleção no estúdio.

`POST /v1/artistic-island/mix-plan` recebe, por exemplo:

```json
{
  "instrument": "backing_vocal",
  "context": "vocal",
  "prompt": "backing feminino largo, noturno e inteligível",
  "max_steps": 12,
  "include_optional": true,
  "reference_id": "preset-kairos-001"
}
```

A resposta contém `chain`, `master_bus`, `provenance` e `warnings`. Cada passo tem `order`, `algorithm`, `parameters`, `rationale` e `execution_mode`. O endpoint não lê nem grava áudio e não cria tarefas.

## Execução de preview

`NumpyChainExecutor` aceita arrays `float32` com shape `(frames,)` ou `(frames, canais)`, com um ou dois canais. O executor implementa apenas uma referência conservadora para compressor simples, exciter, width, delay e reverb algorítmico curto. Dynamic EQ, spectral balancing, correção de pitch, mudança de formante e HRTF permanecem no relatório como `skipped` até um adapter específico ser habilitado.

O resultado sempre retorna o array e um `ExecutionReport` com etapas `applied`, etapas `skipped`, warnings e picos antes/depois. Essa divisão evita apresentar uma sugestão de cadeia como se fosse um master final de nível comercial.

## Fluxo com o estúdio

O operador captura/importa takes na console browser, seleciona um instrumento, escolhe contexto e opcionalmente informa uma referência. O painel consulta o Atlas e mostra a cadeia. O bounce WAV atual continua sendo local e manual. Uma futura rota de upload autenticado poderá associar um `asset_id` a um `project_id`; só então um adapter poderá aplicar uma cadeia aprovada e criar um `MultimediaRequest`/`TrackRequest` no `TaskStore`.

## Fluxo com o núcleo agentico

O Designer de Som pode usar a Ilha para enriquecer o `audio_plan`, mas o `AgenticOrchestrator` continua produzindo handoffs aprováveis. A cadeia sugerida deve entrar como metadado/proveniência de um handoff, não como execução implícita. O mesmo gate de aprovação que protege `VideoRequest` e `MultimediaRequest` deve proteger qualquer processamento de stems.

## Roadmap seguro

A evolução deve ocorrer em commits independentes: ampliar o Atlas com dados licenciados; adicionar medição LUFS, true peak e compatibilidade mono; criar timeline, trim e crossfade; persistir sessões; implementar upload autenticado; adicionar adapters DSP por capability; testar stems sintéticos; e só depois integrar plugins nativos em imagens GPU explicitamente versionadas e auditadas.
