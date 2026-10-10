"""Prepara o trabalho de um Reel do Pomake sem que o modelo precise ler a estratégia inteira.

Uso:
  python3 preparar.py candidatas [--n 5]
  python3 preparar.py territorios
  python3 preparar.py pautas --territorio <1-6>
  python3 preparar.py redator --pauta <ID>
  python3 preparar.py redator --territorio <1-6> --tema "<tema pedido por Eduardo>"
  python3 preparar.py revisor <arquivo-do-reel.md>
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
from _comum import (ESTRATEGIA, POMAKE, RAIZ, campo, ler_pautas, ler_reels,  # noqa: E402
                    secoes)

SKILL = Path(__file__).resolve().parents[1]
ESTADOS_REFERENCIA = {"aprovado", "publicado"}
STATUS_ELEGIVEIS = ["apta", "nao_avaliada"]
MAX_EXEMPLOS = 2
MAX_NAO_REPETIR = 30

SECOES_TERRITORIO = ["Situação humana", "Trabalho editorial", "Tese do Pomake", "Fronteiras",
                     "Critério para reconhecer uma pauta deste território"]
SECAO_T6 = "Funcionamento confirmado relevante para este território"
SECOES_FUNDACAO = ["Público", "Papel do perfil", "Promessa editorial", "Limites", "Linguagem e criação"]


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


def arquivo_territorio(numero):
    achados = sorted((ESTRATEGIA / "territories").glob(f"0{numero}-*.md"))
    if len(achados) != 1:
        raise ErroExtracao(f"ERRO: arquivo do território {numero} não encontrado.")
    return achados[0]


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
    """Extrai do banco somente a série e a pauta indicadas."""
    caminho = ESTRATEGIA / pauta["arquivo"]
    texto = ler(caminho)
    numero = int(pauta["id"].split("-P")[1])
    m = re.search(rf"^### Pauta {numero} — .*?(?=^### |^## |\Z)", texto, re.M | re.S)
    if not m:
        raise ErroExtracao(f"ERRO: pauta {numero} não encontrada em {caminho.relative_to(RAIZ)}.")
    return f"**Pauta:** {pauta['id']}\n**Território:** {pauta['territorio']}\n**Série:** {pauta['serie']}\n\n{m.group(0).strip()}"


def exemplos_aprovados(reels, excluir=None):
    refs = [r for r in reels if r["estado"] in ESTADOS_REFERENCIA and r["caminho"] != excluir]
    return refs[-MAX_EXEMPLOS:]


def lista_nao_repetir(reels, excluir=None):
    linhas = []
    outros = [r for r in reels if r["caminho"] != excluir][-MAX_NAO_REPETIR:]
    for r in outros:
        f = r["falas"]
        linhas.append(
            f"- **{r['relativo'].split('/')[-1]}** ({r['estado']}, território {r['territorio']})\n"
            f"  - Fala 1: {f.get('Fala 1', '—')}\n"
            f"  - Texto do criativo: {' '.join(r['secoes'].get('Texto do criativo', '—').split())}\n"
            f"  - Fechamento: {f.get('Fechamento', '—')}")
    rejeicoes = [f"- **{r['relativo'].split('/')[-1]}:** {' '.join(r['secoes'].get('Avaliação de Eduardo', '').split())}"
                 for r in reels if r["estado"] == "rejeitado" and r["secoes"].get("Avaliação de Eduardo")]
    texto = "Não repita gancho, texto do criativo, transições, frases de fechamento nem o argumento destes Reels:\n\n"
    texto += "\n".join(linhas) if linhas else "(nenhum Reel anterior)"
    texto += "\n\n### Motivos de rejeição de Eduardo (evite todos)\n\n"
    texto += "\n".join(rejeicoes) if rejeicoes else "(nenhuma rejeição registrada)"
    return texto


def blocos_exemplos(reels, excluir=None):
    exemplos = exemplos_aprovados(reels, excluir)
    if not exemplos:
        return [bloco("Reels aprovados (referência de nível)", "domains/products/pomake/reels/",
                      "(nenhum Reel aprovado ainda)")]
    return [bloco(f"Reel aprovado {i} (referência de nível, não de molde)", r["relativo"], r["texto"])
            for i, r in enumerate(exemplos, 1)]


def blocos_territorio(numero, secoes_desejadas):
    caminho = arquivo_territorio(numero)
    titulos = list(secoes_desejadas)
    if str(numero) == "6" and SECAO_T6 not in titulos:
        titulos.append(SECAO_T6)
    return bloco(f"Território {numero} — essencial", caminho.relative_to(RAIZ).as_posix(),
                 extrair(caminho, titulos, prefixo=True))


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
        return (STATUS_ELEGIVEIS.index(p["status"]), contagem.get(t, 0), p["id"][:2], p["id"])

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
        print(f"{i}. {p['id']} [{p['status']}] — {p['titulo']} (território {p['territorio']}; série {p['serie']})")


def cmd_territorios(args):
    """Resumo dos 6 territórios e da regra de propriedade, para classificar um tema de Eduardo."""
    sec = secoes(ler(ESTRATEGIA / "territories.md"))
    for titulo, corpo in sec.items():
        m = re.match(r"(\d)\. \[(.+?)\]", titulo)
        if m:
            print(f"{m.group(1)}. {m.group(2)}: {corpo.split(chr(10)+chr(10))[0].strip()}")
    print()
    print(extrair(ESTRATEGIA / "territories.md", ["Regra de propriedade editorial"]))


def cmd_pautas(args):
    """Títulos e status das pautas de um território, para encontrar a que corresponde a um tema."""
    for p in ler_pautas():
        if p["territorio"].split(" ")[0] == str(args.territorio):
            print(f"{p['id']} [{p['status']}] — {p['titulo']}")


def cmd_redator(args):
    reels = ler_reels()
    if args.pauta:
        pauta = pauta_por_id(args.pauta)
        numero = pauta["territorio"].split(" ")[0]
        bloco_pauta = bloco("Pauta", f"editorial-strategy/{pauta['arquivo']}", texto_da_pauta(pauta))
        extra_tema = []
    else:
        if not (args.territorio and args.tema):
            raise SystemExit("ERRO: use --pauta <ID> ou --territorio <1-6> --tema \"...\".")
        numero = str(args.territorio)
        bloco_pauta = bloco("Tema pedido por Eduardo", "pedido de Eduardo",
                            f"**Pauta:** orientacao-eduardo\n**Território:** {numero}\n\n{args.tema}\n\n"
                            "Não troque este tema por outro.")
        extra_tema = [bloco("Territórios e regra de propriedade", "editorial-strategy/territories.md",
                            extrair(ESTRATEGIA / "territories.md", ["Regra de propriedade editorial"]))]

    partes = [
        "# Briefing do redator — Reel do Pomake\n\n"
        "Leia na ordem. As primeiras seções definem a qualidade; as seguintes definem o assunto e os limites.",
        bloco("Instruções do redator", ".agents/skills/pomake-reels/references/redator.md",
              sem_titulo(ler(SKILL / "references/redator.md"))),
        bloco("Catálogo de ganchos", "editorial-strategy/hooks.md", sem_titulo(ler(ESTRATEGIA / "hooks.md"))),
        bloco("Voz e padrão de copy", "editorial-strategy/voice.md", sem_titulo(ler(ESTRATEGIA / "voice.md"))),
        bloco("Formato do Reel com a Lívia", "editorial-strategy/reel-livia.md",
              sem_titulo(ler(ESTRATEGIA / "reel-livia.md"))),
        bloco("Lívia", "creative-direction/livia.md", sem_titulo(ler(POMAKE / "creative-direction/livia.md"))),
        *blocos_exemplos(reels),
        bloco_pauta,
        blocos_territorio(numero, SECOES_TERRITORIO),
        bloco("Regra de produção", "editorial-strategy/territories.md",
              extrair(ESTRATEGIA / "territories.md", ["Regra de produção"])),
        *extra_tema,
        bloco("Fundação: público, promessa e limites", "editorial-strategy/foundation.md",
              extrair(ESTRATEGIA / "foundation.md", SECOES_FUNDACAO)),
        bloco("Ponte editorial (qualificação da pauta)", "editorial-strategy/production-bridge.md",
              sem_titulo(ler(ESTRATEGIA / "production-bridge.md"))),
        *blocos_pomake(numero),
        bloco("O que não repetir", "domains/products/pomake/reels/", lista_nao_repetir(reels)),
    ]
    nome = f"redator-{args.pauta or 'orientacao-eduardo'}"
    gravar(nome, partes)


def cmd_revisor(args):
    caminho = Path(args.reel).resolve()
    if not caminho.exists():
        raise SystemExit(f"ERRO: Reel não encontrado: {args.reel}")
    texto = caminho.read_text(encoding="utf-8")
    reel = {"texto": texto, "relativo": caminho.name,
            "pauta": campo(texto, "Pauta"), "territorio": campo(texto, "Território")}
    reels = ler_reels()
    numero = reel["territorio"]
    if not numero:
        raise SystemExit("ERRO: o Reel não tem o campo Território.")
    if reel["pauta"] and reel["pauta"] != "orientacao-eduardo":
        pauta = pauta_por_id(reel["pauta"])
        bloco_pauta = bloco("Pauta", f"editorial-strategy/{pauta['arquivo']}", texto_da_pauta(pauta))
    else:
        bloco_pauta = bloco("Pauta", "pedido de Eduardo", "orientacao-eduardo (tema dado por Eduardo).")
    partes = [
        "# Briefing do revisor — Reel do Pomake\n\n"
        "Você não participou da criação. Avalie somente com o checklist e o material abaixo.",
        bloco("Checklist de revisão", ".agents/skills/pomake-reels/references/revisao.md",
              sem_titulo(ler(SKILL / "references/revisao.md"))),
        bloco("Reel em revisão", reel["relativo"], reel["texto"]),
        *blocos_exemplos(reels, excluir=caminho),
        bloco("Catálogo de ganchos", "editorial-strategy/hooks.md", sem_titulo(ler(ESTRATEGIA / "hooks.md"))),
        bloco("Voz e padrão de copy", "editorial-strategy/voice.md", sem_titulo(ler(ESTRATEGIA / "voice.md"))),
        bloco("Formato do Reel com a Lívia", "editorial-strategy/reel-livia.md",
              sem_titulo(ler(ESTRATEGIA / "reel-livia.md"))),
        bloco_pauta,
        blocos_territorio(numero, ["Trabalho editorial", "Fronteiras",
                                   "Critério para reconhecer uma pauta deste território"]),
        bloco("Fundação: limites e linguagem", "editorial-strategy/foundation.md",
              extrair(ESTRATEGIA / "foundation.md", ["Limites", "Linguagem e criação"])),
        bloco("Controle de qualidade da ponte editorial", "editorial-strategy/production-bridge.md",
              extrair(ESTRATEGIA / "production-bridge.md", ["Controle de qualidade antes de qualquer publicação"])),
        *blocos_pomake(numero),
        bloco("Outros Reels (para checar repetição)", "domains/products/pomake/reels/",
              lista_nao_repetir(reels, excluir=caminho)),
    ]
    gravar(f"revisor-{caminho.stem}", partes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="comando", required=True)
    c = sub.add_parser("candidatas")
    c.add_argument("--n", type=int, default=5)
    r = sub.add_parser("redator")
    r.add_argument("--pauta")
    r.add_argument("--territorio", type=int, choices=range(1, 7))
    r.add_argument("--tema")
    sub.add_parser("territorios")
    sub.add_parser("rascunhos")
    pt = sub.add_parser("pautas")
    pt.add_argument("--territorio", type=int, choices=range(1, 7), required=True)
    v = sub.add_parser("revisor")
    v.add_argument("reel")
    args = parser.parse_args()
    {"candidatas": cmd_candidatas, "territorios": cmd_territorios, "pautas": cmd_pautas,
     "rascunhos": cmd_rascunhos,
     "redator": cmd_redator, "revisor": cmd_revisor}[args.comando](args)


if __name__ == "__main__":
    main()
