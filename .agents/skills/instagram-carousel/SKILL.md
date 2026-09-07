---
name: instagram-carousel
description: "Transforme um pacote de conteúdo pronto em um carrossel final para Instagram, usando a marca e referências visuais do repositório. Use quando um item estiver em ready_for_design; não use para pesquisa ou criação editorial ainda sem copy final."
---

# Instagram Carousel

Crie uma entrega visual original, legível e fiel à copy aprovada. O repositório é a memória compartilhada do fluxo: não dependa de contexto que não esteja registrado nele.

## Encontrar o trabalho certo

1. Leia `AGENTS.md`, `mapa.md`, `references/brand/brand.md` e `references/design/index.md`.
2. Se o usuário fornecer um ID, use apenas `content/items/<id>/`. Caso contrário, encontre um único pacote com `status: ready_for_design`, priorizando `priority` e depois a data de criação.
3. Leia `metadata.yaml`, `brief.md` e `carousel.md` do pacote. Só prossiga se a copy estiver completa, as fontes necessárias estiverem registradas e o número de slides fizer sentido para a narrativa.
4. Quando informações essenciais faltarem, não preencha lacunas por conta própria. Atualize o item para `blocked`, aponte a necessidade em `handoff.notes` e informe o usuário.

## Assumir e produzir

1. Antes de criar a arte, atualize `metadata.yaml` para `status: in_production`, `owner: codex` e a data atual. Se a sincronização remota estiver autorizada, registre a assunção em um commit focado.
2. Preserve a copy final. Não altere palavras, números, promessas ou fontes sem pedido do usuário; erros objetivos devem ser sinalizados antes de mudar o conteúdo.
3. Consulte somente as referências visuais relevantes listadas no índice. Use seus princípios para uma composição própria, sem reproduzir uma arte existente.
4. Produza um slide por arquivo PNG, em 1080 × 1350 (4:5), na pasta `content/items/<id>/deliverables/`. Nomeie em ordem: `slide-01.png`, `slide-02.png` e assim por diante.
5. Crie `deliverables/caption.md` com a legenda final extraída de `carousel.md`, e `deliverables/design-notes.md` com as referências consultadas, decisões visuais e quaisquer limitações materiais.

Ao criar ou revisar a entrega, siga [a lista de qualidade](references/quality-checklist.md).

## Encerrar a entrega

1. Confirme que todos os slides previstos existem, estão ordenados e apresentam exatamente a copy aprovada.
2. Atualize `metadata.yaml` para `status: in_review`, `owner: user`, `updated_at` e uma nota curta de entrega em `handoff.notes`.
3. Revise o conjunto de arquivos alterados. Quando houver um remoto autorizado, faça um commit focado, por exemplo `design(<id>): add carousel deliverables`, e envie-o ao GitHub.

Nunca altere `approved` ou `published`: esses estados pertencem ao usuário.
