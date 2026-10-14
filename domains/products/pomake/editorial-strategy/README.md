# Estratégia editorial do Pomake

**Estado:** decisões aprovadas por Eduardo (2026-10-07 a 2026-10-11); reorganizada em 2026-10-13 para servir à produção.
**Canais:** Instagram e TikTok.

Este diretório é a **única** estratégia de conteúdo do Pomake, executada exclusivamente pela skill [`pomake-reels`](../../../../.agents/skills/pomake-reels/SKILL.md). Qualquer outra estratégia, skill ou memória sobre conteúdo do Pomake perdeu validade em 2026-10-10 (decisão de Eduardo).

## Documentos

- [Fundação editorial](foundation.md): público, papel do perfil, promessa e limites.
- [Territórios editoriais](territories.md): os seis territórios, a regra de propriedade e a regra de produção.
- [Banco de pautas](content-bank/): ideias reutilizáveis, com um exemplo de recorte em cada uma.
- [Índice de pautas](pautas.yaml): status de cada pauta e Reels produzidos a partir dela.
- [Catálogo de ganchos](hooks.md): consulta editorial opcional; não entra no briefing do redator.

O conteúdo passa por pauta, [história bruta](../../../../.agents/skills/pomake-reels/references/historia.md), [matéria clara](../../../../.agents/skills/pomake-reels/references/redator.md) e [adaptação da fala para Reel](../../../../.agents/skills/pomake-reels/references/adaptador.md). A matéria precisa ser compreensível antes de receber gancho, ritmo e texto de tela.

## Formato da pauta

Cada pauta guarda uma **ideia reutilizável**. Ela pode render vários Reels quando há novas perguntas, cenas e ações para o espectador, sem repetir o argumento com outra profissão. O banco mantém os territórios e os IDs já usados. Cada entrada fornece três insumos:

- **O que a Lívia conta:** a ligação entre uma situação reconhecível e uma ideia útil. É a mensagem central da pauta, ainda sem falas prontas.
- **Exemplo de recorte:** uma pessoa de uma profissão ou negócio identificável fazendo algo que o espectador consiga visualizar. É uma possibilidade hipotética, nunca apresentada como caso real.
- **Post possível nesse recorte:** o conteúdo específico que essa pessoa poderia publicar a partir do exemplo. Outro recorte da mesma pauta precisa ter sua própria cena e ação concreta.

A cena não precisa representar todas as profissões ao mesmo tempo. Um exemplo específico pode fazer a pessoa de outra área reconhecer a situação equivalente. O título nomeia a ideia, não um roteiro único. Antes de reutilizar uma pauta, consulte os Reels ligados a ela em `pautas.yaml` e escolha um recorte cuja cena, dúvida e ação prática acrescentem algo. Trocar apenas a profissão ou as palavras não cria outro Reel. Uma pauta nova só entra se sua ideia central for distinta das existentes.

Não use perda de clientes, reação do público, ganho de tempo ou resultado como conclusão automática. Só afirme o que a cena mostra ou o que uma fonte fornecida por Eduardo comprova. Se a pauta não se sustentar como história curta e compreensível, reescreva a pauta antes de produzir o Reel.

## Como acrescentar uma pauta

1. Escreva a pauta no arquivo do território, em `content-bank/`, com o próximo número.
2. Acrescente a entrada em `pautas.yaml` com `status: ativa`. O campo `reels` guarda todos os Reels aprovados da pauta; publicar um não a encerra. Use `arquivada` somente por decisão editorial explícita.

## Títulos usados pelo gerador

O script `.agents/skills/pomake-reels/scripts/preparar.py` extrai trechos destes documentos pelos títulos abaixo. Renomear ou remover um deles faz o gerador parar com erro até o script ser atualizado.

- `foundation.md`: Público; Limites.
- `territories.md`: os títulos numerados dos seis territórios (`## N. Nome`) e Regra de propriedade editorial.
- `content-bank/0N-*.md`: os títulos `### Pauta N — <título>`.
- `../o-que-e-o-pomake.md`: Estado e uso (o texto antes dele é a definição usada no território 6).
- `hooks.md` pode ser consultado separadamente, mas não entra no briefing do redator.
- `.agents/skills/pomake-reels/references/historia.md`: instruções da história bruta.
- `.agents/skills/pomake-reels/references/redator.md`: instruções da matéria.
- `.agents/skills/pomake-reels/references/adaptador.md`: instruções da adaptação da fala para Reel.

