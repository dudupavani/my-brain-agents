# Agente de produtos

Este diretório é o contrato do perfil de produtos no Hermes.

## Escopo atual

O agente mantém materiais, decisões e trabalho relacionados a produtos em `domains/products/`.

Como ainda não há regras específicas registradas para esse perfil neste repositório, o agente não deve inventar um sistema editorial, estados ou formatos de entrega. Ao surgir uma necessidade recorrente, registre aqui a regra correspondente e atualize `architecture/registry.yaml` se o escopo mudar.

## Antes de agir

1. Ler `AGENTS.md`.
2. Consultar `architecture/registry.yaml` e `architecture/routing.md`.
3. Ler este contrato.
4. Ler `domains/products/README.md`.

## Memória permitida

- Criar e atualizar arquivos dentro de `domains/products/`.
- Usar `shared/` somente quando a informação for deliberadamente útil para outros agentes.
- Criar ou atualizar skills em `.agents/skills/` apenas quando o procedimento for recorrente e estiver claro.
