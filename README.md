# Instagram Creator

Este repositório é a memória compartilhada entre o Hermes, o Codex e você. Ele guarda o conteúdo aprovado, as referências que definem a marca e os carrosséis finais — não apenas conversas soltas.

## Fluxo inicial

```text
Você conversa com Hermes
        ↓
Hermes cria um pacote em content/items/<id>
        ↓  status: ready_for_design
Codex cria o carrossel no mesmo pacote
        ↓  status: in_review
Você revisa, aprova e publica
```

Cada conteúdo vive em uma única pasta. O estado em `metadata.yaml` informa com clareza qual é o próximo trabalho, sem mover arquivos de lugar ou depender da memória de uma conversa.

## Começo de uso

1. Preencha [references/brand/brand.md](references/brand/brand.md) com sua identidade e seus limites editoriais.
2. Coloque exatamente três imagens JPEG de referência em [`.agents/skills/instagram-carousel/assets/templates/`](.agents/skills/instagram-carousel/assets/templates/), com os nomes indicados no arquivo dessa pasta.
3. Dê ao Hermes as instruções de [agents/hermes/HANDOFF.md](agents/hermes/HANDOFF.md).
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

Leia [mapa.md](mapa.md) para navegar pela estrutura e [AGENTS.md](AGENTS.md) para o protocolo que os agentes seguem.
