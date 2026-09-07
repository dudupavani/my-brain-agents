# Protocolo da memória compartilhada

## Missão

Este repositório é a fonte de verdade dos conteúdos de Instagram. Todo agente deve tratar os arquivos como memória persistente: ler o contexto necessário antes de agir e registrar a entrega antes de encerrar.

## Sincronização

1. Antes de trabalhar, atualize o repositório a partir do remoto, quando ele estiver configurado.
2. Trabalhe somente no pacote que você recebeu ou que está inequivocamente disponível pelo seu `status`.
3. Antes de encerrar, revise os arquivos alterados, faça um commit focado e envie-o ao remoto, quando houver acesso autorizado.
4. Nunca force alterações nem sobrescreva trabalho recente de outro agente. Em caso de conflito, compare as versões e peça decisão humana se não houver uma solução óbvia.

## Pacotes e responsabilidade

Cada conteúdo existe em `content/items/<id>/`. Não mova a pasta para representar o avanço do trabalho.

- Hermes cria `metadata.yaml`, `brief.md` e `carousel.md`. Ele pode mudar `draft` para `ready_for_design` quando a copy estiver final.
- Codex só começa a partir de `ready_for_design`. Ele cria ou atualiza `deliverables/` e conduz `in_production` até `in_review`.
- Você aprova, solicita ajustes, publica e pode alterar qualquer estado.

A quantidade de slides é determinada pelo conteúdo. Não existe quantidade fixa nem número padrão herdado do modelo. Hermes deve escolher a quantidade necessária para a narrativa, registrar o total em `target.slide_count` e garantir que a copy tenha exatamente esse número de slides.

## Estados permitidos

| Estado | Significado | Próxima pessoa |
| --- | --- | --- |
| `draft` | Conteúdo ainda em elaboração | Hermes |
| `ready_for_design` | Copy final e pronta para virar carrossel | Codex |
| `in_production` | Design em andamento | Codex |
| `in_review` | Carrossel final disponível para sua revisão | Você |
| `approved` | Aprovado, aguardando publicação | Você |
| `published` | Já publicado | Nenhuma |
| `blocked` | Falta contexto, fonte, decisão ou acesso | Responsável indicado em `handoff.notes` |

Atualize `status`, `owner` e `updated_at` juntos. Use `handoff.notes` para registrar somente a próxima ação necessária quando o item estiver bloqueado ou passar para outra pessoa.

## Regras de qualidade

- Não invente fatos, fontes, resultados ou elementos da marca.
- Não reescreva a copy final de outro agente sem registrar o motivo e sem preservar a intenção.
- Não copie uma referência visual; extraia princípios e crie uma execução original.
- Não apague entregas de outro agente. Prefira uma nova versão ou peça decisão.
- Dados sensíveis, tokens, credenciais e arquivos `.env` nunca entram no repositório.

## Convenção de commits

Use mensagens curtas e rastreáveis:

```text
content(<id>): add carousel copy
design(<id>): add carousel deliverables
chore: update shared workflow
```
