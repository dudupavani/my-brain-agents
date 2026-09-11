# Pomake

Registro versionado dos designs e dos posts PNG gerados pelo Design Renderer.

## Estrutura canônica

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

`design.source.json` preserva byte a byte o JSON recebido e nunca é alterado. `design.json` é a cópia operacional, usada pelo Renderer para adicionar registros em `generatedAssets`.

Cada registro tem `generationId`, `designVersionId` e o caminho relativo do PNG. Cada PNG é um post independente; o índice é derivado dos `design.json` operacionais e pode ser reconstruído sem manifestos ao lado das imagens.

Para reconstruí-lo e validar o repositório:

```bash
python3 domains/products/pomake/scripts/build_index.py --write
python3 domains/products/pomake/scripts/validate_repository.py
```
