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
                    ler_reels, secoes)

ESTADOS = {"proposta", "aprovado", "publicado"}
ALVO_PALAVRAS = (30, 95)  # apenas referência; a leitura em voz alta decide a duração
REPETICAO_ERRO = 8      # palavras seguidas iguais a um Reel anterior: erro
REPETICAO_AVISO = 5     # palavras seguidas iguais a um Reel anterior: aviso
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")
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
        m = re.match(r"^## \d\. (.+)$", linha)
        if m:
            nomes.add(m.group(1).strip())
    return {n for n in nomes if len(normalizar(n)) >= 3}


def validar(caminho):
    erros, avisos = [], []
    caminho = Path(caminho).resolve()
    texto = caminho.read_text(encoding="utf-8")

    # Nome do arquivo: só assim o motor reconhece o Reel (exemplos, repetição)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*\.md", caminho.name):
        erros.append("Nome do arquivo fora do padrão AAAA-MM-DD-assunto-em-minusculas-com-hifens.md.")

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
    itens = falas(roteiro)  # compatibilidade com Reels antigos numerados
    fala_limpa = re.sub(r"^(Fala \d+|Fechamento):\s*", "", roteiro, flags=re.M).strip()

    # Duração estimada; o teste de fala prevalece sobre a contagem.
    palavras = len(normalizar(fala_limpa))
    if not palavras:
        erros.append("Roteiro sem fala.")
    elif estado == "proposta" and not ALVO_PALAVRAS[0] <= palavras <= ALVO_PALAVRAS[1]:
        avisos.append(f"Roteiro com {palavras} palavras; confira a duração falando em voz alta.")

    # Legenda
    legenda = sec.get("Legenda", "")
    if re.search(r"(^|\s)#\w", legenda):
        erros.append("Legenda com hashtag.")
    if EMOJI.search(legenda):
        erros.append("Legenda com emoji.")
    abertura = itens.get("Fala 1") or re.split(r"(?<=[.?!])\s", fala_limpa, maxsplit=1)[0]
    fala1 = normalizar(abertura)
    inicio_legenda = normalizar(re.split(r"(?<=[.?!])\s", legenda.strip(), maxsplit=1)[0]) if legenda.strip() else []
    if fala1 and inicio_legenda and (inicio_legenda == fala1 or " ".join(fala1) in " ".join(inicio_legenda)):
        avisos.append("A legenda começa repetindo a abertura. A legenda deve adaptar o argumento, não copiar a fala.")

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

