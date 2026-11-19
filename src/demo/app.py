"""Demo em tempo real: caixa, letra, confiança, FPS e palavra na tela.

A letra só entra na palavra depois de vários quadros seguidos acima do limiar.
Sem câmera, use um arquivo de vídeo.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from src.detector import PESOS_PADRAO, Detector
from src.soletrador import Soletrador


def abrir_captura(origem: str) -> cv2.VideoCapture:
    if origem.isdigit():
        indice = int(origem)
        # O DroidCam entrega quadro pelo Media Foundation. O DirectShow não abre.
        candidatos = (
            cv2.VideoCapture(indice, cv2.CAP_MSMF),
            cv2.VideoCapture(indice, cv2.CAP_DSHOW),
        )
    else:
        candidatos = (cv2.VideoCapture(origem),)
    for captura in candidatos:
        if not captura.isOpened():
            captura.release()
            continue
        ok, frame = captura.read()
        if ok and frame is not None:
            captura.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return captura
        captura.release()
    raise RuntimeError(f"não abriu a origem {origem}")


def ampliar(frame: np.ndarray, altura_minima: int = 480) -> np.ndarray:
    altura, largura = frame.shape[:2]
    if altura >= altura_minima:
        return frame
    escala = altura_minima / altura
    return cv2.resize(frame, (int(largura * escala), altura_minima), interpolation=cv2.INTER_LINEAR)


def desenhar(
    frame: np.ndarray,
    deteccoes: list[dict],
    soletrador: Soletrador,
    fps: float,
    limiar: float,
) -> np.ndarray:
    tela_video = frame.copy()
    principal = deteccoes[0] if deteccoes else None
    if principal is not None:
        x1, y1, x2, y2 = (int(v) for v in principal["bbox"])
        certo = principal["confianca"] >= limiar
        cor = (80, 200, 120) if certo else (160, 160, 160)
        rotulo = principal["classe"] if certo else "incerto"
        cv2.rectangle(tela_video, (x1, y1), (x2, y2), cor, 2)
        texto_y = y1 - 8
        if texto_y < 24:
            texto_y = min(tela_video.shape[0] - 10, y1 + 24)
        cv2.putText(
            tela_video,
            f"{rotulo} {principal['confianca']:.2f}",
            (x1, texto_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            cor,
            2,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            tela_video,
            "incerto",
            (16, 32),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (180, 180, 180),
            2,
            cv2.LINE_AA,
        )

    altura, largura = tela_video.shape[:2]
    painel = 340
    tela = np.full((altura, largura + painel, 3), 18, dtype=np.uint8)
    tela[:, :largura] = tela_video
    cv2.line(tela, (largura, 0), (largura, altura), (70, 70, 70), 1)

    letra = soletrador.letra_atual() or "incerto"
    linhas = (
        (48, 0.7, "palavra"),
        (96, 1.1, soletrador.texto or "..."),
        (160, 0.7, "agora"),
        (200, 0.9, letra),
        (260, 0.7, f"FPS {fps:.0f}"),
        (300, 0.55, "espaco  apagar  limpar  sair"),
    )
    for y, escala, texto in linhas:
        cv2.putText(
            tela,
            texto,
            (largura + 16, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            escala,
            (245, 245, 245),
            2,
            cv2.LINE_AA,
        )
    return tela


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo de soletração do alfabeto manual")
    parser.add_argument("--origem", default="0", help="índice da câmera ou caminho de vídeo")
    parser.add_argument("--reserva", default="", help="vídeo usado se a câmera não abrir")
    parser.add_argument("--pesos", default=str(PESOS_PADRAO))
    parser.add_argument("--saida", default=r"D:\citizentech\cv\video\demo_anotado.mp4")
    parser.add_argument("--limiar", type=float, default=0.60)
    parser.add_argument("--janela", type=int, default=12)
    parser.add_argument("--minimo", type=int, default=8)
    parser.add_argument("--sem-janela", action="store_true")
    args = parser.parse_args()

    try:
        captura = abrir_captura(args.origem)
        origem_usada = args.origem
    except RuntimeError as exc:
        if not args.reserva:
            print(exc)
            return 2
        print(f"{exc}; usando reserva {args.reserva}")
        captura = abrir_captura(args.reserva)
        origem_usada = args.reserva

    detector = Detector(args.pesos)
    soletrador = Soletrador(args.janela, args.minimo, args.limiar)
    instantes: deque[float] = deque(maxlen=30)
    escrita = None
    saida = Path(args.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    print(f"origem {origem_usada}")
    print(f"pesos {args.pesos}")

    while True:
        ok, frame = captura.read()
        if not ok or frame is None:
            break
        frame = ampliar(frame)
        agora = time.perf_counter()
        instantes.append(agora)
        resultado = detector.detectar(frame)
        principal = resultado["deteccoes"][0] if resultado["deteccoes"] else None
        if principal is None:
            soletrador.observar(None, 0.0)
        else:
            soletrador.observar(principal["classe"], principal["confianca"])

        if len(instantes) >= 2:
            fps = (len(instantes) - 1) / (instantes[-1] - instantes[0])
        else:
            fps = 0.0
        tela = desenhar(frame, resultado["deteccoes"], soletrador, fps, args.limiar)
        if escrita is None:
            altura, largura = tela.shape[:2]
            escrita = cv2.VideoWriter(
                str(saida),
                cv2.VideoWriter_fourcc(*"mp4v"),
                20.0,
                (largura, altura),
            )
        escrita.write(tela)

        if args.sem_janela:
            continue
        cv2.imshow("alfabeto manual", tela)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla in (ord("q"), 27):
            break
        if tecla == ord(" "):
            soletrador.espaco()
        if tecla in (8, 127):
            soletrador.apagar()
        if tecla == ord("x"):
            soletrador.limpar()

    captura.release()
    if escrita is not None:
        escrita.release()
    if not args.sem_janela:
        cv2.destroyAllWindows()
    print(f"texto {soletrador.texto!r}")
    print(f"saida {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
