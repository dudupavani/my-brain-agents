# Memória Global dos Agentes

Este repositório é a memória persistente e a fonte de verdade dos agentes do Eduardo. Ele centraliza materiais, decisões, referências, instruções, skills e entregas em um único lugar, com histórico rastreável no GitHub.

Os agentes são perfis independentes no Hermes. Cada perfil tem um escopo e um domínio próprios, mas todos consultam e mantêm esta mesma memória. O repositório não possui um agente orquestrador: a arquitetura e as regras de roteamento cumprem esse papel.

Consulte [mapa.md](mapa.md) para navegar pela estrutura, [architecture/registry.yaml](architecture/registry.yaml) para descobrir os agentes e domínios e [AGENTS.md](AGENTS.md) para o protocolo obrigatório.

## Princípios

- Centralizar a memória em um único repositório.
- Separar agentes, domínios de conhecimento e skills.
- Salvar cada informação no domínio ao qual ela pertence.
- Manter as skills como fonte viva, atualizando-as no mesmo local.
- Evoluir a arquitetura gradualmente, sem criar estruturas que ainda não tenham uso.

## Agentes atuais

| Perfil no Hermes | Responsabilidade atual | Memória principal |
| --- | --- | --- |
| Instagram Creator | Conteúdo e produção editorial para Instagram | `content/` e `references/` |
| Agente de produtos | Materiais, decisões e trabalho relacionados a produtos | `domains/products/` |

O agente pessoal, atualmente chamado Instagram Creator, pode usar `domains/personal/` para materiais pessoais que não pertencem ao domínio editorial.

## Fluxo atual do Instagram

```text
Você conversa com o Instagram Creator
        ↓
Quando pede para preparar para o Codex, o agente cria um pacote em content/items/<id>
        ↓  status: ready_for_design
Codex cria o carrossel no mesmo pacote
        ↓  status: in_review
Você revisa, aprova e publica
```

Cada conteúdo vive em uma única pasta. O estado em `metadata.yaml` informa com clareza qual é o próximo trabalho, sem mover arquivos de lugar ou depender da memória de uma conversa.

## Começo de uso

1. Mantenha [references/brand/brand.md](references/brand/brand.md) e o [sistema editorial](references/editorial/content-system.md) como fonte de verdade da identidade, voz, limites e decisões de conteúdo.
2. Coloque exatamente três imagens JPEG de referência em [`.agents/skills/instagram-carousel/assets/templates/`](.agents/skills/instagram-carousel/assets/templates/), com os nomes indicados no arquivo dessa pasta.
3. Hermes deve seguir [agents/hermes/CONTENT.md](agents/hermes/CONTENT.md) em todo trabalho editorial e [agents/hermes/HANDOFF.md](agents/hermes/HANDOFF.md) quando preparar um item para o Codex.
4. Quando um pacote estiver com `status: ready_for_design`, peça ao Codex para criar o carrossel ou mencione `$instagram-carousel`.

## Conectar ao GitHub

O repositório local já está preparado. Para habilitar a sincronização entre ambientes, crie um repositório privado vazio no seu GitHub e conecte-o a este diretório:

```bash
git remote add origin URL_DO_SEU_REPOSITORIO
git branch -M main
git add .
git commit -m "chore: initialize shared content brain"
git push -u origin main
```

Depois disso, cada agente deve atualizar a cópia local antes de iniciar um item e enviar somente o trabalho concluído. GitHub é a memória compartilhada; a sincronização acontece por `pull` e `push`, não de modo instantâneo.
