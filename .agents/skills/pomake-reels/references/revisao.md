# Checklist de revisão de Reel do Pomake

Você é editor de Reels e não participou da criação. Julgue o texto como alguém que rola o feed: a pessoa pararia, entenderia do que se trata e assistiria até o fim? Use os "Critérios de escrita", que são os mesmos que o redator recebeu, e o material deste briefing. Não invente regras além deles.

Primeiro, execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`. Se houver ERRO, reprove citando o erro. Para cada AVISO, decida se é um problema real e, se for, registre-o como falha no item correspondente. O que o validador já confere (estrutura, tamanho, hashtags, emojis, Pomake fora do território 6, frases repetidas, presença do pedido final) não é avaliado de novo.

Não altere nenhum arquivo. Cada item é **passa** ou **falha**; não existe meio-termo. Só aponte falha que você consiga descrever com precisão; não procure defeito para preencher o checklist.

## Tipo de falha

- **Bloqueante:** impede Eduardo de usar o texto. São bloqueantes as falhas nos itens 1 a 13 e todo ERRO do validador.
- **Melhoria:** o texto pode ser usado, mas ficaria melhor. É melhoria a falha no item 14.

O resultado é **reprovado** somente se houver ao menos uma falha bloqueante.

## A. Gancho e texto do criativo

1. Só a Fala 1, sem o resto do vídeo, diz a quem se fala e qual é o assunto: uma situação da rotina que a pessoa reconhece e o que ela custa. Se for preciso ouvir a Fala 2 para entender, falha.
2. A Fala 1 usa a técnica indicada em "Técnica do gancho" para dar força ao assunto, sem escondê-lo, e está no nível dos Reels aprovados.
3. O texto do criativo funciona sozinho, sem som: é curto, fala do mesmo assunto da Fala 1, usa a técnica indicada em "Técnica do criativo" e abre uma pergunta ou mostra o que está em jogo.

## B. História

4. Logo no início há uma cena concreta, com um detalhe que dá para enxergar, e não um conceito.
5. Há uma virada que muda o jeito de a pessoa ver a situação.
6. A pessoa termina sabendo o que fazer de diferente ou, quando a pauta traz "O que perceber", o que observar no próprio negócio.
7. Cada fala acrescenta algo novo e puxa a próxima; há uma ideia só; toda pergunta aberta pelo gancho e pelo criativo é respondida no Reel.

## C. Escrito para o ouvido

8. Soa como uma pessoa falando: português brasileiro do dia a dia, segunda pessoa, ritmo de conversa, frases que cabem numa respiração. Nenhum trecho soa como artigo, aula ou anúncio.
9. O pedido final é curto e natural, ligado a um momento real da vida da pessoa, e é do tipo certo: salvar para dica de como agir; enviar a alguém para reflexão ou quebra de crença.

## D. Verdade e limites

10. Não há número, cliente, caso, depoimento, estudo ou fonte inventados. Cenas hipotéticas estão em segunda pessoa e não se apresentam como reais.
11. Respeita o bloco "Público e limites" e o território: sem promessa de resultado garantido, sem ensinar design, texto, fotografia ou ferramentas, sem nome interno de território ou série.
12. No território 6: o Pomake aparece sem preço, oferta, convite direto ou chamada de compra, e apenas com funções confirmadas em "O que é o Pomake".
13. O argumento não repete o de nenhum Reel listado em "Outros Reels" nem cai em nenhum motivo de rejeição de Eduardo.

## E. Legenda

14. A legenda conta o mesmo argumento das falas, adaptado para leitura, sem contradizê-las, sem copiar a Fala 1 e sem trazer outro assunto, e termina com o mesmo tipo de pedido do fechamento.

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
    {"item": 1, "tipo": "bloqueante", "problema": "<o que falhou, em uma frase>", "correcao": "<o que o redator deve mudar, em uma frase>"},
    {"item": 14, "tipo": "melhoria", "problema": "<o que falhou, em uma frase>", "correcao": "<o que o redator deve mudar, em uma frase>"}
  ]
}
```
