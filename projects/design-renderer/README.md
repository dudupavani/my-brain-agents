# Design Renderer

Sistema responsável por receber um `design.json` e o conteúdo do post, preencher os slots e gerar um PNG independente.

Uso interativo:

```sh
python3 render_design.py /caminho/design.json
```

Uso não interativo:

```sh
python3 render_design.py /caminho/design.json --answers respostas.json --product "Nome do produto"
```

O armazenamento canônico fica na raiz do segundo cérebro, em `generated-content/`. O Renderer preserva o JSON de origem como `design.source.json`, mantém o manifesto operacional em `design.json`, cria um UUID v4 por PNG e registra cada geração em `generatedAssets`. O produto é uma pasta informada pelo usuário, sem regra específica para Pomake.

Testes:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
```
