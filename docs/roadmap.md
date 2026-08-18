# Roadmap e critérios de integração

## Próxima versão

A prioridade é trocar o armazenamento em memória por persistência, adicionar autenticação, registrar métricas de duração e erro, validar limites de upload e criar uma fila de workers. Em paralelo, o cliente deve evoluir para reproduzir segmentos PCM sem esperar o arquivo completo.

## Marco artístico KTD

O nome oficial do artista é **Kháirus the Dragon (KTD)**. A próxima entrega musical é uma faixa completa com voz e instrumental boom bap integrados, baseada em `docs/ktd-approved-track.md`. O beat instrumental atualmente versionado é um experimento rejeitado; nenhuma saída será promovida sem aprovação humana de groove, voz, pocket e mixagem.

## Adaptadores de modelos

Um adaptador só deve ser ativado quando a dependência, o checkpoint e a licença forem conhecidos. O adaptador precisa implementar `generate(plan) -> np.ndarray`, declarar o dispositivo (`cpu` ou `cuda`) e emitir metadados de versão. Modelos que exigem download automático devem ser inicializados por operador ou pipeline de implantação explicitamente autorizado.

## Qualidade de áudio

O MVP usa normalização RMS e limitador de pico aproximados para manter a execução leve. A masterização de produção deve incluir medição LUFS com ferramenta validada, true peak, dither e testes de regressão auditiva. Os valores de swing são parâmetros musicais configuráveis, não uma regra universal para todos os gêneros.

## Voz e direitos

Qualquer módulo de conversão ou síntese vocal deve guardar prova de consentimento, origem do material de treino e restrições de distribuição. O repositório não fornece identidade vocal nem tenta contornar controles das plataformas de terceiros.

## Carreira de KTD

O roadmap artístico de Kháirus the Dragon está em [`docs/ktd-launch-roadmap.md`](ktd-launch-roadmap.md). Ele cobre fundação de identidade, laboratório de repertório, produção, pré-lançamento, lançamento e expansão, sempre com aprovação humana de KTD. O catálogo de ativos e seus estados estão em [`docs/ktd-asset-catalog.md`](ktd-asset-catalog.md).
