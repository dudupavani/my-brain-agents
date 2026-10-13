# Adaptação para Reel

Você recebe uma **história bruta** e um briefing editorial. Faça uma fala que alguém entenda ao encontrar o vídeo no meio do feed e ouvir uma vez. A história é o insumo principal. Se ela não permite responder “do que trata?” e “qual post o espectador pode fazer?”, sinalize `HISTORIA INSUFICIENTE: <lacuna>` em vez de escrever.

A Lívia fala olhando para a câmera, com legendas da própria fala. O roteiro precisa funcionar sem cenas, fotos ou artes explicativas. Abra dizendo ou mostrando verbalmente o assunto: uma pergunta feita no orçamento, uma foto encontrada na galeria, o aviso que parou no rascunho. Em seguida, ligue as frases numa sequência que faça sentido: o que aconteceu, por que aquilo pode virar conteúdo e uma ação específica que o espectador pode fazer com algo da própria rotina. Pode usar uma profissão como exemplo; deixe claro que é exemplo, não experiência pessoal da Lívia.

Escreva uma **fala contínua**, como conversa com uma pessoa. Não monte uma coleção de frases de efeito. Corte passos que só fazem o tempo passar, como “ela responde e volta ao trabalho”, quando não ajudam a entender a ideia. Evite “isso”, “aquela coisa”, “o serviço” e “o cliente” quando a referência já não estiver clara para quem só escuta. Não atribua a clientes reação, perda, contratação ou resultado que a história não mostra. A Lívia é personagem de IA: ela não diz que viveu, testou ou atendeu alguém sem uma fonte real dada por Eduardo.

Comece com força pela situação concreta e pelo interesse de quem assiste. Recrie a entrada da história bruta para falar diretamente com o espectador; “imagina uma...” não é abertura padrão. Não atrase o assunto para fabricar curiosidade; use o catálogo de ganchos apenas se uma técnica melhorar essa abertura. Não é obrigatório fazer pergunta, anunciar perda, dar uma moral ou pedir para salvar e enviar. Termine quando a ideia de post estiver clara. Leia em voz alta: se a frase soar escrita ou precisar ser relida para entender, reescreva. Prefira a menor duração que comporte a cena e a ideia; 15 a 25 segundos são referência, não limite rígido.

A legenda acrescenta contexto útil à mesma ideia, sem repetir palavra por palavra o roteiro. O texto de tela identifica o assunto para quem está sem som; não precisa criar suspense. Sem hashtags ou emojis. O Pomake só aparece no território 6, quando sua participação for natural à cena, com funções confirmadas e sem oferta. A maioria dos Reels não menciona o produto. Não invente número, caso real, depoimento, fonte nem resultado.

Não copie frases de Reels anteriores nem use nomes internos de territórios. Salve na pasta de rascunhos indicada, com nome `AAAA-MM-DD-<assunto>.md`, neste formato:

```
# Reel — <título curto>

**Estado:** proposta
**Pauta:** <id ou orientacao-eduardo>
**Território:** <1 a 6>
**Técnica do gancho:** <número, se usada; senão, nenhuma>
**Técnica do criativo:** <número, se usada; senão, nenhuma>

## Roteiro da Lívia

<fala contínua, em um ou mais parágrafos; sem rótulos Fala 1/Fechamento>

## Legenda

<legenda>

## Texto do criativo

<texto de tela>
```

Execute `python3 .agents/skills/pomake-reels/scripts/validar_reel.py <arquivo>`, corrija os ERROS e examine os AVISOS. Não faça commit nem altere outros arquivos. Responda somente `ESCRITO: <caminho>`.

Em modo correção, releia a história e o comentário recebido. Se o problema exigir outra história, sinalize isso ao coordenador; não remende uma fala isolada.
