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

## 1. Apurar e selecionar

1. Crie ou retome `content/items/<id>/` e use `status: draft` durante a apuração.
2. Se a entrada for URL, extraia a fonte, procure a origem primária quando necessário e confira fatos, nomes, números e datas.
3. Identifique uma única ideia central coerente com os objetivos editoriais do Eduardo.
4. Selecione apenas os fatos e pontos necessários para essa ideia. Não tente comprimir o artigo inteiro nem preserve trechos só porque estavam na fonte.
5. Registre em `brief.md` o que foi selecionado, o que foi descartado por irrelevância ou falta de sustentação e as fontes usadas.

Não transforme notícia em opinião obrigatoriamente. Diferencie fato verificado, declaração atribuída, interpretação e hipótese.

## 2. Escrever a narrativa do carrossel

1. Defina a quantidade de slides pela narrativa e pela legibilidade. Não existe número fixo, mínimo editorial ou padrão de oito slides.
2. Escreva em `carousel.md` somente a copy exata que aparecerá na arte.
3. O slide 1 contém uma única frase de hook: provocativa o bastante para interromper a rolagem, mas precisa e sustentada pela fonte. Ela é o primeiro texto e o elemento tipográfico dominante.
4. Cada slide seguinte cumpre uma função clara e desenvolve apenas um ponto principal. Remova repetição, contexto lateral e explicação que exija reduzir excessivamente a tipografia.
5. Use CTA somente quando ele aprofundar naturalmente o conteúdo. Um fechamento factual ou uma conclusão também são válidos.
6. Escreva a legenda final e faça uma revisão editorial comparando a copy com a fonte e com a marca.

Atualize `target.slide_count` para o total real. Quando a copy estiver fechada, registre internamente `ready_for_design`; não peça aprovação intermediária se o pedido foi pelo carrossel completo.

## 3. Planejar o visual

Antes desta etapa, leia [o sistema visual e contrato de renderização](references/visual-system.md) e abra as três referências JPEG em `assets/templates/`.

O conjunto obrigatório é `reference-01.jpg`, `reference-02.jpg` e `reference-03.jpg`. Se qualquer arquivo estiver ausente, ilegível ou não for JPEG, use `blocked`; não improvise outra referência.

1. Crie `visual.md` a partir do modelo do projeto.
2. Escolha para cada slide a família de layout que melhor serve à mensagem, sem repetir mecanicamente o mesmo molde.
3. Defina se o slide exige fotografia, ilustração, gráfico, interface ou nenhuma mídia. Toda imagem deve provar, explicar ou contextualizar o conteúdo.
4. Prefira mídia primária ou fotografia real quando forem relevantes. Não use imagens genéricas para preencher espaço.
5. Atualize o item para `in_production` antes de produzir os arquivos finais.

## 4. Produzir os assets de imagem

- Use mídia oficial ou da própria fonte quando ela for adequada, sua proveniência estiver registrada e o uso estiver autorizado ou claramente permitido.
- Quando for necessário criar uma imagem original e houver uma ferramenta de geração disponível — `image_generate` no Hermes — gere somente o asset visual, sem a copy do slide, sem letras legíveis e sem caixas reservadas para texto.
- Não peça ao gerador de imagem para montar o slide final. Ele não decide conteúdo, narrativa, tipografia nem layout.
- Salve os assets usados em `deliverables/assets/` com nomes descritivos e registre origem, geração e finalidade em `visual.md`.
- Se uma imagem for indispensável e nenhuma fonte ou ferramenta adequada estiver disponível, use `blocked`. Não substitua por ilustração genérica ou placeholder.

## 5. Renderizar os slides

1. Componha os slides com um renderer determinístico que preserve a copy exatamente, como HTML/CSS capturado em PNG ou outro compositor raster já disponível no ambiente.
2. O renderer combina texto aprovado, asset, tipografia, cor, espaçamento e layout. O modelo de imagem nunca escreve o texto final.
3. Não instale dependências silenciosamente. Se não houver um renderer capaz de produzir o resultado com precisão, bloqueie a entrega e informe a capacidade ausente.
4. Nunca use SVG, wireframe, cartões vazios ou placeholders como entrega.
5. Gere `slide-01.png`, `slide-02.png` e assim por diante em `deliverables/`, todos com exatamente 1080 × 1350 pixels, retrato 4:5 para o feed.
6. Gere `deliverables/caption.md` e `deliverables/design-notes.md`. Registre neste último as referências consultadas, o renderer, a tipografia, as mídias e eventuais limitações.

## 6. Validar e entregar

Leia e aplique [a lista de qualidade](references/quality-checklist.md).

- Compare visualmente cada PNG com `carousel.md`; nenhum texto pode faltar, mudar ou ser inventado.
- Confirme dimensões, ordem, quantidade, legibilidade, relação semântica das imagens e ausência de elementos temporários.
- Corrija os problemas encontrados antes de encerrar.
- Atualize `metadata.yaml` para `status: in_review`, `owner: eduardo`, `updated_at` e uma nota curta com a próxima ação.
- Faça um commit focado e envie ao remoto quando houver autorização.

Nunca altere `approved` ou `published`. Esses estados e a publicação pertencem ao Eduardo.
