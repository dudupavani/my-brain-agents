# Sistemas versionados no segundo cérebro

Este diretório contém o código-fonte canônico dos dois sistemas do fluxo visual.

- `extract-design/` recebe uma imagem de referência e produz um `design.json`.
- `design-renderer/` recebe esse JSON e o conteúdo do post e produz PNGs.

As pastas locais originais são cópias de trabalho. Não copie diretórios `.git`, `.DS_Store`, caches ou saídas temporárias para cá. Os dois sistemas continuam independentes em responsabilidade, mas compartilham este repositório e seu histórico.

O armazenamento dos JSONs e PNGs gerados fica em `generated-content/`, fora do código dos sistemas. Regras de produto não devem ser codificadas aqui: o Renderer pergunta o produto e usa a pasta correspondente.

Antes de alterar um sistema, preserve alterações locais, valide o fluxo existente e mantenha os testes daquele sistema passando. Não misture arquivos do Extract Design com arquivos do Design Renderer.
