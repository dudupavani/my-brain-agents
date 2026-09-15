# Renderer de design

Este projeto tem um único fluxo: `design.json` + respostas do usuário → um post PNG independente.

O armazenamento é genérico por produto. Para cada execução válida, o JSON recebido precisa conter `designId`, `designVersionId`, `assetBinding` e `generatedAssets`. Pergunte o nome do produto quando ele não estiver definido. Gere um UUID v4 e grave o PNG em `generated-content/{produto}/styles/{designId}/versions/{designVersionId}/posts/{designId}--{generationId}.png`, relativo à raiz do repositório compartilhado. Depois de o PNG ser criado e validado, faça append em `generatedAssets` com `generationId`, `designVersionId` e `path`; nunca remova registros existentes.

Comportamento conversacional obrigatório:

- O recebimento de um `design.json` anexado já inicia o fluxo; não pergunte se o usuário quer renderizar, validar ou revisar.
- Não ofereça um menu de ações depois do anexo. Faça diretamente a próxima pergunta obrigatória.
- A primeira pergunta deve ser exatamente: `Para qual produto devo criar esses posts?`
- Depois que o produto for informado, pergunte: `Escreva o texto do post.`
- Se o texto já tiver sido informado na mesma mensagem, faça apenas uma confirmação curta.
- Depois de receber o texto, use o conteúdo conforme os slots e papéis definidos no JSON e gere imediatamente o post.
- Não faça perguntas adicionais sobre o que fazer, não invente conteúdo e não peça revisão antes de gerar.
- Mantenha o mesmo produto nas gerações seguintes da conversa, até o usuário informar outro.

- Leia `skills/render-design/SKILL.md` antes de alterar ou executar o renderer.
- Não use Pomake ou outro produto como regra fixa, nome de pasta ou arquitetura.
- Trabalhe somente com o `design.json`; nunca reabra, analise ou recupere conteúdo da imagem de referência.
- Use Pillow para composição raster local. Não crie API, interface web, banco de dados, catálogo de templates, carrossel ou agentes adicionais.
- O motor deve interpretar os campos visuais declarados pelo schema (`canvas`, `background`, `bounds`, `zIndex`, `shape`, `image` e `typography`); não trate esses campos como sugestões nem os ignore silenciosamente.
- Uma imagem ausente ou ilegível é erro de renderização: não entregue um PNG aparentemente válido com um slot de foto vazio por acidente.
- Slots nulos de texto recebem somente o conteúdo fornecido pelo usuário. Para cada geração, todo slot nulo de imagem deve receber uma foto nova, criada a partir do texto do post e do papel da imagem; não deixe o espaço vazio. Só produza estado `skipped` quando o usuário disser `ignorar` explicitamente.
- É proibido reutilizar, abrir ou copiar a imagem que serviu de modelo para o JSON. As fotos podem ser inventadas e devem variar conforme o tema de cada post. Use a referência apenas por meio da estrutura já descrita no JSON e mantenha o enquadramento, recorte e posição do slot.
- Não introduza texto padrão, placeholders, imagem substituta nem reposicione elementos para compensar um slot ignorado.
- Preserve texto fornecido, bbox, alinhamento, ordem de camadas e dimensões do canvas. Use o fallback de `1080 × 1350` somente se o JSON não trouxer tamanho.
- A saída deve ser validada com `python3 validator.py <design.json> --answers <respostas.json> --output <imagem>` ou pelo fluxo `render_design.py`.

Uso interativo:

```sh
python3 render_design.py /caminho/design.json
```

Uso não interativo:

```sh
python3 render_design.py /caminho/design.json --answers respostas.json
```

As respostas são um objeto indexado pelo `id` do slot. Use uma string para preencher e `"skipped"` para omitir.
