# Contexto do projeto — Eduardo Agent Brain

## Missão

Este repositório é o cérebro compartilhado e versionado da operação de agentes do Eduardo. Ele guarda conhecimento durável, decisões, materiais, skills compartilhadas e entregas que precisam continuar acessíveis fora de uma conversa ou ferramenta específica.

Ele complementa, mas não substitui, a estrutura nativa de cada profile do Hermes. Identidade, personalidade, memória privada, sessões, credenciais e skills particulares permanecem no próprio profile.

O Hermes já é um runtime operacional e não é configurado por este repositório. Não altere profiles, `SOUL.md`, memória, credenciais, VPS ou configuração do Hermes como parte da manutenção deste cérebro.

Esta é a arquitetura operacional v1. Ela deve evoluir com evidência de uso; não trate decisões adiadas como se já estivessem definidas.

## Modelo mental obrigatório

- **Agente**: um profile do Hermes com identidade e memória próprias.
- **Modelo ou runtime**: Codex, Claude, Grok ou outro mecanismo usado pelo agente. O modelo não define a identidade nem o domínio do agente.
- **Cérebro**: uma visão lógica dos caminhos do GitHub que um agente consulta e mantém.
- **Domínio**: o lugar canônico de um assunto ou tipo de entrega.
- **Skill**: um procedimento reutilizável; não é memória factual nem um agente.
- **ClickUp**: sistema de acompanhamento do trabalho; não é a fonte canônica do conteúdo das entregas.

Os dois agentes ativos são:

- `products`: conversa com Eduardo sobre seus produtos e softwares, realiza pesquisas, benchmarks e mantém conhecimento de produto.
- `personal-content`: cria o conteúdo pessoal do Eduardo e mantém o fluxo editorial.

Não existe um masterbrain na v1. Eduardo conversa diretamente com cada profile. Uma futura orquestração permanece possível, mas ainda não foi decidida.

O Codex Desktop, quando Eduardo pedir trabalho sobre este repositório, atua como arquiteto e mantenedor da infraestrutura. Ele não deve se presumir um terceiro agente do Hermes nem assumir automaticamente a produção visual.

## Antes de agir

1. Leia este arquivo.
2. Leia `architecture/system.md`, `architecture/decisions.md` e `architecture/registry.yaml` quando a tarefa envolver estrutura, roteamento ou limites.
3. Leia `mapa.md` para localizar o caminho canônico.
4. Identifique seu agente pelo profile/SOUL do Hermes ou pelo pedido explícito do Eduardo. Não invente uma identidade.
5. Leia o contrato correspondente em `agents/`.
6. Ao entrar em um domínio, siga o `AGENTS.md` mais próximo e carregue apenas as referências e skills relevantes.

Se a identidade não estiver disponível e ela mudar materialmente o que pode ser alterado, peça esclarecimento. Uma solicitação explícita do Eduardo para manter a arquitetura autoriza o Codex Desktop a trabalhar em `architecture/`, `agents/`, `mapa.md`, `AGENTS.md`, `README.md` e contratos compartilhados relacionados.

## Persistência e roteamento

- Conversa casual, raciocínio temporário e rascunho descartável não entram automaticamente no GitHub.
- Pesquisa concluída, benchmark, decisão, material reutilizável, regra aprovada, skill compartilhada e entrega final devem ser registrados no domínio canônico.
- Organize pelo assunto e pela responsabilidade, não pelo agente que digitou o arquivo.
- Use `inbox/<agente>/` apenas para uma passagem real entre agentes. O artefato canônico permanece em seu domínio de origem.
- Quando o mesmo material aparecer no ClickUp e no GitHub, o GitHub é a fonte do conteúdo; o ClickUp é a fonte do acompanhamento da tarefa.
- Código-fonte de um software permanece no repositório daquele software. Este cérebro guarda contexto, pesquisa, decisões e links canônicos sobre o produto.

## Sincronização e autoria

1. Atualize o repositório antes de trabalhar, quando houver remoto configurado.
2. Preserve alterações locais ou de outro agente; nunca force sincronização nem sobrescreva trabalho recente.
3. Cada efeito persistente deve ter um responsável claro. Um agente só escreve nos caminhos permitidos em `architecture/registry.yaml`.
4. Revise os arquivos alterados, faça um commit focado e envie ao remoto quando houver acesso autorizado.
5. Em conflito não resolvível com segurança, interrompa a escrita e peça decisão ao Eduardo.

## Qualidade global

- Não invente fatos, fontes, decisões, permissões, resultados ou elementos da marca.
- Não duplique a mesma verdade em múltiplos caminhos; prefira links para a fonte canônica.
- Não salve transcrições ou dumps integrais quando uma síntese verificável for suficiente.
- Não promova uma tentativa pontual para regra ou skill sem recorrência e clareza.
- Não apague nem reescreva entregas relevantes sem preservar a rastreabilidade no Git.
- Tokens, credenciais, `.env`, dados pessoais sensíveis e segredos nunca entram no repositório.

## Commits

Use mensagens curtas e rastreáveis, por exemplo:

```text
knowledge(products): add competitor benchmark
content(<id>): add carousel package
skill: refine benchmark workflow
architecture: evolve shared brain routing
```
