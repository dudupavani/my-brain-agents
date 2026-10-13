# Estratégia editorial do Pomake

**Estado:** decisões aprovadas por Eduardo (2026-10-07 a 2026-10-11); reorganizada em 2026-10-13 para servir à produção.
**Canais:** Instagram e TikTok.

Este diretório é a **única** estratégia de conteúdo do Pomake, executada exclusivamente pela skill [`pomake-reels`](../../../../.agents/skills/pomake-reels/SKILL.md). Qualquer outra estratégia, skill ou memória sobre conteúdo do Pomake perdeu validade em 2026-10-10 (decisão de Eduardo).

## Documentos

- [Fundação editorial](foundation.md): público, papel do perfil, promessa e limites.
- [Territórios editoriais](territories.md): os seis territórios, a regra de propriedade e a regra de produção.
- [Banco de pautas](content-bank/): uma pauta por situação, por território.
- [Índice de pautas](pautas.yaml): status de cada pauta e Reels produzidos a partir dela.
- [Catálogo de ganchos](hooks.md): 18 técnicas de gancho e regras de uso.

O conteúdo passa por pauta, [história bruta](../../../../.agents/skills/pomake-reels/references/historia.md) e [adaptação para Reel](../../../../.agents/skills/pomake-reels/references/redator.md). A história precisa ser compreensível antes de receber gancho, duração e texto de tela.

## Formato da pauta

Cada pauta é uma semente de história, escrita do ponto de vista do dono do negócio (decisão de Eduardo em 2026-10-11). Os quatro campos abaixo são hipóteses para explorar, não falas prontas nem uma sequência obrigatória no vídeo:

- **Situação:** uma cena do dia a dia, em segunda pessoa, com um detalhe que a pessoa consiga enxergar.
- **O que você perde:** a consequência para o negócio, como cliente, valor percebido ou tempo.
- **A virada:** o que a pessoa não percebia e que muda a forma de ver a situação.
- **O que fazer** (territórios 1, 2, 3 e 6) ou **O que perceber** (territórios 4 e 5): uma orientação só, sem ensinar a fazer o post.

A situação deve poder ser reconhecida sem exigir que todo o público tenha a mesma profissão. Isso não exige uma cena genérica: um objeto, uma ação ou uma fala concreta ajudam a pessoa a visualizar o momento. Quando a pauta depende de um trabalho específico, use-o como exemplo hipotético claro, sem apresentá-lo como caso real. O título nomeia o momento, não a tese. Uma pauta nova só entra se não repetir o argumento de outra. (Método aplicado a todo o banco em 2026-10-13.)

O banco existente contém cenas hipotéticas. Afirmações como "o cliente passa direto" ou "o perfil perde confiança" indicam uma consequência possível, não um comportamento observado ou garantido. Quem conta a história pode descartá-las quando não decorrerem claramente da cena. Não atribua resultados reais a clientes sem evidência. Se uma pauta não se sustentar como história curta e compreensível, escolha outra em vez de forçar uma virada.

## Como acrescentar uma pauta

1. Escreva a pauta no arquivo do território, em `content-bank/`, com o próximo número.
2. Acrescente a entrada em `pautas.yaml` com `status: disponivel`.

## Títulos usados pelo gerador

O script `.agents/skills/pomake-reels/scripts/preparar.py` extrai trechos destes documentos pelos títulos abaixo. Renomear ou remover um deles faz o gerador parar com erro até o script ser atualizado.

- `foundation.md`: Público; Limites.
- `territories.md`: os títulos numerados dos seis territórios (`## N. Nome`) e Regra de propriedade editorial.
- `content-bank/0N-*.md`: os títulos `### Pauta N — <título>`.
- `../o-que-e-o-pomake.md`: Estado e uso (o texto antes dele é a definição usada no território 6).
- `hooks.md` é usado por inteiro.
- `.agents/skills/pomake-reels/references/historia.md`: instruções da história bruta.
- `.agents/skills/pomake-reels/references/redator.md`: instruções da adaptação para Reel.

