"""Registra o motivo de uma rejeição de Eduardo em reels/rejeicoes.md.

Uso: python3 rejeitar.py <id-da-pauta|orientacao-eduardo> "<motivo, nas palavras de Eduardo>"

Grava somente a data, a pauta e o motivo. O texto do Reel rejeitado nunca é guardado.
O motor lê este arquivo para não repetir os mesmos erros.
"""
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import REJEICOES, ids_de_pautas  # noqa: E402

CABECALHO = (
    "# Motivos de rejeição de Eduardo\n\n"
    "Só o motivo, nas palavras dele. O texto rejeitado nunca é guardado. "
    "O motor lê este arquivo para não repetir os mesmos erros.\n\n"
)


def registrar(pauta, motivo):
    motivo = " ".join(motivo.split())
    if not motivo:
        sys.exit("ERRO: motivo vazio. Registre somente quando Eduardo tiver dado o motivo.")
    if pauta != "orientacao-eduardo" and pauta not in ids_de_pautas():
        sys.exit(f"ERRO: pauta '{pauta}' não existe em pautas.yaml.")
    if not REJEICOES.exists():
        REJEICOES.write_text(CABECALHO, encoding="utf-8")
    texto = REJEICOES.read_text(encoding="utf-8")
    if not texto.endswith("\n"):
        texto += "\n"
    texto += f"- {time.strftime('%Y-%m-%d')} · {pauta} · {motivo}\n"
    REJEICOES.write_text(texto, encoding="utf-8")
    print(f"OK: motivo registrado para {pauta}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    registrar(sys.argv[1], sys.argv[2])
