# Templates determinísticos

Os JSONs nesta pasta definem o layout dos slides e são a única fonte de posições, cores, tipografia, gradientes, limites de conteúdo e regras de validação para o renderer. `template-registry.json` é o índice obrigatório de seleção.

- `template-01-hook-image-landscape.json`: capa com hook curto e uma imagem horizontal.
- `template-02-hook-support-panel.json`: hook com texto de apoio em painel editorial.
- `template-03-image-support-text.json`: imagem superior e texto explicativo.
- `template-04-longform-text.json`: texto corrido, sem imagem.
- `template-05-centered-title-tall-image.json`: título curto com imagem vertical sangrada.

Para incluir um template futuro, copie seu JSON para esta pasta, registre-o em `template-registry.json` e mantenha um `templateId` único. A renderização segue os dados declarados, sem lógica condicionada ao nome do template.
