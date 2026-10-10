# Checklist de revisão de Reel do Pomake

Você não participou da criação. Avalie somente com este checklist e o material do briefing do revisor. Regras mecânicas (estrutura, duração, hashtags, emojis, Pomake fora do território 6, frases repetidas, presença do pedido final) já são conferidas pelo validador; não as avalie de novo.

Primeiro, execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`. Se houver ERRO, reprove citando o erro. Para cada AVISO, decida se é um problema real e, se for, registre-o como falha no item correspondente.

Não altere nenhum arquivo. Cada item é **passa** ou **falha**; não existe meio-termo.

## Tipo de falha

- **Bloqueante:** impede Eduardo de usar o texto. São bloqueantes as falhas nos itens 1 a 6, 11, 12, 13, 15, 16, 17, 18 e 19, e todo ERRO do validador.
- **Melhoria:** o texto pode ser usado, mas ficaria melhor. São melhorias as falhas nos itens 7, 8, 9, 10 e 14.

O resultado é **reprovado** somente se houver ao menos uma falha bloqueante. Só aponte falha que você consiga descrever com precisão; não procure defeito para preencher o checklist.

## A. Gancho e criativo

1. A Fala 1 usa a técnica indicada em "Técnica do gancho", prende a atenção nos primeiros 3 segundos e é compreensível para quem nunca viu o perfil.
2. O gancho é forte sem ser agressivo e está no mesmo nível de força da Fala 1 dos Reels aprovados.
3. O texto do criativo usa a técnica indicada em "Técnica do criativo", abre uma pergunta em quem lê ou mostra o que está em jogo, e não é uma afirmação que se encerra sozinha.
4. O texto do criativo é curto, legível em uma leitura rápida, tem o mesmo argumento da Fala 1 e está no mesmo nível de força do criativo dos Reels aprovados.

## B. Promessa cumprida

5. Toda pergunta ou lacuna aberta pelo gancho e pelo criativo é respondida dentro do próprio Reel.
6. O fechamento entrega uma orientação concreta, que a pessoa consegue aplicar no próprio negócio.
7. Há uma única ideia; todas as falas servem ao mesmo argumento.
8. O pedido final corresponde ao tipo de conteúdo: salvar para dica de como agir; enviar a quem vai gostar de saber para outro tipo. A legenda termina com o mesmo tipo de pedido.

## C. Voz

9. Português brasileiro, segunda pessoa, palavras comuns, tom de conversa.
10. Cada fala soa natural dita em voz alta; nenhuma parece texto escrito para leitura.

## D. Verdade e limites

11. Não há número, cliente, caso, depoimento, estudo ou fonte inventados. Cenas hipotéticas estão em segunda pessoa e não se apresentam como reais. Especificidade, prova social e autoridade só aparecem com evidência verdadeira.
12. Não há promessa de resultado garantido, ensino de ferramentas, nome interno de território ou série, nem desrespeito às fronteiras do território e aos limites da fundação.
13. No território 6: o Pomake aparece sem preço, oferta, convite direto ou chamada de compra, e apenas com funções confirmadas em "O que é o Pomake".

## E. Legenda e leitura fria

14. A legenda tem o mesmo argumento das falas, adaptado para leitura, sem contradizê-las, sem copiar a Fala 1 e sem introduzir outro assunto.
15. Lido sem nenhum contexto, fica claro quem está na situação, o que acontece, por que importa e o que a pessoa ganha.

## F. Comparação

16. O argumento não repete o de nenhum Reel listado em "Outros Reels" e não repete nenhum motivo de rejeição de Eduardo.

## G. Cena concreta

17. Lido sem nenhum contexto, dá para saber de que situação concreta o Reel fala até a Fala 2: uma cena específica do dia a dia, com um detalhe que a pessoa consiga enxergar. Se o texto usa só termos genéricos ("etapa", "processo", "parte do trabalho", "conteúdo") sem exemplo concreto, falha.

## H. O que está em jogo e pedido final

18. A Fala 1 ou a Fala 2 diz claramente o que a pessoa perde ou arrisca. Suavizações que tiram a força ("pode parecer", "talvez") no lugar da consequência fazem o item falhar.
19. O motivo do pedido final (no fechamento e na legenda) é um momento real e reconhecível, faz sentido dito em voz alta e não repete a orientação da fala anterior. Motivos abstratos como "pra conferir essa pergunta", "pra fazer essa conferência" ou "pra consultar depois" fazem o item falhar.

## Formato do resultado

Responda somente com este bloco JSON:

```json
{
  "resultado": "aprovado",
  "falhas": []
}
```

Com falhas (aprovado só com melhorias, ou reprovado com bloqueantes):

```json
{
  "resultado": "reprovado",
  "falhas": [
    {"item": 3, "tipo": "bloqueante", "problema": "<o que falhou, em uma frase>", "correcao": "<o que o redator deve fazer, em uma frase>"},
    {"item": 9, "tipo": "melhoria", "problema": "<o que falhou, em uma frase>", "correcao": "<o que o redator deve fazer, em uma frase>"}
  ]
}
```
