# Lista de qualidade do carrossel

Use esta lista depois de renderizar e antes de marcar o item como `in_review`.

## Fonte e edição

- A ideia central está coerente com o material fornecido e com os objetivos editoriais do Eduardo.
- `brief.md` distingue fatos, declarações atribuídas, interpretações e pontos descartados.
- Nomes, números, datas, capacidades, promessas e citações possuem sustentação verificável.
- O carrossel seleciona o essencial; não tenta reproduzir o artigo inteiro nem acrescenta contexto inventado.
- A quantidade de slides foi decidida para este conteúdo e coincide com `target.slide_count`.
- A narrativa seleciona e reorganiza apenas o que a fonte sustenta: não há fato, relação causal ou conclusão inventados para ligar os slides.
- O hook é uma única frase, interessante, precisa e fiel à fonte.
- O hook identifica o assunto central em isolamento — produto, empresa, pessoa, evento ou categoria inequívoca — sem depender da legenda ou dos slides seguintes para explicar do que o post trata.
- Cada slide desenvolve um ponto principal; o CTA só existe quando acrescenta valor.

## Direção visual e mídia

- Cada slide registra em `visual.md` o `templateId` JSON escolhido, a copy e a mídia usada.
- O slide final mantém a composição, a hierarquia, a tipografia, as cores, o espaçamento e as proporções do template escolhido.
- A capa trata o hook como primeiro texto e elemento tipográfico dominante.
- Cada imagem prova, explica ou contextualiza o slide em que aparece.
- Fotografia real ou mídia primária foi priorizada quando relevante.
- A origem e a condição de uso de cada mídia externa estão registradas.
- Assets gerados não contêm a copy, letras falsas, títulos ou layout de post.
- Não há mídia genérica, repetida, puramente decorativa ou sem relação com o assunto.
- Nenhum placeholder de medição, caixa vazia ou texto de referência vazou para a entrega; a composição foi produzida pelos dados do template.

## Renderização

- O texto dos PNGs corresponde exatamente a `carousel.md`, inclusive acentos, números e pontuação.
- O texto foi aplicado por renderer determinístico, não desenhado pelo gerador de imagem.
- O arquivo de conteúdo não contém posições, tamanhos, cores, gradientes ou regras de layout.
- O PNG passou pelo `validate_carousel.py`, incluindo dimensões, limites de linhas, fonte, moldura, recorte e raio declarados no template.
- Todos os slides são PNG raster de exatamente 1080 × 1350 pixels, retrato 4:5 para o feed.
- Não há SVG, wireframe, placeholder, arquivo temporário, corte, sobreposição ou texto fora da área segura.
- Hierarquia, contraste, alinhamento, margens, entrelinha e tamanho permanecem fiéis ao template e funcionam em tela pequena.
- A copy foi revisada no PNG final: cada slide está conciso o bastante para leitura confortável e nenhum texto foi comprimido ou reduzido excessivamente para caber.
- O conjunto tem unidade visual sem transformar todos os slides em cópias do mesmo layout.

## Pacote final

- Há um PNG para cada slide, nomeado e ordenado corretamente.
- `caption.md` contém a legenda final.
- `design-notes.md` registra template, renderer, token de tipografia, assets e limitações.
- `metadata.yaml` está em `in_review`, com `owner: eduardo` e próxima ação clara.
