"""Detecção desacoplada: uma imagem entra, caixas e letras saem."""

from __future__ import annotations

import time
from pathlib import Path

from ultralytics import YOLO

PESOS_PADRAO = Path(r"D:\citizentech\cv\models\libras16_pedro2_yolo26n.pt")


class Detector:
    def __init__(self, pesos: Path | str = PESOS_PADRAO, dispositivo: int | str = 0) -> None:
        self.pesos = Path(pesos)
        self.dispositivo = dispositivo
        self.modelo = YOLO(str(self.pesos))

    def detectar(self, imagem, confianca_minima: float = 0.25) -> dict:
        inicio = time.perf_counter()
        resultado = self.modelo.predict(
            imagem,
            imgsz=640,
            conf=confianca_minima,
            device=self.dispositivo,
            verbose=False,
        )[0]
        deteccoes = []
        if resultado.boxes is not None:
            for caixa in resultado.boxes:
                x1, y1, x2, y2 = (float(v) for v in caixa.xyxy[0])
                indice = int(caixa.cls[0])
                deteccoes.append(
                    {
                        "classe": resultado.names[indice],
                        "confianca": float(caixa.conf[0]),
                        "bbox": [x1, y1, x2, y2],
                    }
                )
        deteccoes.sort(key=lambda item: item["confianca"], reverse=True)
        return {
            "deteccoes": deteccoes,
            "tempo_ms": (time.perf_counter() - inicio) * 1000,
        }
