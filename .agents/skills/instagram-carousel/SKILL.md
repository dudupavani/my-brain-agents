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

## 1. Apurar e selecionar

1. Crie ou retome `content/items/<id>/` e use `status: draft` durante a apuração.
2. Se a entrada for URL, extraia a fonte, procure a origem primária quando necessário e confira fatos, nomes, números e datas.
3. Antes de definir o recorte, registre em `brief.md` qual é o assunto específico da fonte, sua promessa editorial, seu formato central e os elementos que não podem desaparecer sem mudar o assunto. O formato pode ser lista, framework, estudo de caso, comparação, lançamento, tutorial, argumento ou outro equivalente.
4. Marque o núcleo inegociável da fonte e mapeie como ele aparecerá nos slides. Se a fonte for uma lista de casos, preserve a visão geral da lista ou apresente casos nomeados; se for estudo de caso, preserve problema, solução e resultado; se for comparação, preserve os elementos comparados; se for lançamento, preserve o que foi lançado, o que mudou e por que importa; se for tutorial, preserve o processo que o torna útil. É permitido resumir, agrupar e omitir detalhes secundários, nunca remover o que define o conteúdo original.
5. Identifique uma única ideia central que sintetize fielmente esse objeto para o público do Eduardo. Ela deve continuar específica o bastante para que a fonte seja reconhecível, e não substituir seu assunto por uma tese aplicável a qualquer material semelhante.
6. Escolha um ângulo editorial explícito: como contar o conteúdo original, o que aconteceu ou qual ideia está em jogo, o que mudou e por que isso importa para este público. O ângulo organiza a história; não troca a história. Se houver mais de uma forma de apresentar a mesma fonte, escolha uma e registre as alternativas de apresentação, sem descartar elementos do núcleo.
7. Selecione os fatos e pontos necessários para comunicar a fonte com clareza. Não tente comprimir cada detalhe, mas não descarte a promessa, a estrutura ou os exemplos que definem seu assunto. Registre somente omissões secundárias ou sem sustentação.
8. Registre em `brief.md` a fonte, o núcleo preservado, a cobertura prevista e o que foi omitido legitimamente.
9. Separe no brief fatos verificáveis, declarações atribuídas à fonte e interpretações editoriais. Uma interpretação pode entrar, mas deve ser reconhecível como interpretação e não pode virar fato por causa da redação.

Não transforme notícia em opinião obrigatoriamente. Diferencie fato verificado, declaração atribuída, interpretação e hipótese.

## 2. Escrever a narrativa do carrossel

### Gate editorial: história antes do design

Antes de escolher templates, imagens ou quantidade final de slides, construa a linha editorial em `brief.md`:

- a promessa: o que o leitor vai entender ao terminar;
- a tensão: qual problema, mudança ou pergunta move o conteúdo;
- a progressão: como a história sai do hook e chega à conclusão;
- a consequência: por que o assunto importa para esse público;
- o takeaway: qual ideia deve permanecer depois do último slide.

Para cada slide, registre o papel narrativo, a pergunta que ele responde, a ponte para o próximo e qual elemento do núcleo da fonte ele preserva. Só avance para a copy final quando a sequência puder ser resumida em uma frase, cada slide for necessário para a compreensão e a soma dos slides mantiver a promessa e a estrutura da fonte. Se a sequência parecer uma coleção de afirmações independentes, volte para a linha editorial; não tente consertar o problema apenas com layout ou imagens. Se a mesma narrativa pudesse servir para outra fonte do mesmo tema, ela está genérica demais e deve ser reescrita.

A legenda pode aprofundar a história, mas não pode carregar o contexto essencial que torna os slides compreensíveis. Leia a sequência sem a legenda e verifique se alguém que não viu a fonte entende o assunto, a mudança e a conclusão.

1. Defina a quantidade de slides pela narrativa e pela legibilidade. Não existe número fixo, mínimo editorial ou padrão de oito slides.
2. Antes de redigir, decomponha a ideia central em passos narrativos: hook, contexto indispensável, desenvolvimento, consequência e fechamento, usando o mapa do núcleo da fonte. O carrossel pode omitir o que for secundário, mas nunca inventar fatos, transições causais ou uma conclusão ausente do material — nem substituir a estrutura original por uma tese independente.
3. Escreva em `carousel.md` somente a copy exata que aparecerá na arte. Cada slide deve comunicar um passo necessário da mesma história e um único ponto principal; não usar o slide como depósito de parágrafos resumidos nem como lista sem enquadramento.
4. Um slide só com título é permitido apenas quando a imagem ou a composição carregar a explicação. Caso contrário, use texto de apoio ou outro template; não deixe títulos soltos para preencher a sequência.
5. Não use limite fixo de caracteres. O critério é a composição: o texto precisa caber com tipografia expressiva e leitura confortável em tela pequena. Se não couber sem enfraquecer a hierarquia, simplifique a copy ou distribua a narrativa em outro slide; nunca reduza a tipografia até caber.
6. O slide 1 precisa apresentar o assunto e o hook. O hook deve ser provocativo o bastante para interromper a rolagem, mas preciso e sustentado pela fonte. O assunto central — produto, empresa, pessoa, evento ou categoria inequívoca — deve aparecer de forma explícita para um leitor que chegou pelo Instagram sem contexto. Quando o template tiver um campo de identificação, use uma etiqueta curta (por exemplo, “GROK BOT”) e mantenha o hook em uma única frase; quando não tiver, incorpore o assunto no próprio hook (por exemplo, “O Grok Bot está sendo desenhado como um colega de trabalho”). Um hook genérico que só faça sentido depois de ler a legenda ou passar para o slide 2 é inválido. Não invente uma segunda linha ou campo fora do contrato do template.
7. A copy do conjunto deve continuar referenciando o assunto central de modo natural. Não apresente o tema apenas na legenda e depois use “isso”, “essa ideia” ou “o produto” sem antecedente claro; retome o nome ou uma referência inequívoca quando isso evitar ambiguidade.
8. Use CTA somente quando ele aprofundar naturalmente o conteúdo. Um fechamento factual ou uma conclusão também são válidos.
9. Escreva a legenda final e faça uma revisão editorial comparando a copy com a fonte e com a marca. A legenda deve ampliar o carrossel, não corrigir uma narrativa incompleta.

Atualize `target.slide_count` para o total real. Quando a copy estiver fechada, registre internamente `ready_for_design`; não peça aprovação intermediária se o pedido foi pelo carrossel completo.

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
