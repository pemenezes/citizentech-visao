"""Conta palavras do resumo e do objetivo no HTML do relatório.

Uma palavra é um trecho separado por espaço, depois de tirar as marcas HTML.
O alvo do plano é resumo entre 240 e 250 e objetivo entre 45 e 50.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HTML = Path(__file__).resolve().parents[1] / "docs" / "relatorio.html"


def palavras(texto: str) -> list[str]:
    limpo = re.sub(r"<[^>]+>", " ", texto)
    limpo = limpo.replace("&nbsp;", " ")
    return [parte for parte in limpo.split() if parte]


def bloco(html: str, identificador: str) -> str:
    achado = re.search(
        rf'id="{identificador}"[^>]*>(.*?)</(?:p|div)>',
        html,
        flags=re.DOTALL,
    )
    if not achado:
        raise SystemExit(f"não achei #{identificador}")
    return achado.group(1)


def main() -> int:
    html = HTML.read_text(encoding="utf-8")
    limites = {"resumo": (240, 250), "objetivo": (45, 50)}
    codigo = 0
    for nome, (baixo, alto) in limites.items():
        total = len(palavras(bloco(html, nome)))
        estado = "ok" if baixo <= total <= alto else "fora"
        if estado != "ok":
            codigo = 1
        print(f"{nome} {total} {estado} alvo {baixo}-{alto}")
    return codigo


if __name__ == "__main__":
    raise SystemExit(main())
