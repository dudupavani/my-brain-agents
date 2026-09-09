# Notas de design

- **Templates aplicados diretamente:** `reference-01.jpg` nos slides 1; `reference-02.jpg` nos slides 2 e 4; `reference-03.jpg` nos slides 3 e 5.
- **Renderer:** `render.py` com Pillow. Cada PNG começou pelo JPEG de template correspondente; somente os placeholders de copy e mídia foram substituídos.
- **Tipografia e composição:** preservadas das referências; o renderer não criou uma composição nova.
- **Mídias:** `openai-sketch.png` e `openai-editing.png`, capturas oficiais do anúncio da OpenAI, usadas nos campos de mídia de seus respectivos templates.
- **QA:** cinco PNGs 1080×1350, sem texto de placeholder visível, revisados contra a composição dos templates.
