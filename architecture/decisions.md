# Decisões da arquitetura

Este arquivo separa decisões ativas, hipóteses em validação e possibilidades futuras.

## Ativas na v1

- Existem dois agentes lógicos: `products` e `personal-content`.
- Cada agente corresponde a um profile independente do Hermes.
- Os profiles e a operação do Hermes já existem e ficam fora do escopo deste repositório.
- Identidade e memória privada não são duplicadas no GitHub.
- O repositório é a fonte canônica de conhecimento e entregas compartilháveis.
- A v1 usa um repositório com dois cérebros lógicos, pois ainda não há fronteira real de permissão entre eles.
- Materiais são organizados pelo domínio, não pelo agente ou modelo que os produziu.
- ClickUp acompanha o trabalho; GitHub mantém o conteúdo canônico da entrega.
- Skills maduras e portáteis vivem em `.agents/skills/`.
- Um efeito persistente tem um responsável e um caminho canônico.
- Código-fonte permanece no repositório do software correspondente.
- Codex, Claude, Grok e outros são runtimes intercambiáveis.

## Provisórias e em validação

- O agente `personal-content` pode conduzir o fluxo editorial completo usando skills distintas, sem depender de um agente separado chamado Codex.
- `inbox/` será usado somente em passagens concretas entre os dois agentes.
- Os formatos internos de benchmark e de conteúdo podem evoluir após casos reais.
- A produção visual automática de carrosséis continua experimental e exige pedido explícito enquanto sua qualidade não estiver validada.

## Adiadas — não presumir que existem

- masterbrain ou agente orquestrador;
- memória semântica compartilhada entre profiles do Hermes;
- sincronização automática entre GitHub e ClickUp;
- scraping e seleção automática de pautas;
- publicação automática em redes sociais;
- múltiplos repositórios por agente ou empresa;
- branches, pull requests ou auto-merge por categoria de alteração.

## Quando revisar

Revise a arquitetura quando surgir um terceiro agente, uma empresa ou equipe com permissões diferentes, uma automação recorrente ou uma falha repetida de roteamento. A revisão deve partir de casos reais.
