# Sistema visual determinístico

Os layouts da skill são dados declarativos em `assets/templates/*.json`. O renderer Pillow usa esses dados diretamente; nem um modelo de imagem nem um compositor manual pode reconstruir ou improvisar o layout.

Leia [a seleção de templates](template-selection.md) antes de decidir o `templateId`. O `carousel.md` continua sendo a única fonte da copy e o `visual.md` registra a escolha do template e a origem da mídia.

O arquivo `assets/design-system.json` centraliza a fonte por token. Se a fonte configurada estiver ausente, a renderização deve falhar explicitamente — nunca recorrer a uma fonte de sistema.

Uma geração de imagem pode fornecer apenas uma fotografia ou ilustração para um slot `image`. Ela não pode criar texto, layout, placeholder ou decoração de slide.
