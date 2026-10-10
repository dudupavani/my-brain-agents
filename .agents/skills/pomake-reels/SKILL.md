---
name: pomake-reels
description: "Gera o texto completo de um Reel orgânico do Pomake apresentado pela Lívia (roteiro de fala, legenda e texto do criativo), a partir da estratégia editorial do Pomake. Use quando Eduardo pedir um Reel, um conteúdo ou um vídeo da Lívia para o perfil do Pomake, com ou sem tema. Não use para anúncios do Meta Ads, carrossel, post estático ou conteúdo pessoal do Eduardo."
---

# Reels do Pomake

Conduza a criação de um Reel do Pomake da escolha da pauta até a entrega do texto final. Eduardo aprova somente o texto final; não peça aprovação entre etapas.

Esta é a única skill para Reels do Pomake. Não use outras skills de conteúdo, copy, roteiro ou Reels do profile para esta tarefa, nem crie ou altere skills durante a execução.

Todos os caminhos abaixo são relativos à raiz do repositório.

## Antes de tudo: sincronizar

Execute `git pull --ff-only` na raiz do repositório antes de qualquer leitura. Se não for possível atualizar sem conflito, pare e informe Eduardo; não faça merge, rebase ou reset.

## Leitura obrigatória

Antes de escrever, leia por completo:

1. `domains/products/pomake/editorial-strategy/foundation.md`
2. `domains/products/pomake/editorial-strategy/territories.md`
3. `domains/products/pomake/editorial-strategy/production-bridge.md`
4. `domains/products/pomake/editorial-strategy/voice.md`
5. `domains/products/pomake/editorial-strategy/hooks.md`
6. `domains/products/pomake/editorial-strategy/reel-livia.md`
7. `domains/products/pomake/creative-direction/livia.md`
8. `domains/products/pomake/editorial-strategy/pautas.yaml`
9. Todos os arquivos de `domains/products/pomake/reels/`, exceto o `README.md`.

Depois de escolher a pauta, leia também o arquivo do território dela, a pauta no banco (`arquivo` indicado em `pautas.yaml`) e, se o território for 6, `domains/products/pomake/o-que-e-o-pomake.md`.

Não leia nem use como referência: `domains/products/pomake/meta-ads-creative-reference.md`, `references/`, `content/` ou qualquer material de outro produto.

## Processo

Execute as etapas na ordem. Não pule nem junte etapas.

### 1. Definir a pauta

- **Eduardo deu tema, ângulo ou situação:** classifique o pedido em um único território, pela regra de propriedade de `territories.md`. Se corresponder a uma pauta do índice, use o `id` dela; caso contrário, a pauta é `orientacao-eduardo`. Não troque o tema pedido por outro.
- **Eduardo não deu orientação:** escolha em `pautas.yaml` uma pauta com status `apta` ou `nao_avaliada`. Prefira `apta`. Nunca escolha `produzida`, `aguardar_material` ou `descartada`. O território deve ser diferente do território do Reel mais recente em `reels/`. O mais recente é o de maior data no nome do arquivo; em empate, o último adicionado segundo `git log`.
- Só pergunte algo a Eduardo se o pedido tiver duas leituras que mudariam o Reel. Faça uma pergunta, uma vez.

### 2. Aplicar a ponte editorial

Avalie a pauta pelos 6 critérios de `production-bridge.md` e decida: **apta**, **aguardar material** ou **descartar**. No índice, esses vereditos correspondem aos status `apta`, `aguardar_material` e `descartada`.

- Cena hipotética em segunda pessoa não exige material. Caso real, número, depoimento, estudo ou fonte exigem material verdadeiro disponível.
- Se a pauta do índice não for apta, registre o status (passo 7, comando `registrar.py`) e escolha outra. Após 3 pautas reprovadas seguidas, pare e informe Eduardo do motivo de cada uma.
- Se a pauta for `orientacao-eduardo` e não for apta, não troque o tema: explique a Eduardo o critério que falhou e o que falta.

### 3. Montar o núcleo (interno, não é entregue)

Defina, em uma linha cada:

- **Situação:** a cena reconhecível da rotina.
- **Tensão:** por que a pessoa continuaria assistindo.
- **Virada:** o detalhe que muda a forma de ver a situação.
- **Orientação:** o que a pessoa pode fazer de diferente no próprio negócio.

Escreva 3 ganchos para a Fala 1, cada um com uma técnica diferente de `hooks.md`, respeitando as regras de uso do catálogo. Escolha o mais forte para este público e esta pauta.

Faça o mesmo para o texto do criativo: 3 opções, cada uma com técnica diferente, seguindo as regras de `reel-livia.md` (seção "Texto do criativo"). Descarte toda opção que seja uma afirmação que se encerra sozinha, sem abrir curiosidade nem mostrar o que está em jogo. Escolha a mais forte.

### 4. Escrever o pacote

Escreva o pacote exatamente no formato de `reel-livia.md`: roteiro da Lívia, legenda e texto do criativo.

- A Fala 1 é o gancho escolhido e deve funcionar nos primeiros 3 segundos.
- O roteiro é texto para ser falado. Leia cada fala como se fosse dita em voz alta e reescreva o que soar como texto escrito.
- O roteiro completo tem no mínimo 40 palavras (Reel de no mínimo 15 segundos).
- Escolha o pedido do fechamento pelo tipo de conteúdo, conforme `reel-livia.md`: salvar (dica de como agir) ou enviar a quem vai gostar de saber (outro tipo). A legenda termina com o mesmo tipo de pedido.
- Legenda sem hashtags e sem emojis.
- Use os Reels com estado `aprovado` ou `publicado` como referência de nível e voz. Não copie frases deles, não repita aberturas, transições ou fechamentos de nenhum Reel existente e não repita o argumento de nenhum deles.
- Evite tudo o que aparece como motivo de rejeição nos Reels com estado `rejeitado`.

### 5. Salvar e validar

Salve em `domains/products/pomake/reels/AAAA-MM-DD-<assunto>.md`, usando a data atual e um assunto curto em minúsculas, sem acentos e com hífens. Use exatamente este cabeçalho:

```
# Reel — <título curto>

**Estado:** proposta
**Pauta:** <id da pauta ou orientacao-eduardo>
**Território:** <número de 1 a 6>
**Técnica do gancho:** <números das técnicas usadas na Fala 1>
**Técnica do criativo:** <números das técnicas usadas no texto do criativo>
```

Em seguida, as seções `## Roteiro da Lívia`, `## Legenda` e `## Texto do criativo`, como em `reel-livia.md`.

Execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`. Corrija o que falhar e execute de novo até passar.

### 6. Revisão independente

A revisão usa o arquivo salvo, o checklist `.agents/skills/pomake-reels/references/revisao.md` e os documentos que o próprio checklist manda consultar (catálogo de ganchos, voz, formato, Reels existentes e, no território 6, a definição do Pomake). Ela nunca usa o núcleo nem o raciocínio da criação.

- **Se o runtime permitir delegar a um subagente:** envie a ele apenas o caminho do arquivo, o caminho do checklist e a instrução de aplicar o checklist, consultando os documentos que ele indica, e devolver o resultado no formato definido. Não envie o núcleo nem o raciocínio da criação.
- **Se não permitir:** abra uma etapa nova de revisão, releia o arquivo salvo e o checklist do zero e avalie como se não tivesse escrito o texto.

Se a revisão reprovar, corrija somente os itens apontados, salve, valide (passo 5) e revise de novo. No máximo 2 ciclos de correção. Se ainda houver reprovação, entregue mesmo assim e informe Eduardo, em uma linha, o item que não passou.

### 7. Registrar

- Atualize o índice: `python3 .agents/skills/pomake-reels/scripts/registrar.py <id-da-pauta> produzida --reel <arquivo>`. Para `orientacao-eduardo`, não altere o índice.
- Siga as regras de sincronização e commit de `AGENTS.md`: `git pull --ff-only` antes, commit focado (`content(pomake): add reel <assunto>`) e envio ao remoto quando houver acesso.

### 8. Entregar

Envie a Eduardo somente o pacote final, no formato de `reel-livia.md`, seguido de uma linha com o caminho do arquivo. Não explique o processo, as técnicas ou a ponte editorial, salvo se ele perguntar.

## Retorno de Eduardo

Quando Eduardo avaliar um Reel, sincronize o repositório (`git pull --ff-only`), identifique o Reel e atualize o arquivo dele, valide e faça commit.

**Qual Reel:** se Eduardo não disser qual, use o Reel com estado `proposta` mais recente. Se houver mais de um Reel em `proposta`, liste os títulos e pergunte qual, uma vez.


- **Aprovou:** `**Estado:** aprovado`.
- **Publicou:** `**Estado:** publicado`.
- **Rejeitou:** `**Estado:** rejeitado` e uma seção `## Avaliação de Eduardo` com o motivo nas palavras dele. Não invente motivo; se ele não disser, pergunte uma vez. Depois, atualize a pauta (exceto `orientacao-eduardo`):
  - motivo ligado ao texto (gancho, falas, tom, legenda): a pauta volta para a fila com `registrar.py <id> apta`;
  - motivo ligado ao assunto, ou segunda rejeição da mesma pauta: `registrar.py <id> descartada`;
  - se o motivo não deixar claro se é texto ou assunto, pergunte uma vez.
- **Editou o texto:** substitua o pacote pela versão dele e registre, em `## Avaliação de Eduardo`, o que mudou entre a versão gerada e a versão final.
- **Pediu ajuste:** altere somente o Reel citado, valide, revise (passo 6) e entregue de novo.

## Proibições

- Não citar o Pomake fora do território 6. No território 6, sem preço, oferta, convite direto ou chamada de compra.
- Não inventar número, cliente, caso, depoimento, estudo, fonte ou função do Pomake.
- Não prometer resultado garantido.
- Não ensinar ferramentas (Canva, prompts, edição, montagem de arte).
- Não usar nomes internos de territórios, séries ou pautas no texto do Reel.
- Não gerar direção visual, cenário, enquadramento ou prompt de takes.
- Não gerar mais de um Reel por pedido, salvo pedido explícito de Eduardo.
- Não alterar a estratégia editorial, o catálogo de ganchos ou esta skill durante a execução.
