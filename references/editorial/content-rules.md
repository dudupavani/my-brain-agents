# Regras editoriais para carrosséis de notícia e ideia

## Escopo

Este documento regula o fluxo de carrosséis de notícias, novidades de IA e ideias relacionadas a produto. Ele não substitui a estratégia de conteúdo completa nem obriga que todo conteúdo tenha a mesma função.

## Filtro editorial atual

Priorize pautas que ajudem a audiência a perceber, de forma concreta, o que a tecnologia já torna possível e como isso se conecta a produtos, trabalho ou negócios na prática.

O papel do conteúdo é tornar a notícia compreensível e relevante. Uma pauta pode ser apenas uma boa síntese factual; não é obrigatório adicionar opinião, lição ou reflexão.

## Entradas aceitas

- URL de uma notícia ou fonte primária
- Descoberta de pesquisa ou scraping
- Vídeo ou post
- Ideia, conversa ou trabalho atual do usuário

O agente extrai o necessário da entrada e registra no pacote. O usuário não deve preencher um formulário, escolher quantidade de slides ou buscar mídia para cada post.

## Fatos, fontes e linguagem

- Registre a fonte principal, URLs, publicador quando identificável e datas relevantes.
- Separe fatos comprováveis, declarações atribuídas e interpretação. Quando o dado vier de uma fonte, deixe a atribuição clara.
- Não invente contexto, métricas, cronologia, citações, promessas ou conclusões para completar uma narrativa.
- Use citação literal somente quando ela for necessária e puder ser conferida na fonte; prefira síntese fiel.
- Se a fonte estiver inacessível, contraditória ou insuficiente para sustentar a copy, marque o item como `blocked` e explique o motivo.

## Escolha do ângulo e da copy

- Comece pelo que aconteceu e pelo que mudou de forma concreta.
- Escolha o recorte que melhor passa pelo filtro editorial atual, sem distorcer a notícia.
- Para uma notícia, clareza vem antes de uma tese. Só inclua consequências ou leitura própria quando elas forem sustentadas pela fonte ou solicitadas pelo usuário.
- O hook do primeiro slide é uma única frase: desperta interesse sem sensacionalismo e sem ir além do que os fatos permitem.
- A quantidade de slides é definida pela narrativa. Não há número padrão.

## Mídia

- Quando disponível e útil, priorize mídia primária ou oficial: imagens da organização/pessoas envolvidas, telas do produto, gráficos, diagramas e documentos da fonte.
- Mídia precisa provar, explicar ou contextualizar a notícia. Uma imagem sem relação semântica com o assunto não deve ser usada.
- Fotografia real é preferível quando uma foto acrescenta significado. Ilustrações só são apropriadas quando representam diretamente o tema.
- A ausência de mídia útil não bloqueia a pauta: o carrossel pode ter slides tipográficos.
- O agente escolhe a mídia e registra origem, papel editorial e uso por slide em `visual.md`. Isso não é uma tarefa para o usuário.

## Autonomia e passagem de etapa

Quando Eduardo pedir somente estrutura, roteiro ou copy a partir de uma entrada utilizável, o agente deve avançar até `ready_for_design`. Quando pedir um carrossel, deve usar a skill `instagram-carousel` e seguir até `in_review`, incluindo imagens e PNGs finais. Não peça aprovação intermediária; só interrompa diante de bloqueio factual, técnico ou de uma escolha que mude materialmente o conteúdo.
