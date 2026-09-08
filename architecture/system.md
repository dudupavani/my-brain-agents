# Arquitetura v1 do cérebro compartilhado

## Objetivo

Este sistema permite que os agentes do Eduardo trabalhem como funcionários especializados sem prender conhecimento ao Hermes, ClickUp, Codex, Claude ou a conversas isoladas.

A v1 atende dois agentes reais: um de produtos e softwares e outro de conteúdo pessoal.

## Camadas

### Profile do Hermes

É o funcionário. Mantém identidade, personalidade, memória privada, sessões, credenciais, automações e skills particulares. O modelo usado pelo profile não muda a identidade do agente.

Os profiles já existem e funcionam fora deste repositório. A arquitetura v1 apenas define o conhecimento que eles leem e escrevem no GitHub; instalação, configuração e operação do Hermes não fazem parte deste sistema.

### GitHub

É o patrimônio compartilhável. Mantém pesquisas, benchmarks, decisões, materiais, regras, entregas, skills portáteis e histórico. Não substitui a memória automática do Hermes.

### ClickUp

É o sistema de acompanhamento. Mantém tarefas, prazos, responsáveis e aprovações. Quando uma entrega aparecer nos dois sistemas, o conteúdo canônico fica no GitHub e o ClickUp aponta para ele.

### Repositórios de software

O código-fonte permanece no repositório do software. Este cérebro guarda contexto, pesquisa, decisões, especificações e links para o código.

## Cérebros lógicos

Um cérebro lógico é uma combinação de caminhos e permissões. Ele não precisa ser um repositório separado.

### Product Brain

- Responsável: `products`.
- Contrato: `agents/products/README.md`.
- Conhecimento canônico: `domains/products/`.
- Entradas destinadas ao agente: `inbox/products/`.
- Contexto comum: `shared/` e skills relevantes.

### Personal Content Brain

- Responsável: `personal-content`.
- Contrato: `agents/personal-content/README.md`.
- Produção canônica: `content/`.
- Marca e regras: `references/`.
- Entradas destinadas ao agente: `inbox/personal-content/`.
- Contexto comum: `shared/` e skills relevantes.

## Comunicação entre agentes

Não existe masterbrain na v1. Eduardo conversa diretamente com cada agente.

Quando um trabalho gerar uma entrada útil para o outro agente, a origem cria uma nota pequena no inbox do destinatário e aponta para o artefato canônico. O inbox não recebe cópias completas.

## Quando criar outro repositório

Separe um cérebro lógico quando existir pelo menos uma fronteira real:

1. pessoas, equipes ou sócios com acessos diferentes;
2. informação empresarial ou pessoal confidencial;
3. credenciais ou automações que exigem isolamento;
4. ciclo de vida e governança próprios;
5. volume de trabalho que prejudica o restante do cérebro.

A existência de outro agente, por si só, não é motivo suficiente.

## Portabilidade

O contrato portátil é formado por `AGENTS.md`, documentos Markdown, dados estruturados e `.agents/skills/`. Instruções específicas de um runtime só devem existir quando houver uma diferença real de comportamento.

## Evolução

Toda mudança estrutural deve atualizar `architecture/decisions.md`, `architecture/registry.yaml` e `mapa.md` quando afetar o roteamento. Experimentos permanecem identificados como experimentos até produzirem evidência suficiente para virar regra.
