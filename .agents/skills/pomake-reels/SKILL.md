---
name: pomake-reels
description: "Cria um Reel orgânico do Pomake para a Lívia ou outra pessoa gravar: escolhe uma pauta, conta a história em linguagem falada e a adapta para roteiro, legenda e texto de tela. Use quando Eduardo pedir conteúdo ou vídeo para o perfil do Pomake, com ou sem tema. Não use para anúncios, carrosséis, posts estáticos ou conteúdo pessoal do Eduardo."
---

# Reels do Pomake

Crie **um** Reel por pedido. O fluxo tem três decisões: escolher a pauta, contar a história de modo compreensível e só então adaptá-la ao tempo e à linguagem de Reel. Não transforme os campos da pauta em falas por ordem. Eles são possibilidades para explorar, não uma estrutura obrigatória.

O pacote final é texto para gravar: roteiro falado, legenda e texto de tela. Eduardo decide se aprova. Nenhum Reel ou rascunho entra no repositório antes da aprovação dele (decisão de 2026-10-10).

Esta é a skill de conteúdo orgânico do Pomake. Caminhos relativos à raiz do repositório; scripts em `.agents/skills/pomake-reels/scripts/`.

## 1. Sincronizar

Execute `git pull --ff-only`. Se houver conflito ou alterações locais que impeçam a atualização, pare e informe Eduardo; não faça merge, rebase nem reset.

## 2. Escolher a pauta

- Sem tema: execute `python3 .agents/skills/pomake-reels/scripts/preparar.py candidatas`. Use a primeira pauta que ofereça uma situação clara, uma ideia de post executável e um argumento diferente dos Reels existentes. A cena pode escolher uma profissão específica; não precisa representar todas ao mesmo tempo. Se a pauta for vaga, escolha outra ou reescreva a pauta antes de produzir.
- Com tema: execute `preparar.py territorios`, classifique-o pela regra de propriedade e veja `preparar.py pautas --territorio <N>`. Use uma pauta que corresponda claramente; caso contrário, use `orientacao-eduardo`. Não substitua o tema de Eduardo.
- Só pergunte quando duas leituras do pedido mudarem materialmente o Reel.

## 3. História bruta

Gere o briefing com `preparar.py historia --pauta <ID>` ou `preparar.py historia --territorio <N> --tema "<tema>"`. Obtenha a pasta com `preparar.py historias`.

Peça a um contador de histórias que leia **somente esse briefing** e salve `AAAA-MM-DD-<assunto>-historia.md` na pasta indicada. A resposta é `HISTORIA: <caminho>`. Ele deve contar o acontecimento em linguagem falada, sem escrever gancho, legenda, chamada para salvar ou roteiro final. A cena da pauta é hipotética, não uma experiência vivida pela Lívia. Se a pauta não sustentar uma história compreensível sem inventar fatos, ele sinaliza isso; escolha outra pauta ou peça a informação indispensável a Eduardo.

Com subagentes disponíveis, use um papel separado para esta etapa. Sem subagentes, execute-a como uma etapa distinta e não antecipe as regras da adaptação.

## 4. Adaptar para Reel

Gere o briefing com `preparar.py redator --pauta <ID>` ou `preparar.py redator --territorio <N> --tema "<tema>"`. Obtenha a pasta com `preparar.py rascunhos`.

Peça ao adaptador que leia **o briefing e a história bruta**. A história é o insumo principal: preserve o que aconteceu e o que a pessoa precisa entender, cortando ou mudando apenas o necessário para caber num Reel. Ele escreve uma fala contínua, que funciona com a Lívia diante da câmera e legendas da fala, sem depender de imagens extras. Ele salva `AAAA-MM-DD-<assunto>.md` na pasta de rascunhos e responde `ESCRITO: <caminho>`. Não acrescente uma moral, uma consequência, uma pergunta ou um pedido final só para preencher uma fórmula.

Com subagentes disponíveis, use um papel diferente do contador de histórias. Sem subagentes, trate esta etapa como uma nova leitura da história, primeiro entendendo-a sem consultar a pauta.

## 5. Conferir e entregar

Execute `validar_reel.py <arquivo>`. Corrija erros mecânicos com o adaptador, no máximo duas tentativas. Leia o roteiro **sem o briefing** como se estivesse ouvindo pela primeira vez: fica claro logo de que se trata, é possível imaginar o que a pessoa fez ou viu e o espectador sai com uma ideia de post que pode fazer? Se houver uma lacuna no texto, peça ao adaptador para recontar; se faltar uma cena na própria história, volte à etapa 3 ou escolha outra pauta. Não preencha a lacuna com uma explicação sua. A leitura de alguém que não participou da criação é a melhor verificação quando disponível; a validação automática não prova que a fala soa humana.

Entregue a Eduardo somente roteiro, legenda e texto de tela. Esta conferência não é uma revisão formal nem um checklist criativo. A leitura e os testes de gravação de Eduardo orientam as próximas versões.

## Avaliação de Eduardo

Se ele pedir ajuste, passe o comentário e a história bruta ao adaptador; quando o problema for a própria história, volte à etapa 3. Depois valide e entregue de novo. Se não identificar qual rascunho ele avaliou, use o mais recente; se houver ambiguidade real, pergunte uma vez.

- **Aprovou ou publicou:** `git pull --ff-only`; mova o rascunho para `domains/products/pomake/reels/`; mude `**Estado:**` para `aprovado` ou `publicado`; valide. Para pauta do banco, execute `registrar.py <ID> produzida --reel <arquivo>`. Adicione só o Reel e, quando alterado, `pautas.yaml`; faça commit `content(pomake): add reel <assunto>` e envie ao remoto.
- **Editou e aprovou:** substitua o pacote pela versão de Eduardo antes de seguir o passo anterior.
- **Rejeitou:** apague os rascunhos da história e do Reel. Se ele deu o motivo, registre somente suas palavras com `rejeitar.py <ID|orientacao-eduardo> "<motivo>"`, faça commit apenas de `rejeicoes.md` e envie ao remoto. Sem motivo, não grave nada e não pergunte. A pauta permanece disponível.
- **Marcado como publicado depois da aprovação:** atualize o estado do Reel, valide e faça commit.

Não use textos rejeitados como exemplos. Não altere estratégia, banco de pautas ou esta skill enquanto estiver produzindo um Reel. Não grave história, briefing ou rascunho no repositório.

