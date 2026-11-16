"""Mede o YOLO26n pré-treinado no COCO, sem treino nas letras, no mesmo teste."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from ultralytics import YOLO

PESOS = Path(r"D:\citizentech\cv\models\yolo26n.pt")
TESTE = Path(r"D:\citizentech\cv\data\processed\libras15_passos\images\test")
SAIDA = Path(r"D:\citizentech\cv\runs\baseline_coco")


def letra_de(caminho: Path) -> str:
    return caminho.stem.split("_", 1)[0].lower()


def main() -> None:
    SAIDA.mkdir(parents=True, exist_ok=True)
    modelo = YOLO(str(PESOS))
    fotos = sorted(TESTE.glob("*.jpg"))
    acertos = 0
    com_caixa = 0
    classes_vistas = Counter()
    por_letra = Counter()
    for foto in fotos:
        letra = letra_de(foto)
        por_letra[letra] += 1
        resultado = modelo.predict(str(foto), imgsz=640, conf=0.25, device=0, verbose=False)[0]
        nomes = []
        if resultado.boxes is not None:
            nomes = [resultado.names[int(c)] for c in resultado.boxes.cls]
        if nomes:
            com_caixa += 1
            classes_vistas.update(nomes)
        if letra in nomes:
            acertos += 1
    resumo = {
        "pesos": str(PESOS),
        "fotos": len(fotos),
        "com_caixa": com_caixa,
        "acerto_nome_da_letra": acertos,
        "classes_coco_mais_comuns": classes_vistas.most_common(8),
        "fotos_por_letra": dict(por_letra),
    }
    (SAIDA / "resumo.json").write_text(json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(resumo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
