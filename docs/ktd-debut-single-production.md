# UNLEASH THE DRAGON — registro de produção

## Status atual

A faixa está classificada como **candidato a single de estreia / prova de arranjo**, ainda pendente de aprovação humana de KTD. A base é inédita e foi construída para o conceito de manifesto, mas a tentativa de gerar uma faixa integral neural com uma nova performance vocal falhou em duas rotas. Para não introduzir uma voz genérica ou abafada, o pipeline preservou a referência vocal oficial e a usou somente como prova de encaixe sobre a nova base.

## Ativos

| Função | Arquivo | Status |
| --- | --- | --- |
| Base inédita | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-bed-v1.wav` | candidato instrumental |
| Prova com referência vocal | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.wav` | candidato / arranjo |
| Prova comprimida | `assets/audio/releases/ktd-debut-single-unleash-the-dragon-official-vocal-arrangement-proof-v1.mp3` | candidato / escuta |
| Voz oficial | `assets/audio/kairos-rapid-rap-flow-demo-en-v3.mp3` | referência aprovada |
| Letra nova | `docs/ktd-debut-single-lyrics.md` | composição original |
| Conceito | `docs/ktd-debut-single-concept.md` | direção de lançamento |
| Render reproduzível | `scripts/render_ktd_debut_single.py` | script técnico |

## Direção musical

A base segue 102 BPM, Fá menor e aproximadamente 150 segundos. O desenho usa kick e snare secos, swing humano leve, subgrave controlado, Rhodes/piano escuro, textura metálica discreta, camada sintética contida e espaços de resposta no hook. A arquitetura é intro, verso, pre-hook, hook, segundo verso, bridge confessional, hook final e outro seco.

A base gerada pelo motor musical chegou a aproximadamente 146,57 segundos; o script de render usa `apad=whole_dur=150` para completar o grid de produção antes da soma vocal. O WAV final da prova tem exatamente 150,00 segundos; a versão MP3 mede aproximadamente 150,05 segundos por causa do padding de codificação.

## Cadeia DSP da prova

A voz oficial é tratada com high-pass em 65 Hz, low-pass em 12.500 Hz e compressão principal em threshold −19 dB, ratio 2,2:1, attack 8 ms, release 90 ms e makeup 1,08. Uma camada paralela usa threshold −32 dB, ratio 8:1, attack 3 ms, release 120 ms, makeup 1,5 e ganho 0,32, somada à voz em proporção 1:0,35. A base é reduzida para 0,58, a voz recebe peso 1,15 na soma e o master é limitado com loudness alvo de −14 LUFS, true peak −1,0 dB, LRA 7 e limiter 0,95.

## Decisão de autenticidade

A referência `kairos-rapid-rap-flow-demo-en-v3.mp3` continua sendo a única referência vocal aprovada. A tomada `ktd-vocal-rough-take-v2.wav` não foi utilizada. O resultado atual não deve ser anunciado como “a nova gravação vocal oficial de KTD”: ele é uma prova de arranjo para validar pocket, impacto, duração, dinâmica e direção de produção.

Para o lançamento definitivo, a etapa seguinte é gravar ou aprovar uma tomada nova sobre a letra de `docs/ktd-debut-single-lyrics.md`, preservando o timbre e a entrega da referência oficial sem clonar intérpretes reais. A promoção do single depende dessa aprovação humana.

## Critérios de escuta

A escuta deve avaliar se o hook entra cedo e permanece memorável, se a voz ocupa a frente sem mascaramento, se a ponte revela vulnerabilidade sem perder autoridade, se o segundo verso abre espaço para double-time e se o final deixa uma assinatura reconhecível. Também devem ser verificadas inteligibilidade, ausência de clipping, originalidade, consistência de metadados e segurança editorial.
