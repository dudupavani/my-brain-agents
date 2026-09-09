# Templates determinísticos

Os JSONs nesta pasta definem o layout dos slides e são a única fonte de posições, cores, tipografia, gradientes, limites de conteúdo e regras de validação para o renderer.

- `template-01-hook-image-landscape.json`: capa com hook curto e uma imagem horizontal.

Os JPEGs `reference-*.jpg` são referências históricas e visuais de medição. Eles não são enviados a um modelo nem usados como base de reconstrução do layout. Os placeholders presentes neles nunca podem aparecer em um PNG de produção.

Para incluir um template futuro, copie seu JSON para esta pasta e mantenha um `templateId` único. A seleção e a renderização seguem os dados declarados, sem lógica condicionada ao nome do template.
