"""Converte o conjunto Passos (15 letras) para YOLO e divide por faixa de arquivo.

A divisão é contígua dentro de cada letra (70/20/10), para não misturar fotos
vizinhas. Continua sendo a mesma pessoa e o mesmo fundo: não é teste de campo.
"""

from __future__ import annotations

import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

RAW = Path(r"D:\citizentech\cv\data\raw\bsl-alphabet-passos\dataset")
OUT = Path(r"D:\citizentech\cv\data\processed\libras15_passos")
NAMES = ["a", "b", "c", "d", "e", "i", "l", "m", "n", "o", "r", "s", "u", "v", "w"]
INDEX = {name: i for i, name in enumerate(NAMES)}


def stem_number(path: Path) -> int:
    digits = "".join(ch for ch in path.stem if ch.isdigit())
    return int(digits) if digits else 0


def yolo_line(xml_path: Path) -> str | None:
    root = ET.parse(xml_path).getroot()
    width = int(root.findtext("size/width"))
    height = int(root.findtext("size/height"))
    objects = root.findall("object")
    if len(objects) != 1:
        return None
    name = objects[0].findtext("name").strip().lower()
    if name not in INDEX:
        return None
    box = objects[0].find("bndbox")
    xmin = int(box.findtext("xmin"))
    ymin = int(box.findtext("ymin"))
    xmax = int(box.findtext("xmax"))
    ymax = int(box.findtext("ymax"))
    bw = xmax - xmin
    bh = ymax - ymin
    if bw <= 1 or bh <= 1:
        return None
    xc = (xmin + xmax) / 2 / width
    yc = (ymin + ymax) / 2 / height
    return f"{INDEX[name]} {xc:.6f} {yc:.6f} {bw / width:.6f} {bh / height:.6f}"


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for split in ("train", "val", "test"):
        (OUT / "images" / split).mkdir(parents=True)
        (OUT / "labels" / split).mkdir(parents=True)

    counts = {split: {name: 0 for name in NAMES} for split in ("train", "val", "test")}
    skipped = 0
    for folder in sorted(p for p in RAW.iterdir() if p.is_dir()):
        pairs = []
        for xml_path in folder.glob("*.xml"):
            image = folder / f"{xml_path.stem}.jpg"
            if not image.exists():
                skipped += 1
                continue
            line = yolo_line(xml_path)
            if line is None:
                skipped += 1
                continue
            pairs.append((stem_number(xml_path), image, line))
        pairs.sort()
        n = len(pairs)
        n_train = int(n * 0.70)
        n_val = int(n * 0.20)
        spans = {
            "train": pairs[:n_train],
            "val": pairs[n_train : n_train + n_val],
            "test": pairs[n_train + n_val :],
        }
        for split, items in spans.items():
            for number, image, line in items:
                dest_stem = f"{folder.name}_{number}"
                shutil.copy2(image, OUT / "images" / split / f"{dest_stem}.jpg")
                (OUT / "labels" / split / f"{dest_stem}.txt").write_text(line + "\n", encoding="utf-8")
                counts[split][line[0] and NAMES[int(line.split()[0])]] += 1

    names_yaml = "\n".join(f"  {i}: {name}" for i, name in enumerate(NAMES))
    (OUT / "data.yaml").write_text(
        "\n".join(
            [
                f"path: {OUT.as_posix()}",
                "train: images/train",
                "val: images/val",
                "test: images/test",
                "names:",
                names_yaml,
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"skipped {skipped}")
    for split, per_class in counts.items():
        print(split, sum(per_class.values()), dict(per_class))


if __name__ == "__main__":
    main()
