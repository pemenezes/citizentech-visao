"""Salva exemplos em que o peso treinado erra a letra no teste."""

from __future__ import annotations

import csv
from pathlib import Path

import cv2
from ultralytics import YOLO

PESOS = Path(r"D:\citizentech\cv\runs\yolo26n_e40\weights\best.pt")
TESTE = Path(r"D:\citizentech\cv\data\processed\libras15_passos\images\test")
SAIDA = Path(r"D:\citizentech\cv\runs\erros_e40")
LIMITE = 12


def letra_de(caminho: Path) -> str:
    return caminho.stem.split("_", 1)[0].lower()


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    modelo = YOLO(str(PESOS))
    guardados = 0
    with (SAIDA / "erros.csv").open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["arquivo", "letra", "previsto", "confianca"])
        for foto in sorted(TESTE.glob("*.jpg")):
            if guardados >= LIMITE:
                break
            letra = letra_de(foto)
            resultado = modelo.predict(str(foto), imgsz=640, conf=0.25, device=0, verbose=False)[0]
            if resultado.boxes is None or len(resultado.boxes) == 0:
                previsto, confianca = "", 0.0
            else:
                indice = int(resultado.boxes.conf.argmax())
                previsto = resultado.names[int(resultado.boxes.cls[indice])]
                confianca = float(resultado.boxes.conf[indice])
            if previsto == letra:
                continue
            imagem = resultado.plot()
            cv2.putText(
                imagem,
                f"verdade {letra}",
                (8, 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
            destino = SAIDA / f"{guardados:02d}_{letra}_virou_{previsto or 'nada'}.jpg"
            cv2.imwrite(str(destino), imagem)
            escritor.writerow([foto.name, letra, previsto, f"{confianca:.3f}"])
            guardados += 1
    print(f"erros_salvos {guardados}")


if __name__ == "__main__":
    main()
