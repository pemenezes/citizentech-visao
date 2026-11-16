"""Monta um vídeo curto com letras do teste público para exercitar a demo.

Repete uma foto e intercala um quadro vazio, para a soletração aceitar
cada letra uma vez. Não é o vídeo do Pedro.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

TESTE = Path(r"D:\citizentech\cv\data\processed\libras15_passos\images\test")
SAIDA = Path(r"D:\citizentech\cv\video\prova_dedo.mp4")
LETRAS = ("d", "e", "d", "o")
QUADROS_LETRA = 20
QUADROS_INTERVALO = 15


def primeira_foto(letra: str) -> Path:
    fotos = sorted(TESTE.glob(f"{letra.upper()}_*.jpg"))
    if not fotos:
        raise FileNotFoundError(letra)
    return fotos[0]


def main() -> None:
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    amostra = cv2.imread(str(primeira_foto("d")))
    vazio = np.full_like(amostra, 40)
    escrita = cv2.VideoWriter(
        str(SAIDA),
        cv2.VideoWriter_fourcc(*"mp4v"),
        20.0,
        (amostra.shape[1], amostra.shape[0]),
    )
    for letra in LETRAS:
        foto = cv2.imread(str(primeira_foto(letra)))
        for _ in range(QUADROS_LETRA):
            escrita.write(foto)
        for _ in range(QUADROS_INTERVALO):
            escrita.write(vazio)
    escrita.release()
    print(f"saida {SAIDA}")


if __name__ == "__main__":
    main()
