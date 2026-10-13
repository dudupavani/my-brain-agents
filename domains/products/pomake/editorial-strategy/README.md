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

Cada pauta é uma semente de história, escrita do ponto de vista do dono do negócio. O banco mantém os territórios e os IDs já usados, mas cada entrada precisa fornecer dois insumos claros:

- **Cena possível:** uma pessoa de uma profissão ou negócio identificável fazendo algo que o espectador consiga visualizar. É um exemplo hipotético, nunca apresentado como caso real.
- **Ideia de post:** o conteúdo específico que essa pessoa poderia publicar a partir da cena. A Lívia pode convidar quem assiste a encontrar um equivalente na própria rotina.

A cena não precisa representar todas as profissões ao mesmo tempo. Um exemplo específico pode fazer a pessoa de outra área reconhecer a situação equivalente. O título nomeia o momento, não uma tese sobre resultados. Uma pauta nova só entra se a cena for compreensível sem ver imagens adicionais, se a ideia de post for executável e se não repetir o argumento de outra.

Não use perda de clientes, reação do público, ganho de tempo ou resultado como conclusão automática. Só afirme o que a cena mostra ou o que uma fonte fornecida por Eduardo comprova. Se a pauta não se sustentar como história curta e compreensível, reescreva a pauta antes de produzir o Reel.

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

