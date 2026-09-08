---
name: news-to-carousel
description: "Transforme uma URL, descoberta, vídeo/post ou ideia em um pacote factual pronto para um carrossel de Instagram. Use para pesquisar, selecionar e estruturar notícias e ideias; não use para criar as artes finais."
---

# News To Carousel

Use esta skill para transformar uma pauta em um pacote editorial completo. Ela conclui a etapa editorial; não desenha slides finais.

## Contexto obrigatório

Antes de decidir a pauta ou escrever, leia:

1. `AGENTS.md`
2. `agents/personal-content/README.md`
3. `content/AGENTS.md`
4. `references/brand/brand.md`
5. `references/editorial/content-rules.md`
6. `content/templates/metadata.yaml`, `brief.md` e `carousel.md`

Se estiver retomando um item existente, leia também todos os arquivos daquele pacote antes de alterá-lo.

Campos ainda vazios em `brand.md` não autorizam suposições. Use as regras editoriais e o material de entrada; bloqueie apenas quando faltar algo que impeça uma entrega fiel.

## Entrada e autonomia

A entrada pode ser uma URL de notícia, uma descoberta de pesquisa ou scraping, um vídeo/post, uma ideia do usuário ou algo discutido em conversa.

- Não peça ao usuário para preencher um briefing, escolher número de slides ou buscar imagens.
- Extraia e registre essas decisões no pacote.
- Quando o usuário pedir um conteúdo final, avance de forma autônoma até `ready_for_design`. Uma URL enviada apenas para análise ou conversa não vira pacote no GitHub por conta própria.
- Use `blocked` somente quando a fonte estiver inacessível, for contraditória, não tiver informação suficiente para sustentar a copy ou exigir uma decisão que altere materialmente o conteúdo.

## Selecionar e apurar

1. Identifique o fato, a fonte primária quando houver, a data e o que mudou de forma concreta.
2. Aplique o filtro de percepção definido em `content-rules.md`: priorize o que revela possibilidades reais da tecnologia e sua consequência prática para produtos, trabalho ou negócios.
3. Uma notícia não precisa virar opinião. Quando a fonte só sustenta um resumo, apresente a notícia com clareza e sem forçar uma tese adicional.
4. Registre URLs, publicador, data e fatos verificáveis em `metadata.yaml` e `brief.md`.
5. Nunca complete lacunas com números, resultados, citações, contexto técnico ou promessas inventadas. Diferencie fato, declaração atribuída e interpretação.

## Criar o pacote

1. Crie `content/items/<id>/` a partir dos modelos. Use um ID estável com data e assunto.
2. Preencha `metadata.yaml` com a origem e mantenha `status`, `owner` e `updated_at` sincronizados.
3. Em `brief.md`, deixe explícitos o fato central, o recorte, o público, os limites e as fontes que sustentam a copy.
4. Em `carousel.md`, escreva a copy final slide a slide. Defina a quantidade de slides pela narrativa; nunca por um número padrão. O total em `target.slide_count` deve coincidir exatamente com o arquivo.
5. O primeiro slide tem uma única frase de hook. Ela deve ser precisa, interessar sem exagerar e não prometer além do que a fonte sustenta.
6. Crie `media.md` somente quando houver mídia útil para a narrativa. Registre por item: qual é o ativo, sua URL ou caminho, a origem, o papel editorial e os slides em que ele faz sentido. Não use mídia decorativa nem transfira essa decisão ao usuário.

## Concluir a etapa editorial

1. Revise fatos, nomes, números, sequência e links.
2. Atualize para `status: ready_for_design`, `owner: personal-content`, `updated_at` e `handoff.ready_for_design_at`.
3. Em `handoff.notes`, registre somente orientações necessárias para a etapa visual, inclusive limitações da mídia ou da fonte.
4. Faça um commit focado e envie ao remoto quando houver acesso autorizado.

Não crie arquivos em `deliverables/` nem produza as artes finais nesta skill. O mesmo profile pode carregar a skill visual em seguida quando Eduardo pedir explicitamente essa produção.
