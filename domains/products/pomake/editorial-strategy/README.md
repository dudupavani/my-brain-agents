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
- [Reel com a Lívia](reel-livia.md): único formato do conteúdo orgânico e pacote de texto de cada peça.
- [Voz e padrão de copy](voice.md): gancho forte sem agressividade, regras de voz e estrutura de referência.
- [Catálogo de ganchos](hooks.md): 18 técnicas de gancho e regras de uso.

## Conexões

- [Reels produzidos](../reels/): peças aprovadas por Eduardo, que servem de referência de qualidade, e o registro dos motivos de rejeição.
- [Definição do produto](../o-que-e-o-pomake.md): fonte aprovada para explicar o que o Pomake faz.

## Títulos usados pelo gerador

O script `.agents/skills/pomake-reels/scripts/preparar.py` extrai trechos destes documentos pelos títulos de seção abaixo. Renomear ou remover um deles faz o gerador parar com erro até o script ser atualizado.

- `foundation.md`: Público; Papel do perfil; Promessa editorial; Limites; Linguagem e criação.
- `territories.md`: Regra de propriedade editorial; Regra de produção; os títulos numerados dos seis territórios.
- `territories/0N-*.md`: Situação humana; Trabalho editorial; Tese do Pomake; Fronteiras; Critério para reconhecer uma pauta deste território; no território 6, também Funcionamento confirmado relevante para este território.
- `production-bridge.md`: Controle de qualidade antes de qualquer publicação.
- `content-bank/0N-*.md`: os títulos `### Pauta N — <título>`.
- `../o-que-e-o-pomake.md`: Estado e uso (o texto antes dele é a definição usada).
- `hooks.md`, `voice.md` e `reel-livia.md` são usados por inteiro.
