"""Roda o farol num vídeo e grava a fase quadro a quadro.

Não altera o peso da Libras. O número de acordo com um operador ainda
não sai daqui: a conferência abaixo só diz se a regra segurou a fase
quando o próprio detector viu alguém na faixa.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from src.farol.fase import Farol
from src.farol.zonas import CENAS, VEICULOS, contem, dentro_de_alguma

PESOS = Path(r"D:\citizentech\cv\models\yolo26n.pt")


def centro(caixa: list[float]) -> tuple[float, float]:
    x1, y1, x2, y2 = caixa
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def pes(caixa: list[float]) -> tuple[float, float]:
    x1, _, x2, y2 = caixa
    return ((x1 + x2) / 2, y2)


def desenhar_zona(tela: np.ndarray, zona: np.ndarray, cor: tuple[int, int, int]) -> None:
    cv2.polylines(tela, [zona], True, cor, 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cena", choices=tuple(CENAS), default="faixa")
    parser.add_argument(
        "--origem",
        default="",
    )
    parser.add_argument(
        "--saida",
        default="",
    )
    parser.add_argument("--pesos", default=str(PESOS))
    args = parser.parse_args()

    cena = CENAS[args.cena]
    faixa, via, espera = cena["faixa"], cena["via"], cena["espera"]
    origem = args.origem or rf"D:\citizentech\cv\video\farol\{args.cena}.mp4"
    saida = args.saida or rf"D:\citizentech\cv\video\farol\{args.cena}_anotada.mp4"
    captura = cv2.VideoCapture(origem)
    if not captura.isOpened():
        raise SystemExit(f"não abriu {origem}")
    fps_video = captura.get(cv2.CAP_PROP_FPS) or 30.0
    largura = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (largura, altura) != cena["tamanho"]:
        raise SystemExit(
            f"as zonas de {args.cena} valem para {cena['tamanho'][0]}×{cena['tamanho'][1]}, "
            f"o vídeo é {largura}×{altura}"
        )

    modelo = YOLO(args.pesos)
    farol = Farol()
    destino = Path(saida)
    destino.parent.mkdir(parents=True, exist_ok=True)
    escritor = cv2.VideoWriter(
        str(destino),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps_video,
        (largura, altura),
    )
    dt = 1.0 / fps_video
    quadros = 0
    pessoa_na_faixa = 0
    segurou = 0
    segundos: dict[int, str] = {}
    inicio = time.perf_counter()

    while True:
        ok, frame = captura.read()
        if not ok:
            break
        resultado = modelo.predict(frame, imgsz=640, conf=0.25, device=0, verbose=False)[0]
        pessoas_faixa = veiculos_via = veiculos_faixa = esperando = 0
        tela = frame.copy()
        desenhar_zona(tela, faixa, (255, 180, 0))
        desenhar_zona(tela, via, (0, 180, 255))
        for zona in espera:
            desenhar_zona(tela, zona, (180, 180, 180))
        if resultado.boxes is not None:
            for caixa in resultado.boxes:
                classe = resultado.names[int(caixa.cls[0])]
                xyxy = [float(v) for v in caixa.xyxy[0]]
                x1, y1, x2, y2 = (int(v) for v in xyxy)
                cv2.rectangle(tela, (x1, y1), (x2, y2), (255, 255, 255), 1)
                if classe == "person":
                    ponto = pes(xyxy)
                    if contem(faixa, ponto):
                        pessoas_faixa += 1
                    elif dentro_de_alguma(espera, ponto):
                        esperando += 1
                elif classe in VEICULOS:
                    if contem(faixa, pes(xyxy)):
                        veiculos_faixa += 1
                    elif contem(via, centro(xyxy)):
                        veiculos_via += 1
        fase = farol.atualizar(pessoas_faixa, veiculos_via, veiculos_faixa, esperando, dt)
        quadros += 1
        if pessoas_faixa > 0:
            pessoa_na_faixa += 1
            if fase == "PEDESTRE":
                segurou += 1
        segundos[int((quadros - 1) / fps_video)] = fase
        cor = (0, 140, 255) if fase == "PEDESTRE" else (80, 200, 120)
        cv2.rectangle(tela, (0, 0), (largura, 150), (0, 0, 0), -1)
        cv2.putText(tela, fase, (16, 48), cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor, 3)
        cv2.putText(
            tela,
            f"faixa {pessoas_faixa}  via {veiculos_via}  espera {esperando}",
            (16, 96),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        escritor.write(tela)

    captura.release()
    escritor.release()
    decorrido = time.perf_counter() - inicio
    fps = quadros / decorrido if decorrido else 0.0
    pedestre = sum(1 for fase in segundos.values() if fase == "PEDESTRE")
    print(f"quadros {quadros}")
    print(f"fps {fps:.1f}")
    print(f"segundos {len(segundos)} pedestre {pedestre} via {len(segundos) - pedestre}")
    print(f"pessoa_na_faixa {pessoa_na_faixa} segurou {segurou}")
    linha = " ".join(f"{segundo}:{fase.split()[-1]}" for segundo, fase in sorted(segundos.items()))
    print(f"linha {linha}")
    print(f"saida {destino}")


if __name__ == "__main__":
    main()
