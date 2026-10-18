---
name: motor-de-pautas
description: "Gera um roteiro de Reels do conteúdo pessoal do Eduardo a partir de uma pauta de pautas.md: escolhe a pauta e um exemplo ainda não usado, faz 3 perguntas a ele, uma por vez, e entrega o roteiro. Use quando Eduardo pedir para ativar o motor de pautas ou gerar um conteúdo por pauta. Não use para o Pomake, carrosséis ou anúncios."
---

# Motor de pautas

Escopo: conteúdo pessoal do Eduardo. As pautas ficam em `.agents/skills/motor-de-pautas/pautas.md`, que o próprio Eduardo preenche.

Cada pauta é uma lição. A mesma lição gera vários conteúdos trocando só o exemplo. Eduardo só responde 3 perguntas e aprova. Todo o resto é da skill.

## Fluxo

Antes de começar, execute `git pull --ff-only`. Se não atualizar, pare e avise Eduardo.

Faça **uma pergunta por vez** e espere a resposta antes da próxima.

1. **Escolher a pauta.** Leia `pautas.md`. Escolha uma pauta e um exemplo que não esteja em "Exemplos já usados" dessa pauta. Mostre a Eduardo qual pauta e qual exemplo escolheu. Ele confirma ou pede outra.
2. **Caso real.** Pergunte se ele tem um caso real sobre isso (dele ou de alguém que ele conhece).
3. **Opinião forte.** Pergunte qual a opinião forte dele sobre o tema.
4. **Formato.** Pergunte o formato (tela dividida, com o monitor em cima e ele embaixo, ou só ele falando) e a duração.
5. **Roteiro.** Entregue o roteiro pronto no esqueleto abaixo. Eduardo aprova ou pede ajuste.
6. **Registrar.** Com o roteiro aprovado, adicione o exemplo em "Exemplos já usados" da pauta em `pautas.md`, faça commit e push.

## Esqueleto do roteiro

1. **Gancho:** a opinião forte dele.
2. **O erro:** o erro da pauta.
3. **Por que dá errado:** a explicação da pauta.
4. **A regra:** a regra prática aplicada ao exemplo escolhido, com o que mostrar na tela.
5. **Fechamento:** o caso real dele.

## Regras de texto

- Escreva como Eduardo fala: frases curtas, tom de conversa, primeira pessoa.
- Use as palavras e a regra das respostas dele. Se a versão dele for diferente da pauta, use a dele.
- Marque em cada bloco o tempo e o que aparece (🎥 ele ou 🖥️ tela). Em tela dividida, diga o que mostrar no monitor e dê o exemplo concreto que vai aparecer.
- O caso real e a opinião vêm só das respostas dele. Não invente caso, dado ou resultado.
