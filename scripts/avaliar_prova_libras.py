"""Avalia o treino curto no teste separado e mede FPS em lote 1."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from ultralytics import YOLO

WEIGHTS = Path(r"D:\citizentech\cv\runs\viabilidade\yolo26n_e5\weights\best.pt")
DATA = Path(r"D:\citizentech\cv\data\processed\libras15_passos\data.yaml")
TEST_IMAGES = Path(r"D:\citizentech\cv\data\processed\libras15_passos\images\test")


def main() -> None:
    model = YOLO(str(WEIGHTS))
    metrics = model.val(
        data=str(DATA),
        split="test",
        imgsz=640,
        batch=16,
        device=0,
        workers=0,
        plots=True,
        project=r"D:\citizentech\cv\runs\viabilidade",
        name="yolo26n_e5_teste",
        exist_ok=True,
    )
    names = metrics.names
    print(f"test_map50 {metrics.box.map50:.4f}")
    print(f"test_map50_95 {metrics.box.map:.4f}")
    print(f"test_precision {metrics.box.mp:.4f}")
    print(f"test_recall {metrics.box.mr:.4f}")
    for index, name in names.items():
        ap50 = float(metrics.box.ap50[index])
        precision = float(metrics.box.p[index])
        recall = float(metrics.box.r[index])
        print(f"classe {name} P {precision:.3f} R {recall:.3f} AP50 {ap50:.3f}")

    images = sorted(TEST_IMAGES.glob("*.jpg"))[:100]
    for image in images[:10]:
        model.predict(str(image), imgsz=640, device=0, verbose=False)
    torch.cuda.synchronize()
    start = time.perf_counter()
    for image in images:
        model.predict(str(image), imgsz=640, device=0, verbose=False)
    torch.cuda.synchronize()
    elapsed = time.perf_counter() - start
    print(f"fps_lote1 {len(images) / elapsed:.1f}")
    print(f"latencia_ms {1000 * elapsed / len(images):.1f}")
    print(f"vram_pico_mib {torch.cuda.max_memory_allocated() / 1024 ** 2:.0f}")


if __name__ == "__main__":
    main()
