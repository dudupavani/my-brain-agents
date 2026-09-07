# Entrega de conteúdo para o Codex

Use este protocolo ao produzir um conteúdo que deverá virar carrossel de Instagram.

1. Atualize o repositório antes de começar, se o remoto estiver configurado. Leia `references/brand/brand.md` e `references/editorial/content-system.md` antes de definir a copy.
2. Crie `content/items/<id>/`, usando os modelos em `content/templates/`.
3. Preencha `brief.md` com objetivo, público, limites e fontes. Preencha `carousel.md` com a copy final, slide a slide, incluindo CTA e legenda proposta. Não use uma quantidade fixa de slides: escolha o total que melhor serve à narrativa e registre-o em `metadata.yaml`.
4. Revise se a copy é factual, completa e realmente final. Não deixe instruções vagas como “desenvolver melhor”.
5. Atualize `metadata.yaml` para `status: ready_for_design`, `owner: codex`, `updated_at` e `handoff.ready_for_design_at`. Se houver orientação importante para o design, escreva-a em `handoff.notes`.
6. Faça um commit focado e envie ao GitHub quando seu acesso estiver configurado.

Não crie imagens finais nem altere arquivos em `deliverables/`. O Codex é responsável pela etapa visual.

Se a pesquisa ou a copy não estiver pronta, mantenha `status: draft`. Se faltar algo para concluir, use `status: blocked` e explique exatamente o que falta em `handoff.notes`.
