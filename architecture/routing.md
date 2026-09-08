# Roteamento da memória

Este arquivo define como um agente decide onde registrar uma informação. O registro principal dos agentes e domínios está em `registry.yaml`.

## Sequência

1. Identificar a intenção do pedido: guardar, investigar, decidir, criar, atualizar ou entregar.
2. Identificar o domínio principal.
3. Ler o contrato do agente e as regras desse domínio.
4. Verificar se o pedido deve ser apenas respondido na conversa ou persistido no repositório.
5. Salvar no caminho canônico do domínio.
6. Atualizar o índice ou metadado correspondente quando existir.
7. Revisar os arquivos alterados e registrar uma entrega rastreável.

## Domínios atuais

| Pedido ou material | Caminho canônico | Responsável |
| --- | --- | --- |
| Conteúdo, pauta ou carrossel de Instagram | `content/` | Instagram Creator e Codex, conforme a etapa |
| Marca, voz e regras editoriais | `references/brand/` e `references/editorial/` | Você e agentes autorizados |
| Material pessoal geral | `domains/personal/` | Agente pessoal |
| Decisão, pesquisa ou artefato de produto | `domains/products/` | Agente de produtos |
| Contexto que precisa servir a vários agentes | `shared/` | Dono definido na própria entrega |
| Procedimento recorrente de um ou mais agentes | `.agents/skills/` | Você e agentes autorizados |

## Limites

- Não duplicar a mesma memória em dois domínios.
- Não salvar uma conversa inteira quando apenas uma decisão ou material for relevante.
- Não transformar uma instrução pontual em skill sem recorrência e clareza suficientes.
- Não colocar materiais dentro de `agents/`: essa pasta descreve agentes; a memória fica nos domínios.
- Quando dois domínios forem plausíveis, escolher o domínio do assunto, não o agente que recebeu o pedido.
- Quando a classificação mudar materialmente o resultado, pedir decisão antes de persistir.

## Skills

`.agents/skills/` é a fonte viva das skills do projeto. Uma atualização substitui a instrução anterior no mesmo caminho; não criar pastas de versão, cópias numeradas ou histórico paralelo.
