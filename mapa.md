# Mapa da memória compartilhada

| Local | Conteúdo | Quem escreve |
| --- | --- | --- |
| `content/items/<id>/` | Um conteúdo completo, da entrega do Hermes ao carrossel final | Hermes e Codex, em etapas diferentes |
| `content/templates/` | Modelos obrigatórios para novos pacotes | Você mantém; agentes só copiam |
| `references/brand/` | Contexto da marca: posicionamento, voz e restrições | Você |
| `references/editorial/` | Sistema editorial: decisões, fontes, notícias e critérios de escrita | Você e Hermes |
| `.agents/skills/instagram-carousel/assets/templates/` | As três imagens JPEG que definem a referência visual dos carrosséis | Você |
| `agents/hermes/` | Instruções de entrega e decisão para o Hermes | Você e Hermes |
| `.agents/skills/instagram-carousel/` | Skill de produção visual do Codex | Codex |
| `AGENTS.md` | Protocolo de colaboração, estados e regras de sincronização | Você e Codex |

## Anatomia de um pacote de conteúdo

```text
content/items/<id>/
├── metadata.yaml       # Identidade, estado e responsável atual
├── brief.md            # Contexto, objetivo e fontes
├── carousel.md         # Copy final, organizada por slide
└── deliverables/       # Criado pelo Codex
    ├── slide-01.png
    ├── slide-02.png
    ├── ...
    ├── caption.md
    └── design-notes.md
```

`metadata.yaml` é a fonte de verdade do estado. O histórico detalhado permanece no Git; não crie registros paralelos de atividade.
