"""Inferência curta para aceitar o ambiente.

Baixa um modelo pequeno para D:\\citizentech\\cv\\models, mede FPS na GPU
e grava uma imagem anotada em runs/smoke. Não treina e não usa dataset.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from ultralytics import YOLO, settings

ROOT = Path(r"D:\citizentech\cv")
MODELS = ROOT / "models"
RUNS = ROOT / "runs" / "smoke"
CANDIDATES = ("yolo26n.pt", "yolo11n.pt")


def configure_paths() -> None:
    settings.update(
        {
            "weights_dir": str(MODELS),
            "datasets_dir": str(ROOT / "data"),
            "runs_dir": str(ROOT / "runs"),
        }
    )


def load_model() -> tuple[YOLO, str]:
    last_error: Exception | None = None
    for name in CANDIDATES:
        dest = MODELS / name
        try:
            if not dest.exists():
                YOLO(name)
                downloaded = Path.cwd() / name
                if downloaded.exists():
                    downloaded.replace(dest)
            model = YOLO(str(dest))
            return model, dest.name
        except Exception as exc:  # noqa: BLE001 — tenta o próximo peso pequeno
            last_error = exc
            print(f"nao_abriu {name}: {exc}")
    raise RuntimeError(f"nenhum modelo pequeno abriu: {last_error}")


def synthetic_frame() -> np.ndarray:
    frame = np.full((480, 640, 3), 32, dtype=np.uint8)
    cv2.rectangle(frame, (80, 60), (280, 360), (180, 180, 180), -1)
    cv2.circle(frame, (450, 220), 80, (200, 200, 200), -1)
    cv2.putText(
        frame,
        "smoke",
        (24, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (240, 240, 240),
        2,
        cv2.LINE_AA,
    )
    return frame


def open_camera() -> cv2.VideoCapture | None:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap.release()
        return None
    ok, frame = cap.read()
    if not ok or frame is None:
        cap.release()
        return None
    return cap


def measure(model: YOLO, frame: np.ndarray, repeats: int = 100) -> float:
    for _ in range(10):
        model.predict(frame, imgsz=640, verbose=False, device=0)
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(repeats):
        model.predict(frame, imgsz=640, verbose=False, device=0)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    return repeats / elapsed


def main() -> int:
    os.environ.setdefault("YOLO_CONFIG_DIR", str(ROOT / "cache" / "ultralytics"))
    MODELS.mkdir(parents=True, exist_ok=True)
    RUNS.mkdir(parents=True, exist_ok=True)
    configure_paths()

    if not torch.cuda.is_available():
        print("cuda_available False")
        return 1

    model, name = load_model()
    print(f"modelo {name}")

    camera = open_camera()
    if camera is None:
        frame = synthetic_frame()
        source = "imagem_sintetica"
    else:
        ok, frame = camera.read()
        camera.release()
        if not ok or frame is None:
            frame = synthetic_frame()
            source = "imagem_sintetica"
        else:
            source = "webcam"
    print(f"fonte {source} shape {frame.shape}")

    fps = measure(model, frame)
    result = model.predict(frame, imgsz=640, verbose=False, device=0)[0]
    annotated = result.plot()
    out = RUNS / "smoke_anotado.jpg"
    cv2.imwrite(str(out), annotated)
    n = 0 if result.boxes is None else len(result.boxes)
    print(f"fps {fps:.1f}")
    print(f"deteccoes {n}")
    print(f"saida {out}")
    print(f"vram_pico_mib {torch.cuda.max_memory_allocated() / 1024 ** 2:.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
