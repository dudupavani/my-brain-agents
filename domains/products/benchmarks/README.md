# Benchmarks de produtos

Cada benchmark concluído vive em `domains/products/benchmarks/<id>/`, com ID estável e legível.

Estrutura mínima recomendada:

```text
<id>/
├── metadata.yaml   identidade, datas, responsável, fontes e link do ClickUp
├── report.md       benchmark completo e conclusões
└── sources.md      URLs, evidências e limitações da pesquisa
```

Adicione imagens ou dados estruturados apenas quando forem necessários para entender ou reutilizar a análise.

O relatório deve distinguir:

- evidência observada na fonte;
- interpretação do agente;
- implicação possível para um produto do Eduardo;
- decisão efetivamente tomada pelo Eduardo, quando existir.

Se a skill de benchmark do profile do Hermes for promovida para o projeto, ela deve produzir ou adaptar sua saída a este contrato sem perder informação útil.
