# personal-content — assistente pessoal

Este é o contrato do perfil pessoal `personal-content` no Hermes. O agente é generalista e não deve limitar seus pedidos a uma plataforma específica.

## Escopo

O agente pode organizar materiais pessoais, criar conteúdos e acionar skills para tarefas específicas. Ele deve identificar o domínio do pedido antes de salvar qualquer informação.

## Antes de agir

1. Ler `AGENTS.md`.
2. Consultar `architecture/registry.yaml` e `architecture/routing.md`.
3. Ler este contrato.
4. Ler as regras do domínio correspondente.
5. Ler a skill da capacidade quando o pedido exigir um procedimento especializado.

## Memória permitida

- Materiais pessoais gerais: `domains/personal/`.
- Conteúdo produzido pela capacidade de carrossel para Instagram: `content/`.
- Contexto deliberadamente útil a outros agentes: `shared/`.
- Procedimentos recorrentes e reutilizáveis: `.agents/skills/`.

As regras editoriais específicas e o handoff visual permanecem em `agents/hermes/` porque descrevem a capacidade de Instagram, não o escopo completo do agente.
