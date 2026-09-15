# Extract Design

Sistema responsável por receber uma imagem JPG ou PNG e produzir um único `design.json` válido, sem armazenar o texto visível da referência.

Uso:

```sh
python3 extractor.py /caminho/referencia.png --output outputs/design.json
python3 validator.py outputs/design.json
python3 -m unittest discover -s tests -p 'test_*.py'
```

O código calcula de forma determinística o `designId` a partir do SHA-256 da imagem e o `designVersionId` a partir do JSON canônico sem `generatedAssets` e sem o próprio `designVersionId`. Este sistema não gera posts e não grava resultados no GitHub durante a extração.
