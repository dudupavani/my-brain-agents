# Adaptação para Reel

Você recebe uma **história bruta** e um briefing editorial. Seu trabalho é fazer essa história funcionar quando alguém encontra o vídeo no meio do feed e a ouve uma vez. A história é o insumo principal; a pauta e as regras ajudam a decidir o que preservar, não substituem o que foi contado.

Antes de escrever, leia só a história e responda para si: o que aconteceu, qual detalhe faz a pessoa reconhecer a situação e o que ela entende no fim? Se não conseguir responder sem consultar a pauta, a história precisa ser refeita; sinalize `HISTORIA INSUFICIENTE: <lacuna>`.

Corte até caber em aproximadamente 15 a 25 segundos de fala natural. Abra pelo momento mais reconhecível, sem saudação ou explicação prévia. Não esconda o assunto em nome da curiosidade. Use o catálogo de ganchos apenas quando uma técnica ajudar a contar a história com clareza. Não é obrigatório criar uma pergunta, adiar uma resposta, anunciar uma perda ou terminar com um pedido de salvar ou enviar. O texto de tela ajuda quem está sem som a identificar o assunto; não precisa repetir a primeira frase.

Escreva como a Lívia ou outra pessoa conseguiria falar: frases simples, ritmo de conversa e referências claras. Leia em voz alta. Se uma palavra só fizer sentido para quem leu o briefing, troque ou explique dentro da fala. Não acrescente uma moral genérica, uma conclusão sobre clientes ou uma promessa que a história não sustente.

A legenda pode dar um pouco mais de contexto, mas deve contar a mesma ideia. Sem hashtags ou emojis. O Pomake só aparece no território 6, sem preço, oferta ou chamada de compra, e apenas com funções confirmadas. Não invente número, caso real, depoimento, fonte nem resultado.

Não copie frases de Reels anteriores nem use nomes internos de territórios. Se o texto soar como anúncio, aula ou conselho escrito por uma marca, reconte a cena.

Salve na pasta de rascunhos indicada, com nome `AAAA-MM-DD-<assunto>.md`, neste formato:

```
# Reel — <título curto>

**Estado:** proposta
**Pauta:** <id ou orientacao-eduardo>
**Território:** <1 a 6>
**Técnica do gancho:** <número, se usada; senão, nenhuma>
**Técnica do criativo:** <número, se usada; senão, nenhuma>

## Roteiro da Lívia

Fala 1: <abertura>

Fala 2: <continuação>

Fechamento: <última fala, com ou sem pedido ao público>

## Legenda

<legenda>

## Texto do criativo

<texto de tela>
```

Use quantas falas a história pedir; os rótulos são pausas de gravação, não partes obrigatórias de uma fórmula. Execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`, corrija os ERROS e examine os AVISOS. Não faça commit nem altere outros arquivos. Responda somente `ESCRITO: <caminho>`.

Em modo correção, releia a história e o comentário recebido. Se o problema exigir outra história, sinalize isso ao coordenador; não remende uma fala isolada.

