"""Valida um arquivo de Reel do Pomake: estrutura e regras mecânicas.

Uso: python3 validar_reel.py <arquivo-do-reel.md>
Sai com código 1 se houver ERRO. AVISO não bloqueia, mas deve ser conferido.

As checagens de repetição comparam o Reel apenas com Reels anteriores a ele.
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import (ESTRATEGIA, SECOES_PACOTE, campo, falas, ids_de_pautas,  # noqa: E402
                    ler_pautas, ler_reels, secoes)

ESTADOS = {"proposta", "aprovado", "publicado", "rejeitado"}
MIN_PALAVRAS = 40
REPETICAO_ERRO = 8      # palavras seguidas iguais a um Reel anterior: erro
REPETICAO_AVISO = 5     # palavras seguidas iguais a um Reel anterior: aviso
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")
PEDIDO = re.compile(r"\b(salv|guard|envi|mand|compartilh|repass|encaminh)\w*", re.I)
TERMOS_COMERCIAIS = ["preço", "r$", "compre", "assine", "assinatura", "teste grátis",
                     "link na bio", "cupom", "desconto"]


def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", texto)


def texto_do_pacote(sec):
    roteiro = re.sub(r"^(Fala \d+|Fechamento):", "", sec.get("Roteiro da Lívia", ""), flags=re.M)
    return "\n".join([roteiro, sec.get("Legenda", ""), sec.get("Texto do criativo", "")])


def maior_trecho_comum(a, b):
    """Maior sequência de palavras consecutivas presente nas duas listas."""
    melhor, trecho = 0, []
    anterior = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        atual = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                atual[j] = anterior[j - 1] + 1
                if atual[j] > melhor:
                    melhor, trecho = atual[j], a[i - atual[j]:i]
        anterior = atual
    return melhor, " ".join(trecho)


def nomes_internos():
    nomes = set()
    for linha in (ESTRATEGIA / "territories.md").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^## \d\. \[(.+?)\]", linha)
        if m:
            nomes.add(m.group(1))
    for p in ler_pautas():
        nomes.add(re.sub(r"^\d+ — ", "", p.get("serie", "")))
    return {n for n in nomes if len(normalizar(n)) >= 3}


def validar(caminho):
    erros, avisos = [], []
    caminho = Path(caminho).resolve()
    texto = caminho.read_text(encoding="utf-8")

    # Estrutura
    estado = campo(texto, "Estado")
    estado = estado.split()[0].rstrip(".").lower() if estado else None
    if estado not in ESTADOS:
        erros.append(f"Estado ausente ou inválido. Use um de: {', '.join(sorted(ESTADOS))}.")

    pauta = campo(texto, "Pauta")
    if pauta is None:
        erros.append("Campo Pauta ausente.")
    elif pauta != "orientacao-eduardo" and pauta not in ids_de_pautas():
        erros.append(f"Pauta '{pauta}' não existe em pautas.yaml.")

    territorio = campo(texto, "Território")
    if territorio is None or not re.fullmatch(r"[1-6]", territorio):
        erros.append("Campo Território ausente ou fora de 1 a 6.")
    for nome in ("Técnica do gancho", "Técnica do criativo"):
        if campo(texto, nome) is None:
            erros.append(f"Campo {nome} ausente.")

    sec = secoes(texto)
    for nome in SECOES_PACOTE:
        if not sec.get(nome):
            erros.append(f"Seção '## {nome}' ausente ou vazia.")
    roteiro = sec.get("Roteiro da Lívia", "")
    itens = falas(roteiro)
    if not itens.get("Fala 1"):
        erros.append("Roteiro sem 'Fala 1:' preenchida (gancho).")
    if not itens.get("Fechamento"):
        erros.append("Roteiro sem 'Fechamento:' preenchido.")
    if estado == "rejeitado" and not sec.get("Avaliação de Eduardo"):
        erros.append("Reel rejeitado sem a seção '## Avaliação de Eduardo'.")

    # Duração
    palavras = len(normalizar(re.sub(r"^(Fala \d+|Fechamento):", "", roteiro, flags=re.M)))
    if palavras < MIN_PALAVRAS:
        erros.append(f"Roteiro com {palavras} palavras; o mínimo é {MIN_PALAVRAS} (Reel de no mínimo 15 segundos).")

    # Legenda
    legenda = sec.get("Legenda", "")
    if re.search(r"(^|\s)#\w", legenda):
        erros.append("Legenda com hashtag.")
    if EMOJI.search(legenda):
        erros.append("Legenda com emoji.")
    fala1 = normalizar(itens.get("Fala 1", ""))
    inicio_legenda = normalizar(re.split(r"(?<=[.?!])\s", legenda.strip(), maxsplit=1)[0]) if legenda.strip() else []
    if fala1 and inicio_legenda and (inicio_legenda == fala1 or " ".join(fala1) in " ".join(inicio_legenda)):
        avisos.append("A legenda começa repetindo a Fala 1. A legenda deve adaptar o argumento, não copiar a fala.")

    # Pedido final
    if itens.get("Fechamento") and not PEDIDO.search(itens["Fechamento"]):
        erros.append("Fechamento sem pedido ao público (salvar ou enviar a alguém).")
    ultimo_paragrafo = [p for p in legenda.strip().split("\n") if p.strip()][-1:] if legenda.strip() else []
    if ultimo_paragrafo and not PEDIDO.search(ultimo_paragrafo[0]):
        erros.append("A legenda não termina com pedido ao público (salvar ou enviar a alguém).")

    # Pomake e tom comercial
    pacote = texto_do_pacote(sec)
    pacote_min = pacote.lower()
    if territorio and territorio != "6" and "pomake" in pacote_min:
        erros.append("O Pomake é citado fora do território 6.")
    if territorio == "6":
        for termo in TERMOS_COMERCIAIS:
            if termo in pacote_min:
                avisos.append(f"Território 6 com termo comercial '{termo}'. Confirme que não é chamada de compra.")

    # Números exigem evidência
    if re.search(r"\d", pacote):
        avisos.append("Há números no texto. Confirme que não são dado, resultado ou estatística inventados.")

    # Nomes internos
    pacote_norm = " ".join(normalizar(pacote))
    for nome in sorted(nomes_internos()):
        if " ".join(normalizar(nome)) in pacote_norm:
            avisos.append(f"O texto contém o nome interno '{nome}'. Nomes de territórios e séries não devem virar fala.")

    # Repetição em relação a Reels anteriores
    reels = ler_reels()
    posicao = next((i for i, r in enumerate(reels) if r["caminho"] == caminho), len(reels))
    palavras_pacote = normalizar(pacote)
    for anterior in reels[:posicao]:
        tamanho, trecho = maior_trecho_comum(palavras_pacote, normalizar(texto_do_pacote(anterior["secoes"])))
        nome = anterior["caminho"].name
        if tamanho >= REPETICAO_ERRO:
            erros.append(f"Repete {tamanho} palavras seguidas de {nome}: \"{trecho}\".")
        elif tamanho >= REPETICAO_AVISO:
            avisos.append(f"Repete {tamanho} palavras seguidas de {nome}: \"{trecho}\". Confira se é expressão comum.")

    return erros, avisos


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    erros, avisos = validar(sys.argv[1])
    for a in avisos:
        print(f"AVISO: {a}")
    for e in erros:
        print(f"ERRO: {e}")
    if erros:
        sys.exit(1)
    print("OK")
