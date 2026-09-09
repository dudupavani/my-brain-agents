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
2. Antes de redigir, decomponha a ideia central em passos narrativos: hook, contexto indispensável, desenvolvimento, consequência e fechamento, usando apenas o que a fonte sustenta. O carrossel pode omitir o que for secundário, mas nunca inventar fatos, transições causais ou uma conclusão ausente do material.
3. Escreva em `carousel.md` somente a copy exata que aparecerá na arte. Cada slide deve comunicar um passo necessário da mesma história e um único ponto principal; não usar o slide como depósito de parágrafos resumidos.
4. Não use limite fixo de caracteres. O critério é a composição: o texto precisa caber com tipografia expressiva e leitura confortável em tela pequena. Se não couber sem enfraquecer a hierarquia, simplifique a copy ou distribua a narrativa em outro slide; nunca reduza a tipografia até caber.
5. O slide 1 contém uma única frase de hook: provocativa o bastante para interromper a rolagem, mas precisa e sustentada pela fonte. Ela é o primeiro texto e o elemento tipográfico dominante.
6. Use CTA somente quando ele aprofundar naturalmente o conteúdo. Um fechamento factual ou uma conclusão também são válidos.
7. Escreva a legenda final e faça uma revisão editorial comparando a copy com a fonte e com a marca.

Atualize `target.slide_count` para o total real. Quando a copy estiver fechada, registre internamente `ready_for_design`; não peça aprovação intermediária se o pedido foi pelo carrossel completo.

## 3. Atribuir os templates aos slides

Antes desta etapa, leia [o sistema visual determinístico](references/visual-system.md) e [a seleção de templates](references/template-selection.md). Os JSONs em `assets/templates/` definem o layout; não há reconstrução visual por modelo de imagem, HTML/CSS ou composição manual.

1. Crie `visual.md` a partir do modelo do projeto.
2. Para cada slide, meça a copy e escolha um `templateId` compatível com o uso, campos obrigatórios, limites de linhas, texto e mídia do JSON. Registre a escolha, a copy e a origem do asset.
3. Monte `deliverables/render-input.json` com o contrato `carousel`, `width`, `height`, `slides`, `templateId` e `content`. O conteúdo contém texto e caminhos de mídia; nunca posições, cores, tamanhos ou regras visuais.
4. Se a copy não couber nos limites declarados, tente outro template. Se nenhum servir, interrompa para revisão editorial; não reduza indefinidamente a fonte, mova a mídia, corte ou reescreva o texto.
5. Defina se o slide exige fotografia, ilustração, gráfico, interface ou nenhuma mídia. Toda mídia deve provar, explicar ou contextualizar o conteúdo.
6. Atualize o item para `in_production` antes de produzir os arquivos finais.

## 4. Produzir a mídia e os slides

- Use mídia oficial ou da própria fonte quando ela for adequada, sua proveniência estiver registrada e o uso estiver autorizado ou claramente permitido.
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
- Execute `scripts/validate_carousel.py --content <render-input.json> --output-dir <deliverables/>` e corrija qualquer falha estrutural.
- Confirme dimensões, ordem, quantidade, legibilidade, relação semântica das imagens e ausência de elementos temporários.
- Corrija os problemas encontrados antes de encerrar.
- Atualize `metadata.yaml` para `status: in_review`, `owner: eduardo`, `updated_at` e uma nota curta com a próxima ação.
- Faça um commit focado e envie ao remoto quando houver autorização.

Nunca altere `approved` ou `published`. Esses estados e a publicação pertencem ao Eduardo.
