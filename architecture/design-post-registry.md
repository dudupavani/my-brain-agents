# Arquitetura genérica dos sistemas de design e posts

Status: ativa

Esta arquitetura vale para qualquer produto. Pomake é apenas um exemplo de produto; não existe uma estrutura exclusiva para ele.

## Os dois sistemas

Os sistemas são independentes e ficam versionados em pastas separadas dentro de `projects/`:

- `projects/extract-design/`: recebe uma imagem de referência e produz um `design.json` que descreve o estilo visual.
- `projects/design-renderer/`: recebe esse JSON e o conteúdo informado pelo usuário e produz um ou mais PNGs. Cada PNG é um post independente.

O transporte do JSON entre os dois sistemas continua sendo manual. O Extract Design não precisa consultar o GitHub durante a extração. O Design Renderer é responsável por armazenar a entrada, gerar os posts e registrar o resultado no segundo cérebro.

## Identificadores

- `designId` identifica o design de origem. É calculado deterministicamente pelo Extract Design a partir do SHA-256 da imagem de referência.
- `designVersionId` identifica a versão exata do JSON extraído. O Extract Design calcula esse valor a partir do JSON canônico, excluindo `generatedAssets` e o próprio `designVersionId`.
- `generationId` identifica uma geração específica. O Design Renderer cria um UUID v4 diferente para cada PNG.

O Design Renderer preserva os três identificadores exatamente como recebidos ou gerados. Ele não cria outro `designId` nem outro `designVersionId`.

## Estrutura canônica

O código dos sistemas e os resultados gerados ficam no mesmo repositório, mas em áreas separadas:

```text
projects/
├── extract-design/
└── design-renderer/

generated-content/
└── <produto>/
    └── styles/
        └── <designId>/
            └── versions/
                └── <designVersionId>/
                    ├── design.source.json
                    ├── design.json
                    └── posts/
                        └── <designId>--<generationId>.png
```

Não existem repositórios Git aninhados dentro de `projects/`. Os diretórios `.git`, caches, `.DS_Store` e saídas temporárias das pastas locais não fazem parte do código canônico.

## O JSON e o vínculo com os posts

Quando o Renderer recebe um JSON:

1. valida `designId`, `designVersionId`, `source.value.sha256`, `assetBinding` e `generatedAssets`;
2. pergunta o produto quando ele ainda não foi definido na conversa;
3. cria, se necessário, a pasta desse produto;
4. copia os bytes recebidos para `design.source.json`;
5. cria ou reutiliza `design.json` como cópia operacional;
6. gera cada PNG dentro da pasta da versão;
7. somente depois de validar cada PNG, acrescenta um registro em `design.json`.

O registro de cada post tem este formato mínimo:

```json
{
  "generationId": "<uuid-v4>",
  "designVersionId": "<designVersionId>",
  "path": "generated-content/<produto>/styles/<designId>/versions/<designVersionId>/posts/<designId>--<generationId>.png"
}
```

`design.source.json` nunca é alterado. `design.json` acumula os registros e nunca perde gerações anteriores.

O vínculo é reversível sem depender apenas do nome visual:

- design → posts: abrir a versão correspondente de `design.json` e ler `generatedAssets`;
- post → design: usar o caminho da pasta para localizar produto, `designId` e `designVersionId`, usar o nome para localizar `generationId` e confirmar o registro em `design.json`.

## Reutilização, versões e conflitos

- Mesmo JSON novamente: reutilizar a mesma versão e apenas acrescentar novos posts.
- Mesmo `designId` com novo `designVersionId`: criar outra pasta de versão; não misturar os registros.
- Mesmo `designVersionId` com bytes diferentes: preservar a entrada em `conflicts/` e interromper a operação.
- `source.value.sha256` incompatível com as versões existentes daquele `designId`: preservar a entrada como conflito e interromper.
- PNG ausente, inválido, sem registro ou com registro apontando para outro caminho: bloquear o commit.
- Gerações anteriores nunca são apagadas ou substituídas.

Não há catálogo global, banco de dados ou manifesto paralelo obrigatório. A estrutura de pastas e `generatedAssets` são suficientes para a navegação e mantêm a solução pequena.

## GitHub e operação

O segundo cérebro é a fonte oficial do código e dos resultados. Os dois sistemas podem ter pastas locais de trabalho, mas a cópia canônica é `projects/` neste repositório.

Antes de uma alteração, o checkout do segundo cérebro deve ser atualizado com `git pull --ff-only`. Um agente não deve fazer merge, rebase, reset ou force push para resolver divergências. Alterações de código entram em commit próprio; uma geração de posts deve ser commitada somente depois da validação completa de JSONs, PNGs e vínculos.

O Design Renderer deve confirmar o push. Se o push falhar, a execução não é concluída e o agente deve informar o erro claramente.

## Fora do escopo

Esta arquitetura não cria publicação em redes sociais, calendário editorial, banco de dados, catálogo de templates, carrossel, variações de post ou regras específicas de Pomake.
