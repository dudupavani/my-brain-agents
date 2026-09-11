---
name: instagram-carousel
description: "Transforme conteúdo, URL ou pacote existente em um carrossel final para o feed do Instagram: selecione os pontos essenciais, escreva a copy, planeje e gere imagens relevantes, renderize o texto com precisão e entregue PNGs 1080 × 1350. Use quando Eduardo pedir para criar ou fazer um carrossel; não use para mera análise, brainstorm ou publicação."
---

# Instagram Carousel

Conduza o carrossel de ponta a ponta dentro do agente `personal-content`. O usuário fornece o conteúdo ou indica sua origem; a skill resolve o restante sem briefing manual nem aprovação entre etapas.

## Contexto obrigatório

Antes de trabalhar, leia:

1. `AGENTS.md` e `agents/personal-content/README.md`;
2. `content/AGENTS.md`;
3. `references/brand/brand.md`;
4. `references/editorial/content-system.md`;
5. `references/editorial/content-rules.md` quando a entrada envolver notícia, novidade de IA, fonte externa ou ideia relacionada a produto;
6. os modelos em `content/templates/`.

Se houver item existente, leia todos os seus arquivos antes de alterá-lo. Campos ainda indefinidos nas referências não autorizam invenções.

## Resolver a entrada

Use, nesta ordem, o que estiver inequivocamente indicado no pedido:

1. item ou caminho informado pelo usuário;
2. conteúdo ou URL fornecido na conversa atual;
3. um único item compatível já existente em `content/items/`.

Se houver mais de um conteúdo possível e a escolha mudar materialmente o resultado, pergunte qual usar. Uma solicitação para analisar, resumir ou conversar sobre algo não autoriza criar um carrossel.

Quando o pedido for para criar o carrossel completo, avance até os PNGs finais no mesmo trabalho. Só interrompa por falta de fonte essencial, ambiguidade material, ausência das referências obrigatórias ou indisponibilidade de uma capacidade técnica indispensável. Não configure ferramentas, instale dependências nem publique o conteúdo por conta própria.

### Regra inegociável: adaptar, não criar outro conteúdo

Quando Eduardo fornecer uma URL, artigo, vídeo, documento ou post para virar carrossel, esse material é o objeto do conteúdo. O trabalho é adaptar o conteúdo original para slides, não usá-lo como repertório, inspiração ou evidência para criar uma tese nova.

Preserve o assunto específico, a promessa editorial e a estrutura que torna a fonte reconhecível. Um ângulo pode organizar, resumir, agrupar e tornar a explicação mais interessante; não pode trocar o núcleo por uma reflexão genérica, uma opinião paralela ou uma ideia que serviria para qualquer fonte do mesmo tema. Só trate uma fonte como inspiração quando Eduardo pedir isso explicitamente.

## 1. Ler e entender a fonte

1. Crie ou retome `content/items/<id>/` e use `status: draft` durante a apuração.
2. Leia e interprete o conteúdo utilizável antes de escolher assunto, recorte, narrativa, copy ou imagens. Para uma URL, extraia o corpo do material, procure a origem primária quando necessário e confira fatos, nomes, números e datas. Não infira o assunto apenas pelo título, snippet, imagem de capa, resumo externo ou conhecimento prévio. Se o conteúdo estiver inacessível ou incompleto a ponto de impedir essa compreensão, use `blocked`.
3. Registre em `brief.md` um mapa fiel da fonte: síntese do conteúdo, assunto específico, promessa editorial, formato central, argumento principal, tópicos importantes, exemplos que sustentam esses tópicos e limites do que a fonte afirma.
4. Separe os tópicos em núcleo obrigatório, apoio útil e detalhe secundário. Um tópico é obrigatório quando sua ausência faria o leitor deixar de reconhecer o assunto ou não receber a promessa da fonte. Nunca trate como detalhe um elemento que define uma lista, framework, estudo de caso, comparação, lançamento, tutorial ou argumento.
5. Mapeie cada tópico obrigatório para a forma como será preservado nos slides. Em fontes com muitos itens, agrupe itens relacionados em uma formulação curta ou lista legível; não invente categorias que mudem seu sentido e não prometa cobertura exaustiva quando estiver mostrando apenas exemplos.
6. Identifique uma ideia central que sintetize fielmente a fonte para o público do Eduardo. Escolha um ângulo que defina como contar essa ideia; o ângulo não pode trocar o assunto por uma tese genérica, uma opinião paralela ou uma reflexão que serviria para outra fonte.
7. Registre fatos verificáveis, declarações atribuídas e interpretações editoriais separadamente. Não transforme notícia em opinião obrigatoriamente.

## 2. Condensar para a comunicação do Instagram

### Gate editorial: fonte entendida antes da copy

O carrossel deve ter **6 ou 7 slides, nunca mais de 7**, salvo autorização explícita do Eduardo. O limite não autoriza distorcer a fonte: exige agrupar tópicos relacionados, cortar detalhes secundários e escolher a sequência mais eficiente para a promessa original. Se o conteúdo não couber, não aumente a quantidade; refine o recorte dentro do núcleo obrigatório.

Antes de qualquer design, escreva a linha editorial em `brief.md`:

- promessa: o que o leitor entenderá ao terminar;
- tensão: qual problema, mudança ou pergunta move a sequência;
- progressão: como a história sai do hook e chega à conclusão;
- consequência: por que isso importa para este público;
- takeaway: qual ideia permanece depois do último slide.

Para cada slide, registre o papel narrativo, a pergunta respondida, o tópico da fonte preservado e a ponte para o próximo. A sequência precisa ser compreensível sem legenda, resumível em uma frase e específica desta fonte. Se a mesma narrativa servir para outro conteúdo do mesmo tema, ela está genérica demais.

1. Faça o slide 1 apresentar o assunto e a tensão em uma única frase curta. O assunto deve aparecer no hook ou em uma etiqueta prevista pelo template.
2. Escreva cada slide para leitura rápida: uma ideia principal, frases curtas, linguagem concreta e sem introduções, justificativas ou metacomentários desnecessários.
3. Não escreva “o artigo mostra”, “segundo a fonte”, “neste estudo” ou equivalentes dentro dos slides. A fonte orienta a copy, mas a comunicação fala diretamente com o público. Atribuições só aparecem quando forem indispensáveis para não apresentar uma alegação da fonte como fato universal, e podem ficar na legenda.
4. Cada slide deve avançar a mesma história. Não use slides para reproduzir capítulos do artigo, empilhar estatísticas ou preencher uma lista sem contexto.
5. Um slide só com título é válido apenas se a composição ou a imagem carregar a explicação. Não acrescente apoio artificial para preencher um template.
6. Escreva em `carousel.md` somente a copy exata que aparecerá na arte. Não use limites fixos de caracteres, mas corte qualquer palavra que não aumente compreensão, tensão ou consequência.
7. Depois de fechar a copy, leia todos os slides em sequência e compare-os novamente com o mapa da fonte. Reprove e reescreva se houver tópico obrigatório ausente, mudança de assunto, transição inventada, conclusão não sustentada, linguagem meta ou excesso que impeça leitura rápida.
8. Escreva a legenda para ampliar o conteúdo, não para explicar o que os slides deveriam ter dito. Use CTA somente se ele aprofundar naturalmente o assunto.

Atualize `target.slide_count` para 6 ou 7. Quando a copy passar pela leitura social e pela comparação final com a fonte, registre internamente `ready_for_design`; não peça aprovação intermediária se o pedido foi pelo carrossel completo.

## 3. Atribuir os templates aos slides

Antes desta etapa, leia [o sistema visual determinístico](references/visual-system.md) e [a seleção de templates](references/template-selection.md). Os JSONs em `assets/templates/` definem o layout; não há reconstrução visual por modelo de imagem, HTML/CSS ou composição manual.

O registry é um repertório de composições, não uma gramática fixa para todos os slides. A forma visual deve seguir o papel narrativo e a copy de cada slide. Um conjunto pode combinar capa com imagem, título e apoio, imagem com apoio, texto corrido sem título e título com imagem. Não force a mesma combinação de elementos em todos os slides, não acrescente títulos apenas para preencher hierarquia e não escreva texto de apoio artificial para ocupar um slot.

1. Crie `visual.md` a partir do modelo do projeto.
2. Faça uma auditoria visual dos assets disponíveis na fonte antes de escolher qualquer imagem. Para uma URL, inspecione todas as imagens oficiais relevantes da página — não apenas a primeira, a mais fácil de baixar ou a que tiver melhor proporção — e registre no `visual.md` o que cada candidata representa e por que foi selecionada ou descartada.
3. Para cada slide, use `assets/templates/template-registry.json` e o `contentModel` para escolher um `templateId` compatível com o papel narrativo, a composição necessária, os campos disponíveis, os limites de linhas, o texto e a mídia. Registre a escolha, a copy e a origem do asset.
4. Escolha imagens pela relação semântica com o ponto do slide: a imagem precisa mostrar o produto, a pessoa, a interface, o evento ou a consequência que a copy está explicando. Não use wallpaper, avatar ou imagem abstrata apenas porque é bonita, oficial ou combina com as cores. Se nenhuma imagem provar ou contextualizar o ponto, use um template tipográfico; não preencha o slot por obrigação.
5. Se nenhum template registrado representar a composição que a copy exige, não contorça o texto para caber nem preencha slots sem função. Interrompa para revisão do sistema visual ou crie um template declarativo específico antes de renderizar.
6. Monte `deliverables/render-input.json` com o contrato `carousel`, `width`, `height`, `slides`, `templateId` e `content`. O conteúdo contém texto e caminhos de mídia; nunca posições, cores, tamanhos ou regras visuais.
7. Se a copy não couber nos limites declarados, tente outro template. Se nenhum servir, interrompa para revisão editorial; não reduza indefinidamente a fonte, mova a mídia, corte ou reescreva o texto.
8. Defina se o slide exige fotografia, ilustração, gráfico, interface ou nenhuma mídia. Toda mídia deve provar, explicar ou contextualizar o conteúdo.
9. Atualize o item para `in_production` antes de produzir os arquivos finais.

## 4. Produzir a mídia e os slides

- Use mídia oficial ou da própria fonte quando ela for adequada, sua proveniência estiver registrada e o uso estiver autorizado ou claramente permitido.
- Em artigos com muitas imagens, prefira a imagem que mostra diretamente o assunto do slide. A beleza, a resolução, o recorte ou a proximidade visual com o template não são critérios suficientes.
- Quando for necessário criar uma imagem original e houver uma ferramenta de geração disponível — `image_generate` no Hermes — gere somente o asset visual, sem a copy do slide, sem letras legíveis e sem caixas reservadas para texto. O asset ocupa somente um slot de imagem do template.
- Salve os assets usados em `deliverables/assets/` com nomes descritivos e registre origem, geração e finalidade em `visual.md`.
- Se uma imagem for indispensável e nenhuma fonte ou ferramenta adequada estiver disponível, use `blocked`. Não substitua por ilustração genérica ou placeholder.

## 5. Renderizar os slides

1. Use `scripts/render_carousel.py --content <render-input.json> --output-dir <deliverables/>`. O Pillow lê o template e o `assets/design-system.json`; o modelo de imagem nunca escreve texto nem reconstrói o layout.
2. Não instale dependências silenciosamente. Se a fonte configurada, o template, a mídia ou o renderer estiverem indisponíveis, bloqueie a entrega e informe a ausência.
3. Nunca use SVG, wireframe, cartões vazios ou placeholders como entrega.
4. Gere `slide-01.png`, `slide-02.png` e assim por diante em `deliverables/`, todos com exatamente 1080 × 1350 pixels, retrato 4:5 para o feed.
5. Gere `deliverables/caption.md` e `deliverables/design-notes.md`. Registre neste último os `templateId`s, renderer, token de fonte, mídias e eventuais limitações.

## 6. Validar e entregar

Leia e aplique [a lista de qualidade](references/quality-checklist.md).

- Compare visualmente cada PNG com `carousel.md`; nenhum texto pode faltar, mudar ou ser inventado.
- Faça uma leitura editorial dos slides sem abrir `caption.md`: confirme que o assunto, a promessa da fonte, sua estrutura central, o recorte, a progressão e o takeaway estão compreensíveis para alguém que não viu a fonte.
- Compare a sequência final com o mapa do núcleo em `brief.md`. Não aprove um carrossel que seja factual e bem escrito, mas que tenha mudado de assunto, apagado a promessa editorial ou convertido a fonte em uma tese genérica.
- Execute `scripts/validate_carousel.py --content <render-input.json> --output-dir <deliverables/>` e corrija qualquer falha estrutural.
- Confirme dimensões, ordem, quantidade, legibilidade, relação semântica das imagens e ausência de elementos temporários.
- Corrija os problemas encontrados antes de encerrar.
- Atualize `metadata.yaml` para `status: in_review`, `owner: eduardo`, `updated_at` e uma nota curta com a próxima ação.
- Faça um commit focado e envie ao remoto quando houver autorização.

Nunca altere `approved` ou `published`. Esses estados e a publicação pertencem ao Eduardo.
