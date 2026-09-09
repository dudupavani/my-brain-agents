# Sistema visual determinístico

Os layouts da skill são dados declarativos em `assets/templates/*.json`, selecionados por `assets/templates/template-registry.json`. O renderer Pillow usa esses dados diretamente; nem um modelo de imagem nem um compositor manual pode reconstruir ou improvisar o layout.

Leia [a seleção de templates](template-selection.md) antes de decidir o `templateId`. O `carousel.md` continua sendo a única fonte da copy e o `visual.md` registra a escolha do template e a origem da mídia.

## Seleção semântica de mídia

O renderer não escolhe imagens: ele apenas desenha o caminho recebido no `render-input.json`. A seleção acontece antes da renderização e precisa ser auditável.

- Para uma URL ou pacote com várias imagens, inspecione o conjunto de assets oficiais disponíveis e registre no `visual.md` o que cada imagem representa.
- Relacione cada imagem ao ponto específico do slide. Uma imagem só entra quando mostra, prova ou contextualiza a copy daquele slide.
- Não escolha uma imagem apenas porque ela é bonita, tem a proporção certa, foi a primeira encontrada ou combina com a paleta.
- Wallpapers, avatares e imagens abstratas só são adequados quando o slide fala explicitamente de ambiente visual, identidade, presença ou sistema gráfico.
- Se não houver uma imagem semanticamente útil, prefira um template tipográfico. Um slot preenchido com mídia genérica enfraquece a narrativa.

O arquivo `assets/design-system.json` centraliza a fonte por token. Se a fonte configurada estiver ausente, a renderização deve falhar explicitamente — nunca recorrer a uma fonte de sistema.

Uma geração de imagem pode fornecer apenas uma fotografia ou ilustração para um slot `image`. Ela não pode criar texto, layout, placeholder ou decoração de slide.
