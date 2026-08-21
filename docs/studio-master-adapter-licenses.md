# StudioMaster — matriz de licenças dos adapters

Esta matriz é uma triagem de engenharia e não substitui revisão jurídica para um binário distribuído. O princípio do projeto é instalar adapters somente no ambiente do operador, não copiar código para o repositório e não colocar pesos, soundfonts, modelos ou dados de treinamento no Git.

| Adapter | Origem oficial | Licença do código | Risco/condição de integração | Fallback padrão |
| --- | --- | --- | --- | --- |
| CREPE | [marl/crepe](https://github.com/marl/crepe) | MIT | O pacote inclui modelo pré-treinado e depende de TensorFlow; pesos, datasets citados e redistribuição devem ser auditados separadamente. | `HumToMidiSketcher` sobre frames fornecidos |
| Pedalboard | [spotify/pedalboard](https://github.com/spotify/pedalboard) | GPLv3 | A própria documentação informa componentes GPLv3 e dependências com opções comerciais, incluindo JUCE/Rubber Band; distribuição fechada/comercial exige análise de compatibilidade e avisos. | Preview NumPy/contratos DSP |
| FluidSynth | [FluidSynth/fluidsynth](https://github.com/FluidSynth/fluidsynth) | LGPL | A biblioteca é LGPL, mas SoundFonts, bancos e arquivos MIDI têm licenças próprias e não devem ser baixados implicitamente. | Cadeia instrumental declarativa sem renderização |
| Demucs | [demucs no PyPI](https://pypi.org/project/demucs/) | MIT para o código | Checkpoints e datasets não são automaticamente equivalentes à licença do código; separar stems exige modelo, Torch/torchaudio e armazenamento temporário controlado. | Handoff de stems já aprovados |
| MOSNet | [lochenchou/MOSNet](https://github.com/lochenchou/MOSNet) | MIT para o repositório | Pesos e dados VCC2018 têm origem e condições próprias; a métrica deve ser chamada de score técnico/MOS estimado, nunca de avaliação humana. | `PerceptualValidator` CPU |
| MoviePy | [zulko/moviepy](https://github.com/zulko/moviepy) | MIT | O encode/decode usa FFmpeg e fontes/filtros podem trazer licenças separadas; o renderer deve usar asset autorizado e validar MP4 com `ffprobe`. | Plano de clip e canvas browser |

## Regras do registry

O registry deve declarar `code_license`, `model_license_status`, `runtime_dependencies`, `requires_gpu`, `requires_external_asset`, `risk_level`, `fallback` e `enabled`. A mera presença de um pacote Python não torna um adapter pronto para produção. Um adapter só pode ser habilitado quando o operador fornecer versão, checksum, origem, licença aceita, modelo/peso autorizado e política de retenção.

Adapters com dependência copyleft ou com assets externos não são incorporados ao caminho obrigatório do KAIR-S-SONICA. A integração real deve ser feita por import lazy e interface estreita; quando a dependência estiver ausente ou a licença não estiver marcada como aceita, o sistema retorna `unavailable` e usa o fallback determinístico.

## Fontes consultadas

[1]: https://github.com/marl/crepe "CREPE — repositório oficial"
[2]: https://raw.githubusercontent.com/marl/crepe/master/LICENSE "CREPE — licença MIT"
[3]: https://github.com/spotify/pedalboard "Pedalboard — repositório oficial e seção de licença"
[4]: https://github.com/fluidsynth/fluidsynth "FluidSynth — repositório oficial e seção de licença"
[5]: https://pypi.org/project/demucs/ "Demucs — página oficial no PyPI"
[6]: https://github.com/lochenchou/MOSNet "MOSNet — repositório oficial e seção de licença"
[7]: https://github.com/zulko/moviepy "MoviePy — repositório oficial e seção de licença"
[8]: https://github.com/spotify/pedalboard/blob/main/LICENSE "Pedalboard — arquivo de licença"
[9]: https://github.com/fluidsynth/fluidsynth/blob/master/LICENSE "FluidSynth — arquivo de licença"
