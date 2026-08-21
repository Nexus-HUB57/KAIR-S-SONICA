# FIRE IN THE FLOOD — status da reconstrução performática

## Estado atual

O projeto está em **`performance_rebuild_required`**. A decupagem temporal continua fechada em 168,000 segundos, com 16 blocos de 10 segundos e um encerramento de 8 segundos, no formato vertical oficial 9:16, 720×1280, 24 fps.

O preview editorial anterior, `artifacts/video/fire-in-the-flood-existing-materials-preview-v5.mp4`, foi mantido apenas como referência de montagem e atmosfera. Ele foi auditado como **mood film sem lip-sync** e não pode ser promovido ao clipe final. O plano `artifacts/video/dynamic-shots/fire-in-the-flood-s01-10s.mp4` também é somente uma prova visual anterior, sem aprovação performática.

## Contrato implementado

A fila `data/releases/fire-in-the-flood-10s-generation-queue-v1.json` foi regenerada como `performance-generation-queue-v1`. Ela contém 17 prompts, com 14 cenas vocais (S01–S14) e 3 cenas instrumentais (S15–S17).

Nas cenas S01–S14, cada prompt exige: canto de KTD em cena; texto exato do bloco; articulação visível de fonemas e sílabas; ataques consonantais; sustentação de vogais; respiração; movimento de mandíbula, garganta e peito; foco ocular; expressão; e gestos conduzidos pela letra. Caminhar ou olhar para a câmera de boca fechada falha no gate.

Nas cenas S15–S17, a fila proíbe inventar letra ou vocalização e exige presença física viva, respiração, olhar, postura, movimento e reação ao ambiente. A master v4 continua sendo adicionada somente na montagem final.

## Referência de identidade

Foi preparado o keyframe `assets/video/keyframes/ktd-fire-in-the-flood-s01-vocal-performance-portrait-keyframe.png`. Ele mostra KTD como referência de performance: microfone prático, boca aberta em articulação, mandíbula e garganta ativas, respiração e intenção emocional. O keyframe é **referência para geração temporal**, nunca quadro final do clipe.

A identidade permanece bloqueada: homem negro adulto, cabeça raspada, barba longa, corpo atlético compacto, olho esquerdo âmbar/mel, olho direito azul-claro, riscos dourados nas sobrancelhas e mapa imutável das tatuagens do Dragão Diamante.

## Validações executadas

O gerador `scripts/build_fire_in_the_flood_10s_queue.py` foi compilado e executado sem erro. O arquivo JSON foi validado. O validador `scripts/validate_fire_in_the_flood_performance_queue.py` confirmou:

| Verificação | Resultado |
|---|---|
| Cenas totais | 17 |
| Cenas com performance vocal | S01–S14 |
| Cenas instrumentais | S15–S17 |
| Lip-sync em nível de fonema exigido | Sim |
| Respiração e ataques consonantais exigidos | Sim |
| Letra exata incluída nos prompts vocais | Sim |
| Vocalização inventada nos trechos instrumentais | Bloqueada |
| Still, slideshow e mood performance silenciosa | Bloqueados |

## Próximo gate operacional

A geração temporal dos planos performáticos deve ocorrer em `generate_audio=False`, com o keyframe portrait correspondente e saída individual em `artifacts/video/dynamic-shots/`. Cada plano precisa ser auditado contra a master v4 antes de entrar no montador. Uma falha de boca fechada, mouthing genérico, identidade instável, ausência de respiração ou gesto não relacionado à frase reprova o plano.

Depois que S01–S17 forem gerados e aprovados humanamente, `scripts/assemble_fire_in_the_flood_10s.py` deve normalizar os planos para 720×1280/24 fps, concatená-los em frames inteiros e fazer mux somente com `assets/audio/releases/ktd-main-single-fire-in-the-flood-v1-reference-aligned-mix-v4.wav`. Nenhum PNG/keyframe ou preview sem lip-sync deve ser usado como material final.

A quota diária de geração de vídeo estava esgotada no momento desta atualização. Por isso, esta etapa entrega o contrato performático, a fila corrigida, o keyframe de referência e os gates de validação sem fabricar planos mudos ou um clipe final enganoso.
