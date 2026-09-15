---
name: extract-reference
description: Extrai um único design.json de uma imagem de referência usando inspeção visual e Pillow.
---

# Extract Reference

Leia `../../AGENTS.md`. Inspecione a imagem visualmente, identifique áreas textuais sem transcrever seu conteúdo e execute `extractor.py`. O script mede pixels; a inspeção do agente define a função visual dos elementos. Valide o único `design.json` com `validator.py`. A referência nunca é modificada nem reutilizada como imagem de saída.
