"""Valida a estrutura de um arquivo de Reel do Pomake.

Uso: python3 validar_reel.py <arquivo-do-reel.md>
Sai com código 1 se houver erro. Avisos não bloqueiam.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import ids_de_pautas  # noqa: E402

ESTADOS = {"proposta", "aprovado", "publicado", "rejeitado"}
SECOES = ["Roteiro da Lívia", "Legenda", "Texto do criativo"]
TERMOS_COMERCIAIS = ["preço", "r$", "compre", "assine", "assinatura", "teste grátis",
                     "link na bio", "cupom", "desconto"]


def campo(texto, nome):
    m = re.search(rf"^\*\*{re.escape(nome)}:\*\*\s*(.+)$", texto, re.M)
    return m.group(1).strip() if m else None


def secoes(texto):
    partes = re.split(r"^## ", texto, flags=re.M)
    resultado = {}
    for parte in partes[1:]:
        titulo, _, corpo = parte.partition("\n")
        resultado[titulo.strip()] = corpo.strip()
    return resultado


def validar(caminho):
    erros, avisos = [], []
    texto = Path(caminho).read_text(encoding="utf-8")

    estado = campo(texto, "Estado")
    if estado is None or estado.split()[0].rstrip(".").lower() not in ESTADOS:
        erros.append(f"Estado ausente ou inválido. Use um de: {', '.join(sorted(ESTADOS))}.")
    else:
        estado = estado.split()[0].rstrip(".").lower()

    pauta = campo(texto, "Pauta")
    if pauta is None:
        erros.append("Campo Pauta ausente.")
    elif pauta != "orientacao-eduardo" and pauta not in ids_de_pautas():
        erros.append(f"Pauta '{pauta}' não existe em pautas.yaml.")

    territorio = campo(texto, "Território")
    if territorio is None or not re.fullmatch(r"[1-6]", territorio):
        erros.append("Campo Território ausente ou fora de 1 a 6.")

    if campo(texto, "Técnica do gancho") is None:
        erros.append("Campo Técnica do gancho ausente.")
    if campo(texto, "Técnica do criativo") is None:
        erros.append("Campo Técnica do criativo ausente.")

    sec = secoes(texto)
    for nome in SECOES:
        if not sec.get(nome):
            erros.append(f"Seção '## {nome}' ausente ou vazia.")

    roteiro = sec.get("Roteiro da Lívia", "")
    if not re.search(r"^Fala 1:\s*\S", roteiro, re.M):
        erros.append("Roteiro sem 'Fala 1:' preenchida (gancho).")
    if not re.search(r"^Fechamento:\s*\S", roteiro, re.M):
        erros.append("Roteiro sem 'Fechamento:' preenchido.")

    pacote = "\n".join(sec.get(n, "") for n in SECOES).lower()
    if territorio and territorio != "6" and "pomake" in pacote:
        erros.append("O Pomake é citado fora do território 6.")
    if territorio == "6":
        for termo in TERMOS_COMERCIAIS:
            if termo in pacote:
                avisos.append(f"Território 6 com termo comercial '{termo}'. Confirme que não é chamada de compra.")

    if estado == "rejeitado" and not sec.get("Avaliação de Eduardo"):
        erros.append("Reel rejeitado sem a seção '## Avaliação de Eduardo'.")

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
