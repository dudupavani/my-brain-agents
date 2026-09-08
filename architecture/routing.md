# Roteamento do cérebro compartilhado

## Sequência

1. Determine se o pedido exige apenas resposta ou uma entrega durável.
2. Identifique o domínio do artefato, independentemente de quem o produziu.
3. Leia o contrato do agente e o `AGENTS.md` do domínio.
4. Trabalhe no caminho canônico e registre fontes, responsável e estado quando aplicável.
5. Se outro agente precisar agir, crie uma nota pequena no inbox dele apontando para a origem.
6. Sincronize a entrega. Se existir tarefa no ClickUp, atualize-a com o link canônico.

## Destinos

| Informação ou entrega | Destino | Observação |
| --- | --- | --- |
| Benchmark de concorrente | `domains/products/benchmarks/<id>/` | GitHub contém o relatório; ClickUp aponta para ele |
| Pesquisa, decisão ou especificação de produto | `domains/products/` | Agrupe pelo produto quando isso já fizer sentido |
| Código-fonte de software | Repositório do software | Registre aqui somente contexto e link |
| Conteúdo pessoal para redes | `content/items/<id>/` | Siga `content/AGENTS.md` |
| Marca ou regra editorial aprovada | `references/` | Exige decisão explícita do Eduardo |
| Procedimento compartilhável | `.agents/skills/<nome>/` | Não guarde fatos de uma execução na skill |
| Material útil aos dois agentes | `shared/` | Declare propósito e responsável |
| Passagem entre agentes | `inbox/<destinatário>/` | Aponte para a origem; não duplique o artefato |

## Limites

- Não salve um artefato no diretório do agente apenas porque ele o produziu.
- Não use ClickUp e GitHub como duas fontes independentes da mesma entrega.
- Não copie memória privada do Hermes para o repositório.
- Não crie novo domínio ou repositório sem uma responsabilidade durável ou fronteira de acesso.
