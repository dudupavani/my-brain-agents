"""Funções compartilhadas pelos scripts da skill pomake-reels."""
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
PAUTAS = RAIZ / "domains/products/pomake/editorial-strategy/pautas.yaml"
REELS = RAIZ / "domains/products/pomake/reels"


def ids_de_pautas():
    texto = PAUTAS.read_text(encoding="utf-8")
    return set(re.findall(r"^  - id: (T\d-P\d{2})$", texto, re.M))
