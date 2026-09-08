# Contratos dos agentes

Esta pasta descreve os perfis de agente que operam sobre a memória global. Cada perfil no Hermes é independente; os arquivos aqui não criam um orquestrador.

Um contrato de agente deve registrar, de forma curta:

- finalidade e limites do perfil;
- domínio ou domínios que ele pode manter;
- arquivos que deve ler antes de agir;
- caminhos que pode criar ou alterar;
- formato da entrega para os demais agentes.

O agente não deve guardar materiais nesta pasta. Use os caminhos de memória registrados em `architecture/registry.yaml`.

Os contratos atuais estão em:

- `agents/hermes/`: contrato editorial do perfil Instagram Creator;
- `agents/products/`: contrato inicial do agente de produtos.
