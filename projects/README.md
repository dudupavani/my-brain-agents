# Sistemas

Os dois sistemas que compõem o fluxo visual ficam versionados no segundo cérebro, em pastas separadas:

- [`extract-design/`](extract-design/): extrai a estrutura visual de uma imagem e gera o JSON de estilo.
- [`design-renderer/`](design-renderer/): usa o JSON e o conteúdo informado para gerar posts PNG.

Eles não são agentes e não são um único programa. Cada pasta tem sua própria entrada, saída, testes e instruções. O vínculo entre JSONs e posts gerados fica em [`generated-content/`](../generated-content/), seguindo a arquitetura genérica registrada em [`architecture/design-post-registry.md`](../architecture/design-post-registry.md).
