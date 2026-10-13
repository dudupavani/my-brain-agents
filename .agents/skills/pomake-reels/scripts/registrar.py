"""Liga um Reel aprovado a uma pauta reutilizável ou muda seu estado editorial.

Uso: python3 registrar.py <id-da-pauta> --reel <arquivo-do-reel.md>
     python3 registrar.py <id-da-pauta> ativa|arquivada
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import PAUTAS, RAIZ  # noqa: E402

STATUS = {"ativa", "arquivada"}


def registrar(pauta_id, status=None, reel=None):
    if status is not None and status not in STATUS:
        sys.exit(f"ERRO: status inválido. Use um de: {', '.join(sorted(STATUS))}.")
    if status is None and reel is None:
        sys.exit("ERRO: informe um estado ou use --reel <arquivo>.")
    linhas = PAUTAS.read_text(encoding="utf-8").split("\n")
    try:
        inicio = linhas.index(f"  - id: {pauta_id}")
    except ValueError:
        sys.exit(f"ERRO: pauta '{pauta_id}' não existe em pautas.yaml.")
    fim = inicio + 1
    while fim < len(linhas) and not linhas[fim].startswith("  - id: ") and linhas[fim].strip():
        fim += 1
    for i in range(inicio, fim):
        if status is not None and linhas[i].startswith("    status: "):
            linhas[i] = f"    status: {status}"
        if reel and linhas[i].startswith("    reels: "):
            caminho = Path(reel).resolve()
            if not caminho.exists():
                sys.exit(f"ERRO: arquivo do Reel não encontrado: {reel}")
            try:
                relativo = caminho.relative_to(RAIZ).as_posix()
            except ValueError:
                sys.exit("ERRO: o Reel precisa estar dentro do repositório.")
            atuais = re.findall(r"[^\[\],\s]+", linhas[i][len("    reels: "):])
            if relativo not in atuais:
                atuais.append(relativo)
            linhas[i] = "    reels: [" + ", ".join(atuais) + "]"
    PAUTAS.write_text("\n".join(linhas), encoding="utf-8")
    print(f"OK: {pauta_id}" + (f" → {status}" if status else "") + (f" (Reel: {reel})" if reel else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    reel = None
    if "--reel" in args:
        i = args.index("--reel")
        reel = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
    if len(args) not in (1, 2):
        print(__doc__)
        sys.exit(2)
    registrar(args[0], args[1] if len(args) == 2 else None, reel)

