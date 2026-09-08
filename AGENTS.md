# Protocolo da memória global

## Propósito

Este repositório é a memória persistente e a fonte de verdade do sistema de agentes do Eduardo. Ele centraliza materiais, decisões, referências, instruções, skills e entregas em um único lugar.

Os agentes são perfis independentes no Hermes. Não existe um agente orquestrador: cada perfil deve identificar o próprio escopo, ler as regras do domínio correspondente e salvar o resultado no local correto.

O GitHub é o meio de sincronização. A memória é formada pelos arquivos, pela arquitetura e pelo histórico versionado do repositório.

## Como localizar o trabalho

Antes de agir, todo agente deve:

1. Ler este arquivo.
2. Consultar `architecture/registry.yaml` para identificar o próprio contrato, domínio e caminhos permitidos.
3. Ler o contrato do agente em `agents/` e as regras do domínio antes de criar ou alterar arquivos.
4. Trabalhar somente dentro do escopo identificado.
5. Registrar a entrega no repositório quando ela for uma decisão, material ou artefato persistente.

Se o pedido não tiver um domínio claro, o agente deve pedir esclarecimento antes de salvar em um local arbitrário.

O mapa de navegação está em `mapa.md`. As regras de roteamento estão em `architecture/routing.md`.

## O agente pessoal e suas capacidades

O perfil `personal-content` é um assistente pessoal generalista. Ele pode criar, organizar e manter diferentes tipos de conteúdo e materiais. Instagram não define o escopo do agente: é apenas uma das capacidades disponíveis por meio de skills.

Ao trabalhar com conteúdo editorial para Instagram, ele deve ler `references/brand/brand.md` e `references/editorial/content-system.md` e seguir o contrato da capacidade em `agents/hermes/CONTENT.md`.

Conversa, pesquisa e rascunho não entram automaticamente no GitHub. O agente só cria ou altera `content/items/<id>/` quando Eduardo pedir explicitamente para preparar o conteúdo para o Codex. Nesse caso, também deve ler e seguir `agents/hermes/HANDOFF.md`.

## Sincronização

1. Antes de trabalhar, atualize o repositório a partir do remoto, quando ele estiver configurado.
2. Trabalhe somente no pacote que você recebeu ou que está inequivocamente disponível pelo seu `status`.
3. Antes de encerrar, revise os arquivos alterados, faça um commit focado e envie-o ao remoto, quando houver acesso autorizado.
4. Nunca force alterações nem sobrescreva trabalho recente de outro agente. Em caso de conflito, compare as versões e peça decisão humana se não houver uma solução óbvia.

## Pacotes da capacidade de carrossel para Instagram

Cada conteúdo existe em `content/items/<id>/`. Não mova a pasta para representar o avanço do trabalho.

- Hermes cria `metadata.yaml`, `brief.md` e `carousel.md`. Ele pode mudar `draft` para `ready_for_design` quando a copy estiver final.
- Codex só começa a partir de `ready_for_design`. Ele cria ou atualiza `deliverables/` e conduz `in_production` até `in_review`.
- Você aprova, solicita ajustes, publica e pode alterar qualquer estado.

A quantidade de slides é determinada pelo conteúdo. Não existe quantidade fixa nem número padrão herdado do modelo. Hermes deve escolher a quantidade necessária para a narrativa, registrar o total em `target.slide_count` e garantir que a copy tenha exatamente esse número de slides.

Carrosséis são entregues para o feed do Instagram, sempre em 1080 × 1350 pixels (4:5). Formatos de Stories, como 1080 × 1920, não são aceitos como entrega final.

Antes de pesquisar, selecionar ou escrever uma pauta, o agente editorial deve ler `references/editorial/content-rules.md`. Para transformar URL, descoberta, vídeo/post ou ideia em pacote de carrossel, deve seguir `.agents/skills/news-to-carousel/SKILL.md`.

## Estados dos pacotes de conteúdo

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

## Regras globais de qualidade

- Não invente fatos, fontes, resultados ou elementos da marca.
- Não reescreva a copy final de outro agente sem registrar o motivo e sem preservar a intenção.
- Não copie uma referência visual; extraia princípios e crie uma execução original.
- Não apague entregas de outro agente. Prefira uma nova versão ou peça decisão.
- Dados sensíveis, tokens, credenciais e arquivos `.env` nunca entram no repositório.

## Skills

As skills do projeto ficam em `.agents/skills/` e são a fonte viva de instruções operacionais para os agentes. Quando uma skill for atualizada, ela deve ser atualizada no mesmo local, sem criar versões paralelas ou cópias numeradas.

Uma skill só deve ser criada ou promovida para o repositório quando representar um procedimento recorrente, útil e suficientemente claro. Rascunhos de conversa, tentativas pontuais e instruções ainda não validadas permanecem fora da memória persistente.

## Convenção de commits

Use mensagens curtas e rastreáveis:

```text
content(<id>): add carousel copy
design(<id>): add carousel deliverables
chore: update shared workflow
```
