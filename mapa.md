# Mapa da memória global

O repositório é organizado por domínio de memória, não por conversa. Os agentes são consumidores e mantenedores de áreas específicas; suas responsabilidades e caminhos estão em `architecture/registry.yaml`.

| Local | Conteúdo | Quem escreve |
| --- | --- | --- |
| `architecture/` | Registro de agentes, domínios e regras de roteamento | Você e Codex |
| `shared/` | Contextos e decisões que podem ser usados por mais de um agente | Você e agentes autorizados |
| `domains/personal/` | Materiais pessoais que não pertencem a um domínio especializado | Agente pessoal |
| `domains/products/` | Materiais, decisões e artefatos de produtos | Agente de produtos |
| `content/items/<id>/` | Um conteúdo completo de Instagram, da entrega do Hermes ao carrossel final | Hermes e Codex, em etapas diferentes |
| `content/templates/` | Modelos obrigatórios para novos pacotes | Você mantém; agentes só copiam |
| `references/brand/` | Contexto da marca: posicionamento, voz e restrições | Você |
| `references/editorial/` | Sistema editorial amplo e regras específicas para pautas, fatos, fontes e mídia | Você e agentes |
| `.agents/skills/instagram-carousel/assets/templates/` | As três imagens JPEG que definem a referência visual dos carrosséis | Você |
| `agents/` | Contratos e instruções específicas dos perfis de agente | Você e agentes |
| `agents/hermes/` | Contrato editorial atual do perfil Instagram Creator | Você e Hermes |
| `.agents/skills/instagram-carousel/` | Skill de produção visual do Codex | Codex |
| `.agents/skills/news-to-carousel/` | Skill compartilhada para transformar pautas em pacote pronto para design | Você e agentes |
| `.agents/skills/` | Skills vivas, atualizadas no mesmo local quando evoluem | Você e agentes |
| `AGENTS.md` | Protocolo global, escopos e regras de sincronização | Você e Codex |

## Anatomia de um pacote de conteúdo

```text
content/items/<id>/
├── metadata.yaml       # Identidade, estado e responsável atual
├── brief.md            # Contexto, objetivo e fontes
├── carousel.md         # Copy final, organizada por slide
├── media.md             # Opcional: mídia com origem, papel e slides indicados
└── deliverables/       # Criado pelo Codex
    ├── slide-01.png
    ├── slide-02.png
    ├── ...
    ├── caption.md
    └── design-notes.md
```

`metadata.yaml` é a fonte de verdade do estado. O histórico detalhado permanece no Git; não crie registros paralelos de atividade.

## Regra de expansão

Para adicionar um novo agente ou domínio, primeiro registre-o em `architecture/registry.yaml`, depois crie seu contrato e seu espaço de memória. Não crie pastas genéricas antes de existir uma responsabilidade clara para elas.
