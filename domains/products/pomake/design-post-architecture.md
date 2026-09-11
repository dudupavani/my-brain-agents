# Arquitetura de designs e posts do Pomake

Status: v1 implementável

## Objetivo

Persistir no cérebro compartilhado, sem apagar histórico:

- cada JSON produzido pelo Extrator;
- todas as imagens PNG produzidas pelo Renderer;
- o vínculo entre a origem visual, a versão do JSON e cada post.

A arquitetura não altera o Extrator. O Renderer faz a ingestão, preserva os artefatos, registra os PNGs e reconstrói o índice no repositório.

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

## Estrutura canônica atual

```text
domains/products/pomake/
├── designs/
│   └── <designId>/
│       └── versions/
│           └── <designVersionId>/
│               ├── design.source.json
│               └── design.json
├── generated/
│   └── <designId>/
│       └── <designId>--<generationId>.png
└── index.json
```

Os diretórios `designs/` e `generated/` são específicos do domínio do Pomake. Eles não substituem `content/items/`, que continua reservado aos pacotes de conteúdo pessoal do Eduardo. Cada execução gera um post independente.

## Papel de cada arquivo

### `design.source.json`

É a cópia exata, byte a byte, do JSON recebido para aquele `designVersionId`. Deve permanecer intocada, inclusive quanto a espaçamento, ordenação e campos que não participam do cálculo do `designVersionId`.

### `versions/<designVersionId>/design.source.json`

É a cópia exata de cada saída do Extrator para o mesmo `designId` e `designVersionId`.

O arquivo não deve ser reconstruído a partir de `design.json`. A finalidade é preservar o JSON que o Extrator realmente produziu.

Se o mesmo `designVersionId` reaparecer com conteúdo byte a byte idêntico, a ingestão é idempotente: mantém o arquivo existente e não cria uma cópia artificial. Se reaparecer com bytes diferentes, arquiva a entrada em uma área de conflito, sem substituir a versão ativa, e marca a inconsistência para revisão.

### `design.json`

É o manifesto operacional acumulado do design. O Renderer continua recebendo um arquivo com o formato que já conhece e adiciona registros em `generatedAssets`.

Quando uma nova versão do Extrator chegar, o Renderer deve:

1. arquivar a saída exata como `design.source.json` na pasta da versão;
2. criar `design.json` como cópia operacional;
3. usar o `design.json` daquela versão;
4. adicionar os novos registros somente nessa versão.

Assim, a evolução do estilo não apaga as gerações anteriores.

### PNG

O caminho registrado pelo Renderer é preservado dentro do domínio do Pomake:

```text
generated/<designId>/<designId>--<generationId>.png
```

O vínculo oficial fica em `generatedAssets` no `design.json` da versão e no `index.json` derivado.

### Vínculo do PNG

Não existe manifesto individual ao lado do PNG nesta estrutura. Cada imagem é vinculada diretamente pelo registro em `generatedAssets`:

```json
{
  "generationId": "<uuid-v4>",
  "designVersionId": "<designVersionId>",
  "path": "generated/<designId>/<designId>--<generationId>.png"
}
```

O `index.json` é reconstruído a partir desses registros e dos arquivos de cada versão.

### `index.json`

É um catálogo derivado, gerado pelo projeto arquiteto depois que os arquivos foram validados. Ele facilita encontrar designs e posts pela API do GitHub ou por ferramentas que não querem percorrer todos os diretórios. O arquivo pode ser reconstruído com `scripts/build_index.py --write`.

O índice não é a única fonte de verdade: pode ser reconstruído a partir de `design.json` e das versões-fonte. Se o índice discordar desses arquivos, a validação falha e ele deve ser regenerado.

## Consultas garantidas

### A partir de `designId`

1. abrir todas as pastas em `designs/<designId>/versions/`;
2. ler o `generatedAssets` de cada `design.json`;
3. confirmar cada `path` no diretório `generated/<designId>/`.

O `index.json` oferece a mesma navegação em uma única leitura.

### A partir de um PNG

1. ler `designId` e `generationId` no caminho/nome;
2. consultar `index.json` e localizar o `designVersionId`;
3. abrir o `design.source.json` e o `design.json` da versão correspondente.

## Regras de duplicata e conflito

| Situação | Tratamento |
| --- | --- |
| Novo `designId` | Criar `designs/<designId>/versions/<designVersionId>/`, preservar a saída em `design.source.json` e iniciar `design.json`. |
| Mesmo `designId`, novo `designVersionId` | Guardar o novo JSON na nova pasta de versão; nunca substituir versões anteriores. |
| Mesmo `designId` e mesmo `designVersionId`, bytes idênticos | Operação idempotente; manter o arquivo canônico existente. |
| Mesmo `designId` e mesmo `designVersionId`, bytes diferentes | Arquivar em conflito, preservar a versão ativa e falhar a validação. |
| Mesmo `designId`, `source.value.sha256` diferente | Arquivar como entrada inconsistente; não misturar com o design ativo. |
| Mesmo `generationId` e mesmo PNG | Operação idempotente. |
| Mesmo `generationId` com PNG ou registro diferente | Arquivar como conflito e falhar a validação. |
| PNG sem registro em `design.json` | Referência quebrada; não entra no commit final. |
| Registro em `generatedAssets` sem PNG | Referência quebrada; não entra no commit final. |

Nenhum conflito é resolvido apagando ou sobrescrevendo o artefato original.

## Fluxo de ingestão e commits

O transporte entre os dois projetos continua manual. A ingestão no cérebro segue esta ordem:

1. receber o JSON do Extrator e, quando houver, as PNGs do Renderer;
2. validar `designId`, `designVersionId`, `source.value.sha256`, `generationId` e os caminhos;
3. comparar o `designId` e o `source.value.sha256` com o que já existe no GitHub;
4. preservar a saída do Extrator como origem da pasta da versão;
5. preparar o `design.json` operacional daquela versão;
6. chamar ou receber o resultado do Renderer;
7. registrar cada PNG em `generatedAssets`, com o `designVersionId` usado;
8. conferir caminhos e referências nos dois sentidos;
9. reconstruir `index.json`;
10. executar a validação completa;
11. fazer um commit atômico contendo JSONs, PNGs e índice;
12. enviar o commit ao remoto autorizado.

Uma solicitação que peça várias imagens deve ser processada uma por vez. Cada imagem continua tendo seu próprio `generationId` e registro independente.

O commit não deve conter somente parte da relação. Um PNG sem registro ou um JSON atualizado sem seus novos PNGs deixa o repositório em estado incompleto e deve ser bloqueado antes do commit.

Como vários agentes usam o mesmo GitHub, o fluxo deve começar com `git pull --ff-only`. Se outro agente publicar antes, não se deve fazer merge, rebase, reset ou force-push automaticamente; a operação deve preservar as mudanças e ser reaplicada como uma nova inclusão append-only.

## Limites

- O Extrator continua sendo responsável por `designId` e `designVersionId`.
- O Renderer continua sendo responsável por `generationId`, PNG e registros em `generatedAssets`.
- O Renderer é responsável pela cópia imutável, versionamento no repositório, índice, validação e commits.
- O texto do post e demais dados de conteúdo não alteram a identidade do design, salvo quando o Renderer já os incorporar no resultado visual.
- O repositório não usa o nome visual do design como chave.
- A arquitetura não presume publicação em rede social nem substitui o código-fonte dos dois projetos.
