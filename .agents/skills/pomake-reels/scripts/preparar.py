"""Prepara o trabalho de um Reel do Pomake sem que o modelo precise ler a estratégia inteira.

Uso:
  python3 preparar.py candidatas [--n 5]
  python3 preparar.py territorios
  python3 preparar.py pautas --territorio <1-6>
  python3 preparar.py historia --pauta <ID>
  python3 preparar.py historia --territorio <1-6> --tema "<tema>"
  python3 preparar.py historias
  python3 preparar.py redator --pauta <ID>
  python3 preparar.py redator --territorio <1-6> --tema "<tema pedido por Eduardo>"
  python3 preparar.py materias
  python3 preparar.py adaptador
  python3 preparar.py rascunhos

O Reel é escrito como rascunho fora do repositório (pasta indicada por "rascunhos") e só
entra em domains/products/pomake/reels/ depois da aprovação de Eduardo.

Os briefings são extraídos dos documentos originais da estratégia, que continuam sendo a
única fonte. Eles são gravados em arquivos temporários, fora do repositório; o script
imprime o caminho e o tamanho. Se uma seção esperada não existir, o script para com erro.

Títulos de seção dos quais este script depende estão listados em
domains/products/pomake/editorial-strategy/README.md (seção "Títulos usados pelo gerador").
"""
import argparse
import os
import re
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import (ESTRATEGIA, POMAKE, RAIZ, ler_pautas,  # noqa: E402
                    ler_reels, secoes)

SKILL = Path(__file__).resolve().parents[1]
STATUS_ELEGIVEIS = ["ativa"]
SECOES_FUNDACAO = ["Público", "Limites"]


class ErroExtracao(SystemExit):
    pass


def ler(caminho):
    if not caminho.exists():
        raise ErroExtracao(f"ERRO: arquivo não encontrado: {caminho.relative_to(RAIZ)}")
    return caminho.read_text(encoding="utf-8")


def extrair(caminho, titulos, prefixo=False):
    """Extrai seções '## <título>' de um arquivo. Para com erro se alguma não existir."""
    sec = secoes(ler(caminho))
    partes = []
    for titulo in titulos:
        chave = next((t for t in sec if (t.startswith(titulo) if prefixo else t == titulo)), None)
        if chave is None:
            raise ErroExtracao(
                f"ERRO: seção '## {titulo}' não encontrada em {caminho.relative_to(RAIZ)}. "
                "O briefing não foi gerado. Restaure o título ou atualize o gerador.")
        partes.append(f"### {chave}\n\n{sec[chave]}")
    return "\n\n".join(partes)


def corpo_antes_de(caminho, titulo):
    texto = ler(caminho)
    if f"\n## {titulo}" not in texto:
        raise ErroExtracao(f"ERRO: seção '## {titulo}' não encontrada em {caminho.relative_to(RAIZ)}.")
    return texto.split(f"\n## {titulo}")[0].strip()


def sem_titulo(texto):
    """Remove a primeira linha de título '# ...' e linhas de metadados em negrito do topo."""
    linhas = texto.strip().split("\n")
    while linhas and (linhas[0].startswith("# ") or linhas[0].startswith("**") or not linhas[0].strip()):
        linhas.pop(0)
    return "\n".join(linhas).strip()


def rebaixar_titulos(texto):
    """Rebaixa os títulos do conteúdo incorporado em um nível, sem tocar em blocos de código,
    para que só os blocos do briefing fiquem no nível '##'."""
    linhas, em_codigo = [], False
    for linha in texto.split("\n"):
        if linha.strip().startswith("```"):
            em_codigo = not em_codigo
        elif not em_codigo and re.match(r"^#{1,5} ", linha):
            linha = "#" + linha
        linhas.append(linha)
    return "\n".join(linhas)


def bloco(titulo, fonte, conteudo):
    return f"## {titulo}\n\n_Fonte: {fonte}_\n\n{rebaixar_titulos(conteudo.strip())}\n"


def pauta_por_id(pauta_id):
    pauta = next((p for p in ler_pautas() if p["id"] == pauta_id), None)
    if pauta is None:
        raise ErroExtracao(f"ERRO: pauta '{pauta_id}' não existe em pautas.yaml.")
    return pauta


def texto_da_pauta(pauta):
    """Extrai do banco somente a pauta indicada."""
    caminho = ESTRATEGIA / pauta["arquivo"]
    texto = ler(caminho)
    numero = int(pauta["id"].split("-P")[1])
    m = re.search(rf"^### Pauta {numero} — .*?(?=^### |^## |\Z)", texto, re.M | re.S)
    if not m:
        raise ErroExtracao(f"ERRO: pauta {numero} não encontrada em {caminho.relative_to(RAIZ)}.")
    corpo = m.group(0).strip().split("\n", 1)[1].strip()
    return f"**Pauta:** {pauta['id']}\n**Título:** {pauta['titulo']}\n**Território:** {pauta['territorio']}\n\n{corpo}"


def recortes_anteriores(pauta_id, reels):
    """Mostra o conteúdo já produzido com a mesma ideia antes de escolher outro recorte."""
    anteriores = [r for r in reels if r["pauta"] == pauta_id]
    if not anteriores:
        return "(esta pauta ainda não tem Reel aprovado)"
    linhas = []
    for r in anteriores:
        roteiro = re.sub(r"^(Fala \d+|Fechamento):\s*", "",
                         r["secoes"].get("Roteiro da Lívia", "").strip(), flags=re.M)
        frases = re.split(r"(?<=[.?!])\s+", roteiro)
        recorte = r.get("recorte") or (frases[0] if frases else "—")
        final = r["falas"].get("Fechamento") or (frases[-1] if frases else "—")
        linhas.append(f"- **{r['relativo']}**\n  - Recorte: {recorte}\n  - Final: {final}")
    return "Escolha outra cena, dúvida e ação prática. Mudar apenas a profissão não basta.\n\n" + "\n".join(linhas)


def bloco_territorio(numero):
    """Só o resumo do território: do que fala e como o Reel termina."""
    sec = secoes(ler(ESTRATEGIA / "territories.md"))
    chave = next((t for t in sec if t.startswith(f"{numero}. ")), None)
    if chave is None:
        raise ErroExtracao(f"ERRO: território {numero} não encontrado em territories.md.")
    return bloco(f"Território {chave}", "editorial-strategy/territories.md", sec[chave])


def blocos_pomake(numero):
    if str(numero) != "6":
        return []
    caminho = POMAKE / "o-que-e-o-pomake.md"
    return [bloco("O que é o Pomake (funções confirmadas; único território que cita o produto)",
                  caminho.relative_to(RAIZ).as_posix(), sem_titulo(corpo_antes_de(caminho, "Estado e uso")))]


def pasta_trabalho():
    pasta = Path(os.environ.get("POMAKE_REELS_TMP", Path(tempfile.gettempdir()) / "pomake-reels"))
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def cmd_rascunhos(args):
    pasta = pasta_trabalho() / "rascunhos"
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"RASCUNHOS: {pasta}")
    for arquivo in sorted(pasta.glob("*.md")):
        print(f"- {arquivo}")


def cmd_materias(args):
    pasta = pasta_trabalho() / "materias"
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"MATERIAS: {pasta}")
    for arquivo in sorted(pasta.glob("*.md")):
        print(f"- {arquivo}")


def cmd_historias(args):
    pasta = pasta_trabalho() / "historias"
    pasta.mkdir(parents=True, exist_ok=True)
    print(f"HISTORIAS: {pasta}")
    for arquivo in sorted(pasta.glob("*.md")):
        print(f"- {arquivo}")


def gravar(nome, partes):
    pasta = pasta_trabalho()
    destino = pasta / f"{nome}-{time.strftime('%Y%m%d-%H%M%S')}.md"
    conteudo = "\n\n".join(p.strip() for p in partes if p and p.strip()) + "\n"
    destino.write_text(conteudo, encoding="utf-8")
    print(f"BRIEFING: {destino}")
    print(f"TAMANHO: {len(conteudo)} caracteres (~{len(conteudo) // 4} tokens)")
    return destino


def cmd_candidatas(args):
    reels = ler_reels()
    ultimo = reels[-1]["territorio"] if reels else None
    contagem = {}
    for r in reels:
        contagem[r["territorio"]] = contagem.get(r["territorio"], 0) + 1
    elegiveis = [p for p in ler_pautas() if p.get("status") in STATUS_ELEGIVEIS]
    elegiveis = [p for p in elegiveis if p["territorio"].split(" ")[0] != ultimo] or elegiveis

    def chave(p):
        t = p["territorio"].split(" ")[0]
        return (len(p.get("reels", [])), contagem.get(t, 0), p["id"])

    elegiveis.sort(key=chave)
    escolhidas, territorios = [], []
    for p in elegiveis:  # uma por território primeiro, depois completa
        t = p["territorio"].split(" ")[0]
        if t not in territorios:
            escolhidas.append(p)
            territorios.append(t)
        if len(escolhidas) == args.n:
            break
    for p in elegiveis:
        if len(escolhidas) >= args.n:
            break
        if p not in escolhidas:
            escolhidas.append(p)
    if not escolhidas:
        print("NENHUMA PAUTA ELEGÍVEL. Informe Eduardo.")
        return
    print(f"Território do Reel mais recente: {ultimo or '—'}. Use as pautas nesta ordem:\n")
    for i, p in enumerate(escolhidas, 1):
        usos = len(p.get("reels", []))
        print(f"{i}. {p['id']} [{p['status']}, {usos} Reel(s)] — {p['titulo']} (território {p['territorio']})")


def cmd_territorios(args):
    """Resumo dos 6 territórios e da regra de propriedade, para classificar um tema de Eduardo."""
    sec = secoes(ler(ESTRATEGIA / "territories.md"))
    for titulo, corpo in sec.items():
        if re.match(r"\d\. ", titulo):
            print(f"{titulo}: {corpo.split(chr(10))[0].replace('**Do que fala:** ', '').strip()}")
    print()
    print(extrair(ESTRATEGIA / "territories.md", ["Regra de propriedade editorial"]))


def cmd_pautas(args):
    """Títulos e status das pautas de um território, para encontrar a que corresponde a um tema."""
    for p in ler_pautas():
        if p["territorio"].split(" ")[0] == str(args.territorio):
            print(f"{p['id']} [{p['status']}, {len(p.get('reels', []))} Reel(s)] — {p['titulo']}")


def dados_do_assunto(args):
    if args.pauta:
        pauta = pauta_por_id(args.pauta)
        numero = pauta["territorio"].split(" ")[0]
        assunto = bloco("Pauta", f"editorial-strategy/{pauta['arquivo']}", texto_da_pauta(pauta))
    else:
        if not (args.territorio and args.tema):
            raise SystemExit('ERRO: use --pauta <ID> ou --territorio <1-6> --tema "<tema>".')
        numero = str(args.territorio)
        assunto = bloco("Tema pedido por Eduardo", "pedido de Eduardo",
                        f"**Pauta:** orientacao-eduardo\n**Território:** {numero}\n\n{args.tema}\n\n"
                        "Não troque este tema por outro.")
    return numero, assunto


def cmd_historia(args):
    numero, assunto = dados_do_assunto(args)
    reels = ler_reels()
    partes = [
        "# Briefing da história bruta — Reel do Pomake",
        bloco("Como contar a história", ".agents/skills/pomake-reels/references/historia.md",
              sem_titulo(ler(SKILL / "references/historia.md"))),
        assunto,
        *([bloco("Recortes já usados nesta pauta", "domains/products/pomake/reels/",
                 recortes_anteriores(args.pauta, reels))] if args.pauta else []),
        bloco_territorio(numero),
        bloco("Público e limites", "editorial-strategy/foundation.md",
              extrair(ESTRATEGIA / "foundation.md", SECOES_FUNDACAO)),
        *blocos_pomake(numero),
    ]
    gravar(f"historia-{args.pauta or 'orientacao-eduardo'}", partes)


def cmd_redator(args):
    numero, bloco_pauta = dados_do_assunto(args)
    if args.pauta:
        pauta = pauta_por_id(args.pauta)
        direcao = bloco("Assunto", f"editorial-strategy/{pauta['arquivo']}",
                       f"**Pauta:** {pauta['id']}\n**Título:** {pauta['titulo']}")
    else:
        direcao = bloco_pauta

    partes = [
        "# Briefing do redator — matéria do Pomake\n\n"
        "Leia também a história bruta indicada pelo coordenador. Ela é o insumo principal.",
        bloco("Instruções do redator", ".agents/skills/pomake-reels/references/redator.md",
              sem_titulo(ler(SKILL / "references/redator.md"))),
        direcao,
        bloco_territorio(numero),
        bloco("Limites", "editorial-strategy/foundation.md",
              extrair(ESTRATEGIA / "foundation.md", ["Limites"])),
        *blocos_pomake(numero),
    ]
    nome = f"redator-{args.pauta or 'orientacao-eduardo'}"
    gravar(nome, partes)


def cmd_adaptador(args):
    partes = [
        "# Briefing do adaptador — fala para Reels do Pomake\n\n"
        "Leia também a matéria indicada pelo coordenador. Ela é o único insumo de conteúdo.",
        bloco("Instruções do adaptador", ".agents/skills/pomake-reels/references/adaptador.md",
              sem_titulo(ler(SKILL / "references/adaptador.md"))),
        bloco("Limites", "editorial-strategy/foundation.md",
              extrair(ESTRATEGIA / "foundation.md", ["Limites"])),
    ]
    gravar("adaptador", partes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)
    c = sub.add_parser("candidatas")
    c.add_argument("--n", type=int, default=5)
    r = sub.add_parser("redator")
    r.add_argument("--pauta")
    r.add_argument("--territorio", type=int, choices=range(1, 7))
    r.add_argument("--tema")
    h = sub.add_parser("historia")
    h.add_argument("--pauta")
    h.add_argument("--territorio", type=int, choices=range(1, 7))
    h.add_argument("--tema")
    sub.add_parser("territorios")
    sub.add_parser("materias")
    sub.add_parser("adaptador")
    sub.add_parser("rascunhos")
    sub.add_parser("historias")
    pt = sub.add_parser("pautas")
    pt.add_argument("--territorio", type=int, choices=range(1, 7), required=True)
    args = parser.parse_args()
    {"candidatas": cmd_candidatas, "territorios": cmd_territorios, "pautas": cmd_pautas,
     "rascunhos": cmd_rascunhos, "materias": cmd_materias, "historias": cmd_historias,
     "historia": cmd_historia, "redator": cmd_redator,
     "adaptador": cmd_adaptador}[args.comando](args)


if __name__ == "__main__":
    main()

