# Arquitetura de designs e posts do Pomake

Status: v1 implementável

## Objetivo

Persistir no cérebro compartilhado, sem apagar histórico:

- cada JSON produzido pelo Extrator;
- todas as imagens PNG produzidas pelo Renderer;
- o vínculo entre a origem visual, a versão do JSON e cada post.

A arquitetura não altera o Extrator nem o Renderer. O projeto arquiteto faz a ingestão, preserva os artefatos e cria os manifestos do repositório.

## Identificadores

### `designId`

Identifica a imagem de referência e o design de origem. É determinístico:

- a mesma imagem, byte a byte, possui o mesmo SHA-256 e o mesmo `designId`;
- uma imagem diferente possui outro `designId`;
- o projeto arquiteto consulta o repositório para decidir se aquele design já existe;
- nunca deve ser criado um `designId` aleatório para uma nova execução da mesma referência.

### `designVersionId`

Identifica a versão do JSON extraído. O Extrator calcula o valor a partir do JSON canônico, removendo antes `generatedAssets` e o próprio `designVersionId`, e usa o prefixo `version-` com os primeiros 16 caracteres hexadecimais do SHA-256.

O projeto arquiteto preserva esse identificador exatamente como recebeu. Não recalcula uma versão alternativa nem substitui o identificador.

### `generationId`

Identifica uma imagem gerada. É um UUID v4 criado pelo Renderer. Cada PNG recebe um `generationId` próprio, mesmo quando uma única execução produz várias imagens.

Cada PNG é um post independente. Não existe, neste contrato, classificação obrigatória como variação, conjunto ou carrossel.

## Estrutura canônica

```text
domains/products/pomake/
├── designs/
│   └── <designId>/
│       ├── design.source.json
│       ├── design.json
│       └── versions/
│           └── <designVersionId>.source.json
├── generated/
│   └── <designId>/
│       ├── <designId>--<generationId>.png
│       └── <designId>--<generationId>.manifest.json
├── index.json
├── schemas/
│   ├── generation-manifest.schema.json
│   └── index.schema.json
└── scripts/
    ├── build_index.py
    └── validate_repository.py
```

Os diretórios `designs/` e `generated/` são específicos do domínio do Pomake. Eles não substituem `content/items/`, que continua reservado aos pacotes de conteúdo pessoal do Eduardo.

## Papel de cada arquivo

### `design.source.json`

É a cópia exata da primeira saída do Extrator para aquele `designId`. Deve permanecer intocada, inclusive quanto a espaçamento, ordenação e campos que não participam do cálculo do `designVersionId`.

### `versions/<designVersionId>.source.json`

É a cópia exata de cada nova saída do Extrator para o mesmo `designId` quando o `designVersionId` for diferente do original ou de uma versão já arquivada.

O arquivo não deve ser reconstruído a partir de `design.json`. A finalidade é preservar o JSON que o Extrator realmente produziu.

Se o mesmo `designVersionId` reaparecer com conteúdo byte a byte idêntico, a ingestão é idempotente: mantém o arquivo existente e não cria uma cópia artificial. Se reaparecer com bytes diferentes, arquiva a entrada em uma área de conflito, sem substituir a versão ativa, e marca a inconsistência para revisão.

### `design.json`

É o manifesto operacional acumulado do design. O Renderer continua recebendo um arquivo com o formato que já conhece e adiciona registros em `generatedAssets`.

Quando uma nova versão do Extrator chegar, o projeto arquiteto deve:

1. arquivar a saída exata em `design.source.json` ou em `versions/`;
2. criar a cópia operacional a partir da nova versão;
3. carregar os registros históricos de `generatedAssets` do `design.json` anterior;
4. preservar esses registros na nova cópia operacional;
5. chamar o Renderer;
6. salvar o resultado atualizado em `design.json`.

Assim, a evolução do estilo não apaga as gerações anteriores.

### PNG

O caminho registrado pelo Renderer é preservado dentro do domínio do Pomake:

```text
generated/<designId>/<designId>--<generationId>.png
```

O nome usa os identificadores, mas o vínculo oficial não depende apenas dele.

### Manifesto individual do PNG

Cada imagem possui um manifesto no mesmo diretório e com o mesmo identificador:

```text
generated/<designId>/<designId>--<generationId>.manifest.json
```

O manifesto deve conter, no mínimo:

```json
{
  "manifestVersion": 1,
  "designId": "<designId>",
  "designVersionId": "version-<16-hex>",
  "generationId": "<uuid-v4>",
  "designSourcePath": "designs/<designId>/design.source.json",
  "designOperationalPath": "designs/<designId>/design.json",
  "assetPath": "generated/<designId>/<designId>--<generationId>.png",
  "checksums": {
    "sourceJsonSha256": "<sha256>",
    "assetSha256": "<sha256>"
  }
}
```

Para uma versão posterior, `designSourcePath` aponta para `designs/<designId>/versions/<designVersionId>.source.json`.

Esse manifesto resolve a consulta reversa sem depender de inferência pelo nome do arquivo:

```text
PNG → manifesto → designId + designVersionId + generationId
                         ↓
              JSON-fonte exato e JSON operacional
```

O `sourceJsonSha256` e o `assetSha256` protegem contra substituição silenciosa de arquivos. Eles não substituem os identificadores do domínio.

### `index.json`

É um catálogo derivado, gerado pelo projeto arquiteto depois que os arquivos foram validados. Ele facilita encontrar designs e posts pela API do GitHub ou por ferramentas que não querem percorrer todos os diretórios. O arquivo pode ser reconstruído com `scripts/build_index.py --write`.

O índice não é a única fonte de verdade: pode ser reconstruído a partir de `design.json`, das versões-fonte e dos manifestos individuais. Se o índice discordar desses arquivos, a validação falha e ele deve ser regenerado.

## Consultas garantidas

### A partir de `designId`

1. abrir `designs/<designId>/design.json`;
2. ler `generatedAssets`;
3. confirmar cada `path` no diretório `generated/<designId>/`;
4. abrir o manifesto correspondente para descobrir o `designVersionId` de cada PNG.

O `index.json` oferece a mesma navegação em uma única leitura.

### A partir de um PNG

1. localizar o manifesto com o mesmo prefixo e sufixo `.manifest.json`;
2. ler `designId`, `designVersionId` e `generationId` do manifesto;
3. abrir `designSourcePath` para a versão exata do Extrator;
4. abrir `designOperationalPath` para o manifesto acumulado das gerações.

## Regras de duplicata e conflito

| Situação | Tratamento |
| --- | --- |
| Novo `designId` | Criar a pasta, preservar a saída em `design.source.json` e iniciar `design.json`. |
| Mesmo `designId`, novo `designVersionId` | Guardar o novo JSON em `versions/`; nunca substituir a origem anterior. |
| Mesmo `designId` e mesmo `designVersionId`, bytes idênticos | Operação idempotente; manter o arquivo canônico existente. |
| Mesmo `designId` e mesmo `designVersionId`, bytes diferentes | Arquivar em conflito, preservar a versão ativa e falhar a validação. |
| Mesmo `designId`, `source.value.sha256` diferente | Arquivar como entrada inconsistente; não misturar com o design ativo. |
| Mesmo `generationId` e mesmo PNG | Operação idempotente. |
| Mesmo `generationId` com PNG ou manifesto diferente | Arquivar como conflito e falhar a validação. |
| PNG sem registro em `design.json` | Referência quebrada; não entra no commit final. |
| Registro em `generatedAssets` sem PNG | Referência quebrada; não entra no commit final. |
| PNG sem manifesto | Referência reversa incompleta; não entra no commit final. |

Nenhum conflito é resolvido apagando ou sobrescrevendo o artefato original.

## Fluxo de ingestão e commits

O transporte entre os dois projetos continua manual. A ingestão no cérebro segue esta ordem:

1. receber o JSON do Extrator e, quando houver, as PNGs do Renderer;
2. validar `designId`, `designVersionId`, `source.value.sha256`, `generationId` e os caminhos;
3. comparar o `designId` com o que já existe no GitHub;
4. preservar a saída do Extrator como origem ou nova versão;
5. preparar o `design.json` operacional sem perder `generatedAssets` anteriores;
6. chamar ou receber o resultado do Renderer;
7. gerar um manifesto para cada PNG, com o `designVersionId` usado naquela execução;
8. conferir checksums, caminhos e referências nos dois sentidos;
9. reconstruir `index.json`;
10. executar a validação completa;
11. fazer um commit atômico contendo JSONs, PNGs, manifestos e índice;
12. enviar o commit ao remoto autorizado.

Uma execução que produza várias imagens pode gerar vários manifestos no mesmo commit. Cada imagem continua tendo seu próprio `generationId`.

O commit não deve conter somente parte da relação. Um PNG sem manifesto ou um JSON atualizado sem seus novos PNGs deixa o repositório em estado incompleto e deve ser bloqueado antes do commit.

Como vários agentes usam o mesmo GitHub, o fluxo deve começar com `git pull --ff-only`. Se outro agente publicar antes, não se deve fazer merge, rebase, reset ou force-push automaticamente; a operação deve preservar as mudanças e ser reaplicada como uma nova inclusão append-only.

## Limites

- O Extrator continua sendo responsável por `designId` e `designVersionId`.
- O Renderer continua sendo responsável por `generationId`, PNG e registros em `generatedAssets`.
- O projeto arquiteto é responsável pela cópia imutável, versionamento no repositório, manifestos, índice, validação e commits.
- O texto do post e demais dados de conteúdo não alteram a identidade do design, salvo quando o Renderer já os incorporar no resultado visual.
- O repositório não usa o nome visual do design como chave.
- A arquitetura não presume publicação em rede social nem substitui o código-fonte dos dois projetos.
