"""Extrai quadros de um vídeo de uma letra gravada pelo Pedro.

A classe do rótulo é a letra informada. A caixa vem do detector.
Quadro sem mão vai para a pasta revisar, sem rótulo.
Os arquivos ficam no D: e não devem entrar no git.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.detector import PESOS_PADRAO, Detector

DESTINO = Path(r"D:\citizentech\cv\data\raw\pedro")
LETRAS = ["a", "b", "c", "d", "e", "i", "l", "m", "n", "o", "r", "s", "u", "v", "w"]


def caixa_yolo(bbox: list[float], largura: int, altura: int) -> str:
    x1, y1, x2, y2 = bbox
    return (
        f"{(x1 + x2) / 2 / largura:.6f} {(y1 + y2) / 2 / altura:.6f} "
        f"{(x2 - x1) / largura:.6f} {(y2 - y1) / altura:.6f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Extrai quadros de um vídeo de uma letra")
    parser.add_argument("--video", required=True)
    parser.add_argument("--letra", required=True)
    parser.add_argument("--a-cada", type=int, default=5, help="guarda 1 quadro a cada N")
    parser.add_argument("--pesos", default=str(PESOS_PADRAO))
    args = parser.parse_args()

    letra = args.letra.strip().lower()
    if letra not in LETRAS:
        print(f"letra fora do vocabulário atual: {' '.join(LETRAS)}")
        return 2

    captura = cv2.VideoCapture(args.video)
    if not captura.isOpened():
        print(f"não abriu {args.video}")
        return 2

    detector = Detector(args.pesos)
    pasta = DESTINO / letra
    revisar = pasta / "revisar"
    pasta.mkdir(parents=True, exist_ok=True)
    revisar.mkdir(parents=True, exist_ok=True)

    indice = 0
    guardados = 0
    sem_mao = 0
    while True:
        ok, frame = captura.read()
        if not ok or frame is None:
            break
        if indice % args.a_cada != 0:
            indice += 1
            continue
        nome = f"{letra}_{indice:06d}.jpg"
        resultado = detector.detectar(frame)
        if not resultado["deteccoes"]:
            cv2.imwrite(str(revisar / nome), frame)
            sem_mao += 1
        else:
            altura, largura = frame.shape[:2]
            cv2.imwrite(str(pasta / nome), frame)
            classe = LETRAS.index(letra)
            linha = f"{classe} {caixa_yolo(resultado['deteccoes'][0]['bbox'], largura, altura)}"
            (pasta / f"{letra}_{indice:06d}.txt").write_text(linha + "\n", encoding="utf-8")
            guardados += 1
        indice += 1

    captura.release()
    print(f"letra {letra}")
    print(f"com_mao {guardados}")
    print(f"sem_mao {sem_mao}")
    print(f"pasta {pasta}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
