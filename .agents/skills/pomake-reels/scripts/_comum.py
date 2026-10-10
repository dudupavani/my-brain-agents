"""Funções compartilhadas pelos scripts da skill pomake-reels."""
import re
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
POMAKE = RAIZ / "domains/products/pomake"
ESTRATEGIA = POMAKE / "editorial-strategy"
PAUTAS = ESTRATEGIA / "pautas.yaml"
REELS = POMAKE / "reels"
SECOES_PACOTE = ["Roteiro da Lívia", "Legenda", "Texto do criativo"]


def ids_de_pautas():
    texto = PAUTAS.read_text(encoding="utf-8")
    return set(re.findall(r"^  - id: (T\d-P\d{2})$", texto, re.M))


def ler_pautas():
    """Lê pautas.yaml sem dependências externas. Retorna uma lista de dicionários."""
    pautas, atual = [], None
    for linha in PAUTAS.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^  - id: (\S+)$", linha)
        if m:
            atual = {"id": m.group(1)}
            pautas.append(atual)
            continue
        m = re.match(r"^    (\w+): (.*)$", linha)
        if atual is not None and m:
            chave, valor = m.group(1), m.group(2).strip()
            if chave == "reels":
                valor = re.findall(r"[^\[\],\s]+", valor)
            else:
                valor = valor.strip('"')
            atual[chave] = valor
    return pautas


def campo(texto, nome):
    m = re.search(rf"^\*\*{re.escape(nome)}:\*\*\s*(.+)$", texto, re.M)
    return m.group(1).strip() if m else None


def secoes(texto, nivel="## "):
    """Divide um markdown por títulos do nível indicado. Retorna {título: corpo}."""
    partes = re.split(rf"^{re.escape(nivel)}", texto, flags=re.M)
    resultado = {}
    for parte in partes[1:]:
        titulo, _, corpo = parte.partition("\n")
        resultado[titulo.strip()] = corpo.strip()
    return resultado


def falas(roteiro):
    """Retorna {rótulo: texto} das falas de um roteiro (Fala 1, Fala 2..., Fechamento)."""
    itens = {}
    for m in re.finditer(r"^(Fala \d+|Fechamento):\s*(.*?)(?=^\s*(?:Fala \d+|Fechamento):|\Z)",
                         roteiro, re.M | re.S):
        itens[m.group(1)] = " ".join(m.group(2).split())
    return itens


def _momento_git(caminho):
    try:
        saida = subprocess.run(
            ["git", "-C", str(RAIZ), "log", "--diff-filter=A", "--format=%ct", "--", str(caminho)],
            capture_output=True, text=True, timeout=20).stdout.split()
        return int(saida[-1]) if saida else None
    except Exception:
        return None


def ler_reels():
    """Lê todos os Reels, do mais antigo para o mais recente.

    Ordem: data no nome do arquivo; em empate, momento em que entrou no Git;
    arquivos ainda fora do Git contam como os mais recentes.
    """
    reels = []
    for caminho in REELS.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*.md"):
        texto = caminho.read_text(encoding="utf-8")
        sec = secoes(texto)
        momento = _momento_git(caminho)
        reels.append({
            "caminho": caminho,
            "relativo": caminho.relative_to(RAIZ).as_posix(),
            "data": caminho.name[:10],
            "momento": momento if momento is not None else float("inf"),
            "texto": texto,
            "estado": (campo(texto, "Estado") or "").split()[0].rstrip(".").lower() if campo(texto, "Estado") else "",
            "pauta": campo(texto, "Pauta"),
            "territorio": campo(texto, "Território"),
            "secoes": sec,
            "falas": falas(sec.get("Roteiro da Lívia", "")),
        })
    reels.sort(key=lambda r: (r["data"], r["momento"]))
    return reels
