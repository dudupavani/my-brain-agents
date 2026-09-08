# Instruções do domínio de conteúdo pessoal

Este diretório é a fonte canônica dos conteúdos pessoais produzidos para Eduardo.

## Responsável

O agente lógico `personal-content` conduz o fluxo. Codex, Claude ou outro modelo podem executar as capacidades sem se tornarem responsáveis separados.

## Leitura obrigatória

Antes de criar ou alterar um item, leia:

1. `agents/personal-content/README.md`;
2. `references/brand/brand.md`;
3. `references/editorial/content-system.md`;
4. `references/editorial/content-rules.md` quando o item for notícia, novidade de IA ou ideia relacionada a produto;
5. a skill correspondente em `.agents/skills/`.

Para pedidos de carrossel, use `.agents/skills/instagram-carousel/SKILL.md` como workflow único da entrada aos PNGs finais.

## Pacotes

Cada conteúdo vive em `content/items/<id>/`. Não mova a pasta para indicar avanço.

- `draft`: pesquisa ou copy em elaboração;
- `ready_for_design`: copy final e pronta para a capacidade visual;
- `in_production`: produção visual em andamento;
- `in_review`: entrega final aguardando Eduardo;
- `approved`: aprovado por Eduardo;
- `published`: publicado;
- `blocked`: falta fonte, decisão ou acesso.

Nos novos itens, use `owner: personal-content` até `in_review`. A partir de `in_review`, use `owner: eduardo`. Pacotes experimentais antigos podem manter proprietários legados até serem retomados.

A quantidade de slides depende do conteúdo. O formato final do carrossel é 1080 × 1350 pixels, em retrato 4:5, para o feed.

## Persistência

- Uma solicitação clara de conteúdo final cria ou atualiza um pacote sem exigir a frase “prepare para o Codex”.
- Análise, conversa e brainstorm permanecem na conversa, salvo pedido explícito para registrar.
- “Crie ou faça um carrossel” autoriza o fluxo completo até `in_review`, incluindo assets, renderização e QA, sem aprovação intermediária.
- Se Eduardo pedir somente estrutura, roteiro ou copy, encerre em `ready_for_design` e não produza imagens.
- Não altere `approved` ou `published` sem ação do Eduardo.
