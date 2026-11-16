"""Treino curto de viabilidade. Não é o treino final."""

from ultralytics import YOLO


def main() -> None:
    model = YOLO(r"D:\citizentech\cv\models\yolo26n.pt")
    model.train(
        data=r"D:\citizentech\cv\data\processed\libras15_passos\data.yaml",
        epochs=5,
        imgsz=640,
        batch=16,
        cache="ram",
        workers=0,
        amp=True,
        seed=42,
        deterministic=True,
        device=0,
        project=r"D:\citizentech\cv\runs\viabilidade",
        name="yolo26n_e5",
        exist_ok=True,
        pretrained=True,
        patience=20,
        close_mosaic=0,
        plots=True,
        val=True,
        verbose=True,
    )


if __name__ == "__main__":
    main()
