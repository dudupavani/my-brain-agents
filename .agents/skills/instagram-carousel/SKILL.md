---
name: instagram-carousel
description: "Transforme um pacote de conteúdo pronto em um carrossel final para Instagram, usando a marca e as três referências JPEG internas da skill. Use quando um item estiver em ready_for_design; não use para pesquisa ou criação editorial ainda sem copy final."
---

# Instagram Carousel

Crie uma entrega visual original, legível e fiel à copy aprovada. O repositório é a memória compartilhada do fluxo: não dependa de contexto que não esteja registrado nele.

## Referências de design obrigatórias

Antes de criar qualquer slide, abra e analise as três imagens abaixo:

```text
assets/templates/reference-01.jpg
assets/templates/reference-02.jpg
assets/templates/reference-03.jpg
```

Essas três imagens são a fonte visual da skill. Use-as como um sistema de referência: observe a hierarquia, composição, contraste, tipografia, tratamento de imagem, ritmo e uso de cor que elas compartilham ou complementam. Crie uma execução nova; não reproduza uma referência isolada nem copie layouts, textos, logotipos ou imagens.

Se qualquer uma das três imagens estiver ausente, ilegível ou não for JPEG, interrompa a produção e informe o usuário. Não substitua referências, não procure alternativas e não inicie o design sem o conjunto completo.

## Encontrar o trabalho certo

1. Leia `AGENTS.md`, `mapa.md` e `references/brand/brand.md`.
2. Se o usuário fornecer um ID, use apenas `content/items/<id>/`. Caso contrário, encontre um único pacote com `status: ready_for_design`, priorizando `priority` e depois a data de criação.
3. Leia `metadata.yaml`, `brief.md` e `carousel.md` do pacote. Só prossiga se a copy estiver completa, as fontes necessárias estiverem registradas e a quantidade escolhida de slides fizer sentido para a narrativa.
4. Quando informações essenciais faltarem, não preencha lacunas por conta própria. Atualize o item para `blocked`, aponte a necessidade em `handoff.notes` e informe o usuário.

A quantidade de slides é variável. Nunca use 8, ou qualquer outro número, como padrão. Produza apenas os slides necessários para desenvolver a ideia com clareza, sem adicionar telas vazias ou conteúdo de preenchimento.

## Assumir e produzir

1. Antes de criar a arte, atualize `metadata.yaml` para `status: in_production`, `owner: codex` e a data atual. Se a sincronização remota estiver autorizada, registre a assunção em um commit focado.
2. Preserve a copy final. Não altere palavras, números, promessas ou fontes sem pedido do usuário; erros objetivos devem ser sinalizados antes de mudar o conteúdo.
3. Aplique a análise das três referências JPEG obrigatórias para criar uma composição própria, sem reproduzir uma arte existente.
4. Produza um slide por arquivo PNG, em 1080 × 1350 (4:5), na pasta `content/items/<id>/deliverables/`. Nomeie em ordem: `slide-01.png`, `slide-02.png` e assim por diante.
5. Crie `deliverables/caption.md` com a legenda final extraída de `carousel.md`, e `deliverables/design-notes.md` confirmando a consulta às três referências, as decisões visuais e quaisquer limitações materiais.

Ao criar ou revisar a entrega, siga [a lista de qualidade](references/quality-checklist.md).

## Encerrar a entrega

1. Confirme que todos os slides previstos existem, estão ordenados e apresentam exatamente a copy aprovada.
2. Atualize `metadata.yaml` para `status: in_review`, `owner: user`, `updated_at` e uma nota curta de entrega em `handoff.notes`.
3. Revise o conjunto de arquivos alterados. Quando houver um remoto autorizado, faça um commit focado, por exemplo `design(<id>): add carousel deliverables`, e envie-o ao GitHub.

Nunca altere `approved` ou `published`: esses estados pertencem ao usuário.
