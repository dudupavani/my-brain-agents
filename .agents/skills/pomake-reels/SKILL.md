---
name: pomake-reels
description: "Cria um Reel orgânico do Pomake para a Lívia ou outra pessoa gravar: escolhe uma pauta, conta a história, redige a matéria e adapta a fala para vídeo curto. Use quando Eduardo pedir conteúdo ou vídeo para o perfil do Pomake, com ou sem tema. Não use para anúncios, carrosséis, posts estáticos ou conteúdo pessoal do Eduardo."
---

# Reels do Pomake

Crie **um** Reel por pedido. Escolha uma pauta e um recorte ainda não contado, desenvolva a história, redija uma matéria clara e só então adapte a fala para Reels. Cada etapa tem um papel: assunto, acontecimento, matéria e movimento do discurso. Não transforme os campos da pauta em falas por ordem. O exemplo dela é uma possibilidade, não o único assunto que pode nascer da ideia.

O pacote final é texto para gravar: roteiro falado, legenda e texto de tela. Eduardo decide se aprova. Nenhum Reel ou rascunho entra no repositório antes da aprovação dele (decisão de 2026-10-10).

Esta é a skill de conteúdo orgânico do Pomake. Caminhos relativos à raiz do repositório; scripts em `.agents/skills/pomake-reels/scripts/`.

## 1. Sincronizar

Execute `git pull --ff-only`. Se houver conflito ou alterações locais que impeçam a atualização, pare e informe Eduardo; não faça merge, rebase nem reset.

## 2. Escolher a pauta

- Sem tema: execute `python3 .agents/skills/pomake-reels/scripts/preparar.py candidatas`. Use uma pauta ativa que permita um recorte concreto, uma ideia de post executável e um argumento diferente dos Reels existentes. Uma pauta já usada continua disponível. Consulte os recortes anteriores dela antes de escolher outra cena; trocar só a profissão ou as palavras não basta.
- Com tema: execute `preparar.py territorios`, classifique-o pela regra de propriedade e veja `preparar.py pautas --territorio <N>`. Use uma pauta que corresponda claramente; caso contrário, use `orientacao-eduardo`. Não substitua o tema de Eduardo.
- Só pergunte quando duas leituras do pedido mudarem materialmente o Reel.

## 3. História bruta

Gere o briefing com `preparar.py historia --pauta <ID>` ou `preparar.py historia --territorio <N> --tema "<tema>"`. Obtenha a pasta com `preparar.py historias`.

Peça a um contador de histórias que leia **somente esse briefing** e salve `AAAA-MM-DD-<assunto>-historia.md` na pasta indicada. A resposta é `HISTORIA: <caminho>`. Ele escolhe e registra o recorte, desenvolve o acontecimento com ações e detalhes que o redator poderá usar e mostra qual post nasce dele, sem escrever gancho, legenda, chamada para salvar ou roteiro final. O tamanho vem do que a cena precisa, não de uma meta de palavras. A cena é hipotética, não uma experiência vivida pela Lívia. Se a pauta não sustentar outro recorte compreensível sem inventar fatos, escolha outra pauta ou peça a informação indispensável a Eduardo.

Com subagentes disponíveis, use um papel separado para esta etapa. Sem subagentes, execute-a como uma etapa distinta e não antecipe as regras da adaptação.

## 4. Redigir a matéria

Gere o briefing com `preparar.py redator --pauta <ID>` ou `preparar.py redator --territorio <N> --tema "<tema>"`. Obtenha a pasta com `preparar.py materias`.

Peça ao redator que leia **o briefing e a história bruta**. A história é o insumo principal. Ele torna compreensível a ação compartilhada por espectadores de profissões diferentes, desenvolve o que acontece e mostra qual post nasce dali. A matéria preserva detalhes úteis sem virar roteiro final, gancho, legenda ou texto de tela. Ele salva `AAAA-MM-DD-<assunto>-materia.md` na pasta de matérias e responde `MATERIA: <caminho>`.

Com subagentes disponíveis, use um papel diferente do contador de histórias. Sem subagentes, trate esta etapa como uma nova leitura da história, primeiro entendendo-a sem consultar a pauta.

## 5. Adaptar a fala para Reels

Gere o briefing com `preparar.py adaptador`. Obtenha a pasta com `preparar.py rascunhos`.

Peça a um adaptador de Reels que leia **somente o briefing e a matéria do redator**. Ele recria a matéria como fala com movimento: ações, reações e viradas que se encadeiam, com abertura forte e aplicação concreta no próximo post. Dinamismo deve estar nas palavras; não peça direção de câmera, gestos, cortes ou som. Ele não escolhe outro tema nem inventa fatos para criar impacto. Salva `AAAA-MM-DD-<assunto>.md` na pasta de rascunhos e responde `ESCRITO: <caminho>`.

Com subagentes disponíveis, use um papel separado do redator. Sem subagentes, trate esta como uma etapa distinta e leia primeiro a matéria sem consultar a história ou a pauta.

## 6. Conferir e entregar

Execute `validar_reel.py <arquivo>`. Corrija erros mecânicos com o adaptador, no máximo duas tentativas. Leia o roteiro **sem o briefing** como se estivesse ouvindo pela primeira vez: há uma sequência de ações que move a fala, ou apenas uma explicação em frases curtas? A pessoa reconheceria a situação mesmo trabalhando em outra área? O texto mostra uma aplicação concreta antes de convidar a agir? Se houver uma lacuna na fala, peça ao adaptador para recontar; se faltar matéria, volte à etapa 4; se faltar acontecimento, volte à etapa 3 ou escolha outra pauta. Não preencha a lacuna com uma explicação sua. A validação automática não prova que a fala soa humana.

Entregue a Eduardo somente roteiro, legenda e texto de tela. Esta conferência não é uma revisão formal nem um checklist criativo. A leitura e os testes de gravação de Eduardo orientam as próximas versões.

## Avaliação de Eduardo

Se ele pedir ajuste, passe o comentário e a matéria ao adaptador; quando o problema for a matéria ou a história, volte à etapa correspondente. Depois valide e entregue de novo. Se não identificar qual rascunho ele avaliou, use o mais recente; se houver ambiguidade real, pergunte uma vez.

- **Aprovou ou publicou:** `git pull --ff-only`; mova o rascunho para `domains/products/pomake/reels/`; mude `**Estado:**` para `aprovado` ou `publicado`; valide. Para pauta do banco, execute `registrar.py <ID> --reel <arquivo>`. O Reel entra na lista da pauta, que continua ativa para outros recortes. Adicione só o Reel e, quando alterado, `pautas.yaml`; faça commit `content(pomake): add reel <assunto>` e envie ao remoto.
- **Editou e aprovou:** substitua o pacote pela versão de Eduardo antes de seguir o passo anterior.
- **Rejeitou:** apague os rascunhos da história, da matéria e do Reel. Se ele deu o motivo, registre somente suas palavras com `rejeitar.py <ID|orientacao-eduardo> "<motivo>"`, faça commit apenas de `rejeicoes.md` e envie ao remoto. Sem motivo, não grave nada e não pergunte. A pauta permanece ativa.
- **Marcado como publicado depois da aprovação:** atualize o estado do Reel, valide e faça commit.

Não use textos rejeitados como exemplos. Não altere estratégia, banco de pautas ou esta skill enquanto estiver produzindo um Reel. Não grave história, matéria, briefing ou rascunho no repositório.
