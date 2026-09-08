# Eduardo Agent Brain

Base de conhecimento compartilhada e versionada para os agentes do Eduardo. O repositório permite que trabalhos produzidos no Hermes continuem acessíveis ao Codex, Claude Code e outros runtimes sem depender da memória de uma conversa ou de um aplicativo específico.

## O que pertence a cada camada

```text
Profiles do Hermes
  identidade, personalidade, memória privada, sessões e capacidades locais
                         ↓
Este repositório GitHub
  conhecimento, decisões, pesquisas, entregas e skills compartilháveis
                         ↓
ClickUp e outros sistemas
  tarefas, acompanhamento, aprovações e publicação
```

O GitHub é a fonte canônica do conteúdo das entregas. ClickUp pode guardar a tarefa, o responsável, o prazo e um link para o material no GitHub.

## Agentes ativos na v1

| Agente lógico | Função | Cérebro no repositório |
| --- | --- | --- |
| `products` | Construir e pensar produtos e softwares; pesquisar e fazer benchmarks | `domains/products/`, `shared/`, skills relevantes |
| `personal-content` | Criar e manter o conteúdo pessoal do Eduardo | `content/`, `references/`, `shared/`, skills relevantes |

Os nomes reais dos profiles são configurados no Hermes. Codex, Claude ou outro modelo podem ser usados por qualquer profile; eles não viram agentes diferentes por causa disso.

## Como navegar

- [mapa.md](mapa.md): onde encontrar e salvar cada coisa.
- [architecture/system.md](architecture/system.md): desenho completo da arquitetura.
- [architecture/decisions.md](architecture/decisions.md): o que já foi decidido, o que é provisório e o que está adiado.
- [architecture/registry.yaml](architecture/registry.yaml): contratos e permissões em formato estruturado.
- [AGENTS.md](AGENTS.md): contexto obrigatório para qualquer agente ou runtime.

## Princípio de evolução

A v1 usa um único repositório porque os dois agentes pertencem ao Eduardo e ainda não existe uma fronteira real de permissão entre eles. Um domínio só deve virar outro repositório quando houver uma separação concreta de empresa, sócios, equipe, confidencialidade, credenciais ou ciclo de vida.

Arquitetura futura, masterbrain, memória semântica compartilhada, sincronização automática com ClickUp e publicação automática são possibilidades, não funcionalidades presumidas nesta versão.
