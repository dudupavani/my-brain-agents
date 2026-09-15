# Conteúdo gerado

Este diretório guarda os JSONs e PNGs produzidos pelos sistemas versionados em `projects/`. A estrutura é genérica e começa pelo produto informado no fluxo:

```text
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

`design.source.json` é a cópia imutável recebida do Extract Design. `design.json` é a cópia operacional atualizada pelo Design Renderer. Cada registro em `generatedAssets` aponta para um PNG e preserva `designVersionId` e `generationId`.
