"""Treino do YOLO26n nas 15 letras públicas. Ajuste épocas pela linha de comando."""

import argparse

from ultralytics import YOLO


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--name", default="yolo26n_e5")
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--modelo", default=r"D:\citizentech\cv\models\yolo26n.pt")
    parser.add_argument("--batch", type=int, default=16)
    args = parser.parse_args()

    model = YOLO(args.modelo)
    model.train(
        data=r"D:\citizentech\cv\data\processed\libras15_passos\data.yaml",
        epochs=args.epochs,
        imgsz=640,
        batch=args.batch,
        cache="ram",
        workers=0,
        amp=True,
        seed=42,
        deterministic=True,
        device=0,
        project=r"D:\citizentech\cv\runs",
        name=args.name,
        exist_ok=True,
        pretrained=True,
        patience=args.patience,
        close_mosaic=10,
        plots=True,
        val=True,
        verbose=True,
    )


if __name__ == "__main__":
    main()
