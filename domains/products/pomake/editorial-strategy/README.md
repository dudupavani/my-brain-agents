# Estratégia editorial do Pomake

**Estado:** decisões aprovadas.
**Canais:** Instagram e TikTok.
**Fonte:** decisões aprovadas explicitamente por Eduardo em 2026-10-07.

Este diretório é a **única** estratégia de conteúdo do Pomake, executada exclusivamente pela skill [`pomake-reels`](../../../../.agents/skills/pomake-reels/SKILL.md). Qualquer outra estratégia, skill ou memória sobre conteúdo do Pomake perdeu validade em 2026-10-10 (decisão de Eduardo).

Ele registra somente decisões aprovadas. Propostas em discussão não devem ser incorporadas como definições.

## Documentos atuais

- [Fundação editorial](foundation.md): público, papel do perfil, promessa, limites e uso de setores.
- [Territórios editoriais](territories.md): os seis territórios aprovados que organizam os assuntos.
- [Banco de pautas](content-bank/): texto completo de cada pauta, indexado em `pautas.yaml`.
- [Ponte editorial](production-bridge.md): qualifica pautas pelo ganho para a audiência, narrativa e evidência antes de qualquer peça solicitada.
- [Índice de pautas](pautas.yaml): status de cada pauta do banco e Reels já produzidos a partir dela.
- [Catálogo de ganchos](hooks.md): 18 técnicas de gancho e regras de uso.

O formato do Reel e o estilo de escrita ficam nas [instruções do redator](../../../../.agents/skills/pomake-reels/references/redator.md), fonte única para o texto.

## Formato da pauta

Cada pauta é uma semente de história, escrita do ponto de vista do dono do negócio (decisão de Eduardo em 2026-10-11):

- **Situação:** uma cena do dia a dia, em segunda pessoa, com um detalhe que a pessoa consiga enxergar.
- **O que você perde:** a consequência para o negócio, como cliente, valor percebido ou tempo.
- **A virada:** o que a pessoa não percebia e que muda a forma de ver a situação.
- **O que postar** (territórios 1, 2, 3 e 6) ou **Por que isso importa** (territórios 4 e 5): uma orientação só, sem ensinar a fazer o post.

Em 2026-10-11, só a Pauta 1 de cada território está neste formato, em teste. As demais seguem no formato anterior (Cena, Contexto, Resposta desejada) até a reescrita ser aprovada.

## Conexões

- [Reels produzidos](../reels/): peças aprovadas por Eduardo, que servem de referência de qualidade, e o registro dos motivos de rejeição.
- [Definição do produto](../o-que-e-o-pomake.md): fonte aprovada para explicar o que o Pomake faz.

## Títulos usados pelo gerador

O script `.agents/skills/pomake-reels/scripts/preparar.py` extrai trechos destes documentos pelos títulos de seção abaixo. Renomear ou remover um deles faz o gerador parar com erro até o script ser atualizado.

- `foundation.md`: Público; Papel do perfil; Promessa editorial; Limites.
- `.agents/skills/pomake-reels/references/redator.md`: O que você escreve; Como um Reel prende e conduz; Limites (enviados ao revisor).
- `territories.md`: Regra de propriedade editorial; Regra de produção; os títulos numerados dos seis territórios.
- `territories/0N-*.md`: Situação humana; Trabalho editorial; Tese do Pomake; Fronteiras; Critério para reconhecer uma pauta deste território; no território 6, também Funcionamento confirmado relevante para este território.
- `production-bridge.md`: Controle de qualidade antes de qualquer publicação.
- `content-bank/0N-*.md`: os títulos `### Pauta N — <título>`.
- `../o-que-e-o-pomake.md`: Estado e uso (o texto antes dele é a definição usada).
- `hooks.md` é usado por inteiro.
