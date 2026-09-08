# Sistema visual e contrato de renderização

Leia este documento na etapa visual da skill e abra os três JPEGs em `../assets/templates/` antes de definir layouts.

## O que as referências estabelecem

As referências formam três famílias complementares, não três slides obrigatórios:

1. **Capa com mídia**: imagem semanticamente relevante, contraste alto e uma única frase de hook como elemento tipográfico dominante.
2. **Texto**: hierarquia forte entre a ideia principal e o desenvolvimento, com uso de azul, branco e fundo escuro para organizar a leitura.
3. **Texto com mídia**: headline clara acompanhada por fotografia, interface, gráfico ou ilustração que acrescente informação.

O vocabulário comum é tipografia sans-serif contemporânea, contraste alto, azul intenso, carvão, branco, áreas amplas, cantos arredondados e composição limpa. O resultado pode variar entre slides, mas deve parecer parte do mesmo conjunto.

As caixas cinzas, textos de exemplo e setas presentes nos JPEGs são indicações de estrutura. Não os reproduza automaticamente. Nunca deixe marcações, caixas vazias, texto de placeholder ou mídia repetida na entrega.

## Hierarquia

- A capa possui uma frase de hook e nenhum texto concorrente. Ela deve ser o primeiro conteúdo textual percebido e o maior peso visual do slide.
- Cada slide tem um único foco. Headline e corpo podem coexistir, mas não podem parecer duas chamadas independentes.
- Use margens generosas, alinhamento consistente e tamanho de texto legível em tela pequena.
- Se a copy não couber sem comprometer a hierarquia, edite a copy ou distribua a narrativa em outro slide. Não reduza a tipografia até caber.
- Não acrescente número do slide, assinatura, logotipo, cartão, etiqueta ou seta sem função real e sem previsão no plano visual.

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

O renderer deve:

- aplicar o texto de forma determinística, sem reescrever ou redesenhar letras;
- produzir PNG raster de 1080 × 1350 pixels;
- controlar fonte, peso, entrelinha, largura de coluna, alinhamento, cor, posição, recorte e contraste;
- manter o conteúdo dentro da área segura e sem cortes;
- usar os assets como imagem, nunca como portadores da copy;
- permitir correção e nova renderização sem regenerar o conteúdo editorial.

HTML/CSS capturado em PNG ou um compositor raster já disponível são opções válidas. SVG não é entrega e não deve ser usado como atalho para substituir o renderer solicitado.

Se o ambiente não oferecer composição determinística, a produção está bloqueada. Não use um gerador de imagem para simular o slide com texto.
