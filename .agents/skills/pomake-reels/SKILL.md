---
name: pomake-reels
description: "Gera o texto completo de um Reel orgânico do Pomake apresentado pela Lívia (roteiro de fala, legenda e texto do criativo), a partir da estratégia editorial do Pomake. Use quando Eduardo pedir um Reel, um conteúdo ou um vídeo da Lívia para o perfil do Pomake, com ou sem tema. Não use para anúncios do Meta Ads, carrossel, post estático ou conteúdo pessoal do Eduardo."
---

# Reels do Pomake

Você coordena a criação de um Reel do Pomake. Você não escreve nem revisa o texto e não lê os documentos da estratégia: scripts preparam o material, um **redator** escreve e um **revisor** avalia. Eduardo aprova somente o texto final; não peça aprovação entre etapas.

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

Chame o redator com: o caminho do briefing, a data de hoje (AAAA-MM-DD) e a pasta `domains/products/pomake/reels/`. O redator salva o arquivo e responde `ESCRITO: <caminho>` ou `INAPTA: <status> — <motivo>`.

- **INAPTA em pauta do índice:** execute `registrar.py <ID> <aguardar_material|descartada>` e volte ao passo 3 com a próxima candidata. Após 3 pautas inaptas seguidas, pare e informe Eduardo do motivo de cada uma.
- **INAPTA em `orientacao-eduardo`:** informe Eduardo do motivo e pare.

## 4. Validar

Execute `validar_reel.py <arquivo>`. Se houver ERRO, chame o redator em modo correção (mesmo briefing, caminho do arquivo e a saída do validador). Se o erro persistir após 2 tentativas, pare e informe Eduardo.

## 5. Revisor

Gere o briefing: `preparar.py revisor <arquivo>`. Chame o revisor com o caminho do briefing e exija a resposta no formato JSON do checklist (use validação de formato da resposta, se o runtime oferecer).

- **aprovado:** siga para o passo 6, mesmo que haja falhas do tipo melhoria.
- **reprovado:** chame o redator em modo correção (mesmo briefing do redator, caminho do arquivo e todas as falhas do JSON). Ele reescreve o Reel inteiro. Depois repita os passos 4 e 5 uma única vez. Há no máximo **1 ciclo de correção**: se a segunda revisão ainda reprovar, siga para o passo 6 e, na entrega, informe Eduardo em uma linha cada falha bloqueante que restou.

## 6. Registrar

- Pauta do índice: `registrar.py <ID> produzida --reel <arquivo>`. Para `orientacao-eduardo`, não altere o índice.
- `git pull --ff-only`, adicione somente o arquivo do Reel e `pautas.yaml`, faça commit `content(pomake): add reel <assunto>` e envie ao remoto. Só você faz commit; redator e revisor nunca fazem.

## 7. Entregar

Leia somente o arquivo final do Reel e envie a Eduardo o pacote (Roteiro da Lívia, Legenda, Texto do criativo), seguido de uma linha com o caminho do arquivo. Não explique o processo, salvo se ele perguntar.

## Retorno de Eduardo

Sincronize (`git pull --ff-only`), identifique o Reel, atualize o arquivo, valide e faça commit.

**Qual Reel:** se Eduardo não disser qual, use o Reel com estado `proposta` mais recente. Se houver mais de um Reel em `proposta`, liste os títulos e pergunte qual, uma vez.

- **Aprovou:** `**Estado:** aprovado`.
- **Publicou:** `**Estado:** publicado`.
- **Rejeitou:** `**Estado:** rejeitado` e uma seção `## Avaliação de Eduardo` com o motivo nas palavras dele. Não invente motivo; se ele não disser, pergunte uma vez. Depois, atualize a pauta (exceto `orientacao-eduardo`):
  - motivo ligado ao texto (gancho, falas, tom, legenda): `registrar.py <ID> apta`, e a pauta volta para a fila;
  - motivo ligado ao assunto, ou segunda rejeição da mesma pauta: `registrar.py <ID> descartada`;
  - se não ficar claro se é texto ou assunto, pergunte uma vez.
- **Editou o texto:** substitua o pacote pela versão dele e registre, em `## Avaliação de Eduardo`, o que mudou entre a versão gerada e a versão final.
- **Pediu ajuste:** chame o redator em modo correção com o pedido de Eduardo como falha a corrigir; depois repita os passos 4, 5 e 7.

## Proibições

- Não escrever nem reescrever o texto do Reel você mesmo quando houver redator disponível.
- Não ler os documentos da estratégia diretamente; use os scripts.
- Não usar como referência `domains/products/pomake/meta-ads-creative-reference.md`, `references/`, `content/` ou material de outro produto.
- Não alterar a estratégia editorial, o catálogo de ganchos ou esta skill durante a execução.
- Não gerar mais de um Reel por pedido, salvo pedido explícito de Eduardo.
