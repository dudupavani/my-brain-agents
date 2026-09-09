# Especificação visual

## Direção do conjunto

- Templates consultados e usados diretamente: `reference-01.jpg`, `reference-02.jpg`, `reference-03.jpg`.
- Renderer: Pillow/Python, abrindo o JPEG do template como base de cada slide e substituindo exclusivamente seus placeholders.
- Tipografia, cores, espaçamento e elementos fixos: preservados dos JPEGs escolhidos.
- Mídias oficiais: imagens de demonstração do anúncio da OpenAI, baixadas do próprio artigo e usadas para substituir as áreas de imagem dos templates.

## Plano por slide

### Slide 1
- Template: `reference-01.jpg`.
- Placeholder de imagem: substituído por `deliverables/assets/openai-sketch.png`.
- Placeholder de hook: substituído pela copy do slide 1.
- Elementos fixos preservados: fundo, gradação, seta e composição capa.

### Slide 2
- Template: `reference-02.jpg`.
- Placeholder de texto superior: substituído pela primeira frase do slide 2.
- Placeholder de texto inferior: substituído pela segunda frase do slide 2.
- Elementos fixos preservados: painel azul, gradação inferior e seta.

### Slide 3
- Template: `reference-03.jpg`.
- Placeholder de texto superior: substituído pela copy do slide 3.
- Placeholder de imagem: substituído por `deliverables/assets/openai-sketch.png`.
- Elementos fixos preservados: fundo, proporção texto/imagem e cantos arredondados.

### Slide 4
- Template: `reference-02.jpg`.
- Placeholders de texto: substituídos pelas três capacidades do slide 4.
- Elementos fixos preservados: painel azul, gradação inferior e seta.

### Slide 5
- Template: `reference-03.jpg`.
- Placeholder de texto superior: substituído pela copy do slide 5.
- Placeholder de imagem: substituído por `deliverables/assets/openai-editing.png`.
- Elementos fixos preservados: fundo, proporção texto/imagem e cantos arredondados.

## Assets

- `openai-sketch.png`: imagem oficial de demonstração do recurso Sketch no anúncio da OpenAI; slides 1 e 3.
- `openai-editing.png`: imagem oficial de demonstração de edição no anúncio da OpenAI; slide 5.
- `openai-templates.png`: imagem oficial de demonstração de templates, mantida como referência de origem e não usada no corte final.

## Limitações

Os JPEGs do repositório são usados como templates de composição; as imagens da OpenAI são mídia editorial oficial do anúncio. Nenhum placeholder do template deve permanecer no resultado.
