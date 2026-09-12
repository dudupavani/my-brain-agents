# Pomake

Conhecimento durável, pesquisas, decisões, especificações e links canônicos do Pomake.

## Arquitetura dos designs e posts gerados

O fluxo visual do Pomake usa dois projetos separados no Codex Desktop:

1. o Extrator recebe uma imagem de referência e produz um `design.json`;
2. o Renderer recebe esse JSON e o conteúdo do post e produz uma ou mais imagens PNG.

A arquitetura para persistir esses artefatos no cérebro compartilhado está documentada em [design-post-architecture.md](design-post-architecture.md).

O repositório preserva três relações:

- `designId` identifica a imagem de referência e o design de origem;
- `designVersionId` identifica a versão do JSON extraído que foi usada;
- `generationId` identifica cada PNG, que é tratado como um post independente.

O vínculo reverso de cada PNG fica em um manifesto ao lado da imagem. O nome do arquivo facilita a navegação, mas não é a única fonte de verdade.

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
└── scripts/
```

`design.source.json` é a primeira saída exata do Extrator e nunca é sobrescrito. `design.json` é a cópia operacional que o Renderer pode alterar com novos registros em `generatedAssets`. Versões posteriores do JSON ficam em `versions/`.

`index.json` é um índice derivado para navegação e busca. A relação canônica também deve ser verificável a partir do `design.json` e dos manifestos individuais.

Para reconstruí-lo depois de uma ingestão, use:

```bash
python3 domains/products/pomake/scripts/build_index.py --write
python3 domains/products/pomake/scripts/validate_repository.py
```
