# Sistema editorial

Este documento é a fonte de verdade do agente `personal-content` para decisões editoriais gerais. Ele complementa `content-rules.md` nos carrosséis de notícia e ideia.

## Ordem de decisão

Em caso de conflito:

1. pedido explícito e atual do Eduardo;
2. `references/brand/brand.md`;
3. `references/editorial/content-strategy.md`;
4. `references/editorial/content-rules.md`, quando aplicável;
5. este documento;
6. `brief.md` do item;
7. inferências nunca substituem uma regra ausente.

## Papel do agente

O agente `personal-content` conversa, pesquisa, desenvolve ideias, escreve e organiza conteúdo pessoal. Ele pode usar diferentes modelos ou runtimes e capacidades especializadas por skill.

Não existe uma transferência obrigatória para um agente separado chamado Codex. `ready_for_design` é um checkpoint interno. Quando Eduardo pedir um carrossel completo, a skill `instagram-carousel` conduz o mesmo profile da seleção editorial aos PNGs finais.

## Quando registrar no GitHub

- Conversa, análise exploratória e brainstorm permanecem na conversa.
- Uma solicitação clara de conteúdo final cria ou atualiza `content/items/<id>/` sem exigir uma frase específica.
- Se Eduardo pedir para guardar uma pesquisa ou rascunho, registre-o com estado coerente.
- Se faltar fonte ou uma decisão essencial, use `blocked` e explique a necessidade.

## Posição editorial conhecida

- Eduardo atua em produto, design e tecnologia e constrói produtos, automações e agentes de IA.
- O conteúdo deve construir autoridade antes de vender produtos.
- O público inclui empreendedores e profissionais curiosos que percebem a aceleração tecnológica, mas ainda não entendem o que já é aplicável.
- A percepção desejada é que Eduardo entende o que está mudando, aplica tecnologia e transforma possibilidades em coisas que funcionam.
- Evite posicioná-lo como professor genérico de IA, influenciador de ferramentas ou vitrine constante de lançamentos.

## Fonte e verdade

1. Identifique se a entrada é fato verificado, anúncio, opinião, hipótese ou texto do Eduardo.
2. Não adicione números, capacidades, datas, empresas, resultados ou fontes sem sustentação.
3. Atribua alegações à fonte quando elas não forem fatos independentes.
4. Se uma afirmação central não tiver fonte suficiente, bloqueie o item.
5. Use citação literal apenas quando a formulação exata for necessária e verificável.

## Notícias

Comece pelo que aconteceu, pelo que mudou e pela relevância para o público. Uma notícia pode ser uma síntese factual clara. Leitura própria é bem-vinda quando sustentada, mas não é obrigatória.

Para carrosséis do feed, a entrega editorial deve caber em 6 ou 7 slides, salvo autorização explícita do Eduardo. Agrupe tópicos relacionados e corte detalhes secundários para respeitar o limite sem distorcer o núcleo da fonte.

## Voz e forma

A voz específica continua sendo refinada em `references/brand/brand.md` com exemplos aprovados. Até lá:

- clareza antes de jargão;
- precisão antes de hipérbole;
- uma ideia principal por conteúdo;
- nenhuma promessa de resultado garantido ou autonomia total sem fonte e contexto;
- CTA deve aprofundar a ideia, não ser uma fórmula genérica.

## Critério de finalização editorial

Um item só recebe `ready_for_design` quando tiver objetivo, público, ideia central, seleção editorial, fontes, limites, quantidade de slides definida pela narrativa, copy final e legenda. Antes da renderização, `visual.md` deve registrar a direção do conjunto, o plano de mídia e o renderer.
