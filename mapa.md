# Mapa do cérebro compartilhado

Use este mapa para descobrir onde ler e onde registrar uma entrega. A identidade e a memória privada de cada agente permanecem no profile do Hermes; este mapa cobre somente o conhecimento versionado no GitHub.

## Cérebros lógicos ativos

### Produtos

- Contrato: `agents/products/README.md`
- Conhecimento canônico: `domains/products/`
- Benchmarks: `domains/products/benchmarks/`
- Entradas recebidas de outro agente: `inbox/products/`
- Skills: `.agents/skills/` conforme a tarefa

### Conteúdo pessoal

- Contrato: `agents/personal-content/README.md`
- Produção e histórico editorial: `content/`
- Marca e estratégia editorial: `references/brand/` e `references/editorial/`
- Entradas recebidas de outro agente: `inbox/personal-content/`
- Skill de carrossel ponta a ponta: `.agents/skills/instagram-carousel/`

### Interseção compartilhada

- Contexto deliberadamente útil aos dois agentes: `shared/`
- Passagens entre agentes: `inbox/`
- Procedimentos portáteis entre Hermes, Codex, Claude e outros: `.agents/skills/`

## Estrutura

```text
AGENTS.md                   contexto obrigatório do projeto
README.md                   apresentação humana
mapa.md                     navegação e roteamento rápido
architecture/               desenho, decisões e permissões
agents/                     contratos dos profiles, não suas memórias privadas
domains/products/           cérebro lógico de produtos
content/                    cérebro lógico de conteúdo pessoal
references/                 marca e regras editoriais
shared/                     conhecimento realmente compartilhado
inbox/                      passagens pequenas entre agentes
.agents/skills/             procedimentos reutilizáveis do projeto
```

## Destinos comuns

| Entrega | Destino canônico |
| --- | --- |
| Benchmark de concorrente | `domains/products/benchmarks/<id>/` |
| Pesquisa, decisão ou material de produto | `domains/products/` |
| Código-fonte de software | Repositório próprio do software; registre aqui apenas contexto e link |
| Ideia enviada de produtos para conteúdo | `inbox/personal-content/` com link para a origem |
| Ideia enviada de conteúdo para produtos | `inbox/products/` com link para a origem |
| Pacote de conteúdo pessoal | `content/items/<id>/` |
| Identidade e regras editoriais | `references/brand/` e `references/editorial/` |
| Procedimento recorrente e compartilhável | `.agents/skills/<nome>/` |
| Preferência ou memória privada do agente | Profile do Hermes, não este repositório |
| Tarefa, prazo e acompanhamento | ClickUp; linke a entrega canônica do GitHub |

Não crie um novo domínio, cérebro ou repositório apenas porque existe um novo agente. Crie quando existir uma responsabilidade durável ou uma fronteira real de acesso.
