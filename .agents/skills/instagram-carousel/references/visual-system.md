# Contrato de uso dos templates visuais

Leia este documento na etapa visual da skill e passe diretamente o JPEG escolhido em `../assets/templates/` para a capacidade de criação de cada slide.

## Regra principal

Os três JPEGs são templates executáveis, não apenas inspiração. A imagem original é a fonte da composição. Não a substitua por análise, resumo, lista de princípios, tokens de estilo ou qualquer outro dado estruturado que tente reconstruí-la.

Para cada slide:

1. escolha um dos três JPEGs;
2. envie o arquivo original junto com a copy exata do slide;
3. instrua a capacidade de criação a reproduzir o template;
4. substitua somente os textos, imagens e outros placeholders pelo conteúdo real.

Preserve a composição, a hierarquia, a tipografia, as cores, o espaçamento, as proporções, o alinhamento e a posição relativa dos elementos. Adaptações de quebra de linha, recorte ou altura só são permitidas quando necessárias para acomodar o conteúdo e não podem criar uma composição nova.

As caixas cinzas e os textos de exemplo presentes nos JPEGs são placeholders: substitua-os quando representarem conteúdo variável e remova-os quando forem apenas marcação. Elementos fixos da composição, como setas, divisores, cantos e blocos, devem permanecer. Nunca deixe placeholders na entrega.

## Conteúdo e hierarquia

- A capa possui uma frase de hook e nenhum texto concorrente. Ela deve ser o primeiro conteúdo textual percebido e o maior peso visual do slide.
- Cada slide tem um único foco. Headline e corpo podem coexistir, mas não podem parecer duas chamadas independentes.
- Use margens generosas, alinhamento consistente e tamanho de texto legível em tela pequena.
- Se a copy não couber sem comprometer a hierarquia, edite a copy ou distribua a narrativa em outro slide. Não reduza a tipografia até caber.
- Não acrescente número do slide, assinatura, logotipo, cartão ou etiqueta que não existam no template escolhido ou não tenham função real prevista no conteúdo.

## Mídia

Priorize, nesta ordem:

1. mídia primária da fonte ou do produto, quando o uso for permitido;
2. fotografia real da pessoa, empresa, objeto ou contexto envolvido;
3. interface, gráfico ou diagrama que explique o ponto;
4. imagem original gerada especificamente para representar o assunto;
5. nenhuma mídia, quando um slide tipográfico comunicar melhor.

Uma imagem precisa provar, explicar ou contextualizar. Não use banco de imagem genérico, robôs abstratos, cérebros luminosos, código decorativo nem ilustrações desconectadas do texto.

Registre a origem e não presuma direito de uso. Quando a permissão de uma mídia externa estiver incerta, prefira uma imagem original gerada para o assunto ou um slide tipográfico.

Ao gerar um asset, descreva assunto, enquadramento, iluminação, composição e atmosfera. Solicite uma imagem sem palavras, sem letras legíveis, sem títulos e sem layout de post. O espaço negativo pode ser planejado para a composição, mas o gerador não deve desenhar caixas de texto.

## Contrato do renderer

O `carousel.md` é a fonte única do texto. O `visual.md` é a fonte das decisões visuais.

O renderer ou software de criação deve:

- receber a imagem da referência diretamente, sem depender de uma reconstrução textual da composição;
- aplicar o texto sem reescrever a copy aprovada;
- produzir PNG raster de 1080 × 1350 pixels;
- controlar fonte, peso, entrelinha, largura de coluna, alinhamento, cor, posição, recorte e contraste;
- manter o conteúdo dentro da área segura e sem cortes;
- usar os assets como imagem, nunca como portadores da copy;
- permitir correção e nova renderização sem regenerar o conteúdo editorial.

HTML/CSS capturado em PNG ou um compositor raster já disponível são opções válidas quando preservarem o template escolhido. SVG não é entrega e não deve ser usado como atalho para substituir a criação do slide.

Se o ambiente não oferecer uma capacidade que aceite a referência diretamente e preserve a copy, a produção está bloqueada. Não tente reconstruir o slide a partir de uma análise textual da imagem.
