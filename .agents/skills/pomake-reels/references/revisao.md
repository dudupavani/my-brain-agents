# Checklist de revisão de Reel do Pomake

Você não participou da criação. Avalie somente com este checklist e o material do briefing do revisor. Regras mecânicas (estrutura, duração, hashtags, emojis, Pomake fora do território 6, frases repetidas, presença do pedido final) já são conferidas pelo validador; não as avalie de novo.

Primeiro, execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`. Se houver ERRO, reprove citando o erro. Para cada AVISO, decida se é um problema real e, se for, registre-o como falha no item correspondente.

Não altere nenhum arquivo. Cada item é **passa** ou **falha**; não existe meio-termo.

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

## Formato do resultado

Responda somente com este bloco JSON:

```json
{
  "resultado": "aprovado",
  "falhas": []
}
```

Em caso de reprovação:

```json
{
  "resultado": "reprovado",
  "falhas": [
    {"item": 3, "problema": "<o que falhou, em uma frase>", "correcao": "<o que o redator deve fazer, em uma frase>"}
  ]
}
```
