# Seleção de template

Os JSONs em `assets/templates/` são a fonte exclusiva para escolher e renderizar o layout. Não selecione um template aleatoriamente e não reconstrua sua composição visualmente.

Antes de montar o arquivo de conteúdo do renderer:

1. Consulte `intendedUse` e escolha apenas um template apropriado ao papel narrativo do slide.
2. Confirme que todos os elementos com `required: true` terão conteúdo. Um elemento de imagem exige uma imagem real.
3. Meça cada texto usando a largura, `fontSizePx`, `minimumFontSizePx`, `lineHeightPx` e `maximumLines` do próprio JSON.
4. Use `contentConstraints` como guia de seleção e aplique `overflowAction` quando a copy não couber.

O `templateId` escolhido e o conteúdo entram no arquivo de renderização; posições, cores, tamanhos, tipografia e recortes nunca entram nesse arquivo. A chave de cada valor de conteúdo é `contentKey` no elemento do template — ou o próprio `id` quando esse campo não existir.

Se nenhum template comportar a copy dentro dos limites declarados, a produção para com uma mensagem clara. A etapa editorial pode propor uma versão menor, mas o renderer não pode reescrever, ocultar, sobrepor ou cortar o texto.

Para novos templates, adicione o JSON a `assets/templates/`, use somente tipos de elemento que o renderer suporte e mantenha um `templateId` único. A descoberta é automática: não há condicionais pelo nome do template no código.
