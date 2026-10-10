---
name: pomake-reels
description: "Gera o texto completo de um Reel orgânico do Pomake apresentado pela Lívia (roteiro de fala, legenda e texto do criativo), a partir da estratégia editorial do Pomake. Use quando Eduardo pedir um Reel, um conteúdo ou um vídeo da Lívia para o perfil do Pomake, com ou sem tema. Não use para anúncios do Meta Ads, carrossel, post estático ou conteúdo pessoal do Eduardo."
---

# Reels do Pomake

Você coordena a criação de um Reel do Pomake. Você não escreve nem revisa o texto e não lê os documentos da estratégia: scripts preparam o material, um **redator** escreve e um **revisor** avalia. Eduardo aprova somente o texto final; não peça aprovação entre etapas.

**Regra inegociável:** nada é gravado no repositório antes da aprovação de Eduardo. O Reel é escrito como rascunho fora do repositório e só entra em `domains/products/pomake/reels/`, com commit, quando Eduardo aprovar. (Decisão de Eduardo em 2026-10-10.)

Esta é a única skill para Reels do Pomake. Não use outras skills de conteúdo, copy, roteiro ou Reels, nem crie ou altere skills durante a execução.

Caminhos relativos à raiz do repositório. Scripts em `.agents/skills/pomake-reels/scripts/`.

## Redator e revisor

- **Com delegação a subagente disponível:** cada papel é um subagente separado. Envie a ele apenas o caminho do briefing e os dados indicados em cada passo. Nunca envie seu raciocínio nem o conteúdo de outro papel.
- **Sem delegação:** execute cada papel como uma etapa separada, lendo somente o briefing daquele papel, como se fosse a primeira vez.

As instruções de cada papel já estão dentro do briefing que o script gera.

## 1. Sincronizar

Execute `git pull --ff-only`. Se não for possível atualizar sem conflito, pare e informe Eduardo; não faça merge, rebase ou reset.

## 2. Definir a pauta

- **Sem tema de Eduardo:** execute `python3 .agents/skills/pomake-reels/scripts/preparar.py candidatas` e use as pautas na ordem listada.
- **Com tema de Eduardo:** execute `preparar.py territorios` e classifique o tema em um único território pela regra de propriedade. Depois execute `preparar.py pautas --territorio <N>`. Se uma pauta corresponder claramente ao tema, use o `id` dela; senão, a pauta é `orientacao-eduardo`. Nunca troque o tema por outro.
- Só pergunte algo a Eduardo se o pedido tiver duas leituras que mudariam o Reel. Uma pergunta, uma vez.

## 3. Redator

Gere o briefing: `preparar.py redator --pauta <ID>` ou `preparar.py redator --territorio <N> --tema "<tema>"`.

Obtenha a pasta de rascunhos com `preparar.py rascunhos`. Chame o redator com: o caminho do briefing, a data de hoje (AAAA-MM-DD) e essa pasta de rascunhos. O redator salva o rascunho e responde `ESCRITO: <caminho>` ou `INAPTA: <status> — <motivo>`.

- **INAPTA em pauta do índice:** não altere o índice; volte ao passo 3 com a próxima candidata. Após 3 pautas inaptas seguidas, pare e informe Eduardo do motivo de cada uma.
- **INAPTA em `orientacao-eduardo`:** informe Eduardo do motivo e pare.

## 4. Validar

Execute `validar_reel.py <arquivo>`. Se houver ERRO, chame o redator em modo correção (mesmo briefing, caminho do arquivo e a saída do validador). Se o erro persistir após 2 tentativas, pare e informe Eduardo.

## 5. Revisor

Gere o briefing: `preparar.py revisor <arquivo>`. Chame o revisor com o caminho do briefing e exija a resposta no formato JSON do checklist (use validação de formato da resposta, se o runtime oferecer).

- **aprovado:** siga para o passo 6 (Entregar), mesmo que haja falhas do tipo melhoria.
- **reprovado:** chame o redator em modo correção (mesmo briefing do redator, caminho do arquivo e todas as falhas do JSON). Ele reescreve o Reel inteiro. Depois repita os passos 4 e 5 uma única vez. Há no máximo **1 ciclo de correção**: se a segunda revisão ainda reprovar, siga para o passo 6 e, na entrega, informe Eduardo em uma linha cada falha bloqueante que restou.

## 6. Entregar

Leia somente o rascunho final e envie a Eduardo o pacote (Roteiro da Lívia, Legenda, Texto do criativo). Não explique o processo, salvo se ele perguntar. Não grave nada no repositório: aguarde a avaliação dele.

## Avaliação de Eduardo

**Qual rascunho:** se Eduardo não disser qual, use o rascunho mais recente da pasta de rascunhos (`preparar.py rascunhos`). Se houver mais de um e a resposta for ambígua, liste os títulos e pergunte qual, uma vez.

- **Aprovou (ou publicou):** este é o único momento em que algo é gravado.
  1. `git pull --ff-only`.
  2. Mova o rascunho para `domains/products/pomake/reels/` e troque o estado para `**Estado:** aprovado` (ou `publicado`, se ele disser que publicou).
  3. Execute `validar_reel.py` no arquivo movido.
  4. Pauta do índice: `registrar.py <ID> produzida --reel <arquivo>`. Para `orientacao-eduardo`, não altere o índice.
  5. Adicione somente o arquivo do Reel e `pautas.yaml`, faça commit `content(pomake): add reel <assunto>` e envie ao remoto. Só você faz commit; redator e revisor nunca fazem.
- **Editou o texto e aprovou:** substitua o pacote do rascunho pela versão dele e siga os passos de "Aprovou".
- **Rejeitou:** apague o rascunho. Não grave nada no repositório; a pauta continua na fila.
- **Pediu ajuste:** chame o redator em modo correção sobre o rascunho, com o pedido de Eduardo como falha a corrigir; depois repita os passos 4, 5 e 6.
- **Já publicado e depois marcado como publicado:** se Eduardo informar que publicou um Reel que já está aprovado no repositório, troque o estado para `publicado`, valide e faça commit.

## Proibições

- Não escrever nem reescrever o texto do Reel você mesmo quando houver redator disponível.
- Não ler os documentos da estratégia diretamente; use os scripts.
- Não usar como referência `domains/products/pomake/meta-ads-creative-reference.md`, `references/`, `content/` ou material de outro produto.
- Não alterar a estratégia editorial, o catálogo de ganchos ou esta skill durante a execução.
- Não gerar mais de um Reel por pedido, salvo pedido explícito de Eduardo.
- Não gravar no repositório nenhum Reel, rascunho ou alteração de índice antes da aprovação de Eduardo.
