"""Confere a votação da soletração sem usar a GPU."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.soletrador import Soletrador


def alimentar(soletrador: Soletrador, classe: str | None, vezes: int, confianca: float = 0.9) -> list[str]:
    aceitas = []
    for _ in range(vezes):
        letra = soletrador.observar(classe, confianca)
        if letra:
            aceitas.append(letra)
    return aceitas


def main() -> None:
    soletrador = Soletrador(janela=12, minimo=8, limiar=0.60)
    assert alimentar(soletrador, "d", 7) == []
    assert alimentar(soletrador, "d", 2) == ["d"]
    assert alimentar(soletrador, "d", 10) == []
    assert soletrador.texto == "d"

    assert alimentar(soletrador, None, 8, 0.0) == []
    assert alimentar(soletrador, "e", 8) == ["e"]
    assert soletrador.texto == "de"

    assert alimentar(soletrador, "o", 8, 0.40) == []
    assert soletrador.texto == "de"
    assert alimentar(soletrador, None, 8, 0.0) == []
    assert alimentar(soletrador, "o", 8, 0.80) == ["o"]

    soletrador.espaco()
    soletrador.apagar()
    assert soletrador.texto == "deo"
    soletrador.apagar()
    assert soletrador.texto == "de"
    print("soletrador_ok", soletrador.texto)


if __name__ == "__main__":
    main()
