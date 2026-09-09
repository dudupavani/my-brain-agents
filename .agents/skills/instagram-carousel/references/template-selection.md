# Seleção de template

`assets/templates/template-registry.json` indica quais JSONs podem ser usados e em que situação. Os templates e o `assets/design-system.json` são a fonte exclusiva do design. Não selecione um template aleatoriamente e não reconstrua sua composição visualmente.

O registry é um repertório de composições. Não existe uma estrutura obrigatória para todos os slides: alguns podem ter título e apoio, outros apenas texto corrido, imagem e apoio, título e imagem ou uma capa com hook. A copy e o papel narrativo decidem quais elementos são necessários.

Antes de montar o arquivo de conteúdo do renderer:

1. Comece pelo papel narrativo e pela composição necessária: título, apoio, imagem, texto corrido ou combinação desses elementos. Depois filtre pelas entradas `useWhen` do registro e pelos `requiredFields` do `contentModel`; um slot de imagem exige uma imagem real.
2. Meça cada texto usando a largura, `fontSizePx`, `minimumFontSizePx`, `lineHeightPx` e `maximumLines` do próprio JSON.
3. Use os limites recomendados de caracteres e palavras somente para decidir entre layouts compatíveis; o limite efetivo é a medição da copy dentro da caixa.
4. Aplique `overflowAction` quando a copy não couber. Se nenhum template servir para a composição necessária, o processo volta para revisão do sistema visual ou editorial; não force um título, um bloco de apoio ou uma imagem que a narrativa não pede.

O `templateId` escolhido e o conteúdo entram no arquivo de renderização; posições, cores, tamanhos, tipografia e recortes nunca entram nesse arquivo. A chave de cada valor de conteúdo é `contentKey` no elemento do template — ou o próprio `id` quando esse campo não existir.

Se nenhum template comportar a copy dentro dos limites declarados, a produção para com uma mensagem clara. A etapa editorial pode propor uma versão menor, mas o renderer não pode reescrever, ocultar, sobrepor ou cortar o texto.

Para novos templates, adicione o JSON a `assets/templates/`, registre-o no índice, use somente tipos de elemento que o renderer suporte e mantenha um `templateId` único. Não há condicionais pelo nome do template no código.
