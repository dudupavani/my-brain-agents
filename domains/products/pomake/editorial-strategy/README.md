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

O formato do Reel e o estilo de escrita ficam nas [instruções do redator](../../../../.agents/skills/pomake-reels/references/redator.md), fonte única para o texto.

## Formato da pauta

Cada pauta é uma semente de história, escrita do ponto de vista do dono do negócio (decisão de Eduardo em 2026-10-11):

- **Situação:** uma cena do dia a dia, em segunda pessoa, com um detalhe que a pessoa consiga enxergar.
- **O que você perde:** a consequência para o negócio, como cliente, valor percebido ou tempo.
- **A virada:** o que a pessoa não percebia e que muda a forma de ver a situação.
- **O que fazer** (territórios 1, 2, 3 e 6) ou **O que perceber** (territórios 4 e 5): uma orientação só, sem ensinar a fazer o post.

A situação é um momento que qualquer negócio vive, sem depender de uma profissão; uma cena só, contada como se conta a um amigo. O título nomeia o momento, não a tese. Uma pauta nova só entra se não repetir o argumento de outra. (Método aplicado a todo o banco em 2026-10-13.)

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
- `.agents/skills/pomake-reels/references/redator.md`: O que você escreve; Como um Reel prende e conduz; Limites (enviados ao revisor).
