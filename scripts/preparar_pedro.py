"""Organiza os vídeos do Pedro e monta o dataset com amostra pequena.

A letra vem do nome do arquivo. A caixa vem da pele contra a parede branca,
porque o detector treinado nas fotos públicas erra o enquadramento do celular.
O começo de cada clipe, com a mão ainda aberta, fica de fora.
O teste é um trecho contíguo posterior, nunca um quadro sorteado.
g e h são copiados, mas não entram neste treino.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path

import cv2
import numpy as np

ORIGEM = Path(r"C:\Users\pepom\Downloads")
VIDEOS = Path(r"D:\citizentech\cv\video\pedro")
PUBLICO = Path(r"D:\citizentech\cv\data\processed\libras15_passos")
SAIDA = Path(r"D:\citizentech\cv\data\processed\libras16_pedro")
REVISAO = VIDEOS / "_revisao"

NOMES = ["a", "b", "c", "d", "e", "i", "l", "m", "n", "o", "r", "s", "u", "v", "w", "f"]

COPIAS = [
    ("a.mov", "a.mov"),
    ("b.mov", "b.mov"),
    ("c.mov", "c_1.mov"),
    ("c (2).mov", "c_2.mov"),
    ("e.mov", "e.mov"),
    ("d.mov", "d.mov"),
    ("f.mov", "f.mov"),
    ("g.mov", "g_1.mov"),
    ("g2.mov", "g_2.mov"),
    ("h.mov", "h.mov"),
    ("i.mov", "i.mov"),
    ("l.mov", "l.mov"),
    ("m.mov", "m.mov"),
    ("n.mov", "n.mov"),
    ("o.mov", "o.mov"),
    ("r.mov", "r.mov"),
    ("s.mov", "s.mov"),
    ("u.mov", "u.mov"),
    ("v.mov", "v.mov"),
    ("w.mov", "w.mov"),
]

# inicio: fração em que a letra já está estável, vista quadro a quadro.
# papel: dividir = começo estável no treino e fim no teste, com folga no meio.
# c_1 treina e c_2 testa, porque são duas tomadas.
VIDEOS_TREINO = {
    "a.mov": ("a", 0.50, "dividir"),
    "b.mov": ("b", 0.50, "dividir"),
    "c_1.mov": ("c", 0.48, "treino"),
    "c_2.mov": ("c", 0.45, "teste"),
    "d.mov": ("d", 0.55, "dividir"),
    "e.mov": ("e", 0.50, "dividir"),
    "f.mov": ("f", 0.50, "dividir"),
    "i.mov": ("i", 0.55, "dividir"),
    "l.mov": ("l", 0.00, "dividir"),
    "m.mov": ("m", 0.55, "dividir"),
    "n.mov": ("n", 0.70, "dividir"),
    "o.mov": ("o", 0.50, "dividir"),
    "r.mov": ("r", 0.60, "dividir"),
    "s.mov": ("s", 0.70, "dividir"),
    "u.mov": ("u", 0.62, "dividir"),
    "v.mov": ("v", 0.40, "dividir"),
    "w.mov": ("w", 0.40, "dividir"),
}


def caixa_mao(frame: np.ndarray) -> tuple[int, int, int, int] | None:
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    baixa = cv2.inRange(hsv, (0, 30, 60), (25, 190, 255))
    alta = cv2.inRange(hsv, (160, 30, 60), (180, 190, 255))
    mascara = cv2.bitwise_or(baixa, alta)
    nucleo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, nucleo)
    mascara = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, nucleo)
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return None
    contorno = max(contornos, key=cv2.contourArea)
    if cv2.contourArea(contorno) < 0.015 * frame.shape[0] * frame.shape[1]:
        return None
    x, y, w, h = cv2.boundingRect(contorno)
    altura, largura = frame.shape[:2]
    margem_x = int(0.04 * w)
    margem_y = int(0.04 * h)
    x1 = max(0, x - margem_x)
    y1 = max(0, y - margem_y)
    x2 = min(largura - 1, x + w + margem_x)
    y2 = min(altura - 1, y + h + margem_y)
    if (x2 - x1) * (y2 - y1) > 0.85 * largura * altura:
        return None
    return x1, y1, x2, y2


def linha_yolo(caixa: tuple[int, int, int, int], largura: int, altura: int, classe: int) -> str:
    x1, y1, x2, y2 = caixa
    return (
        f"{classe} {(x1 + x2) / 2 / largura:.6f} {(y1 + y2) / 2 / altura:.6f} "
        f"{(x2 - x1) / largura:.6f} {(y2 - y1) / altura:.6f}"
    )


def quadros_estaveis(total: int, inicio: float) -> list[int]:
    começo = int(total * inicio)
    fim = max(começo + 1, total - 2)
    return list(range(começo, fim))


def escolher(indices: list[int], papel: str) -> dict[str, list[int]]:
    if not indices:
        return {"train": [], "teste_pedro": []}
    passo = 1 if len(indices) < 18 else 2 if len(indices) < 40 else 4
    if papel == "treino":
        amostra = indices[::passo][-18:]
        return {"train": amostra, "teste_pedro": []}
    if papel == "teste":
        amostra = indices[::passo][:40]
        return {"train": [], "teste_pedro": amostra}
    corte_treino = max(1, int(len(indices) * 0.40))
    corte_teste = min(len(indices) - 1, int(len(indices) * 0.55))
    treino = indices[:corte_treino][::passo][:18]
    teste = indices[corte_teste:][::passo][:40]
    return {"train": treino, "teste_pedro": teste}


def copiar_videos() -> None:
    VIDEOS.mkdir(parents=True, exist_ok=True)
    for origem_nome, destino_nome in COPIAS:
        origem = ORIGEM / origem_nome
        destino = VIDEOS / destino_nome
        if not origem.exists():
            if not destino.exists():
                raise FileNotFoundError(origem)
            continue
        shutil.copy2(origem, destino)


def limpar_pedro() -> None:
    for pasta in ("images", "labels"):
        for divisao in ("train", "teste_pedro"):
            alvo = SAIDA / pasta / divisao
            if not alvo.exists():
                continue
            for arquivo in alvo.glob("pedro_*"):
                arquivo.unlink()


def ligar_publico() -> None:
    for divisao in ("train", "val", "test"):
        for pasta in ("images", "labels"):
            origem = PUBLICO / pasta / divisao
            destino = SAIDA / pasta / divisao
            destino.mkdir(parents=True, exist_ok=True)
            for arquivo in origem.iterdir():
                if not arquivo.is_file():
                    continue
                ponte = destino / arquivo.name
                if ponte.exists():
                    continue
                ponte.hardlink_to(arquivo)


def escrever_yaml() -> None:
    linhas = ["path: D:/citizentech/cv/data/processed/libras16_pedro", "train: images/train", "val: images/val", "test: images/test", "names:"]
    linhas += [f"  {indice}: {nome}" for indice, nome in enumerate(NOMES)]
    (SAIDA / "data.yaml").write_text("\n".join(linhas) + "\n", encoding="utf-8")
    teste = [
        "path: D:/citizentech/cv/data/processed/libras16_pedro",
        "train: images/teste_pedro",
        "val: images/teste_pedro",
        "names:",
    ]
    teste += [f"  {indice}: {nome}" for indice, nome in enumerate(NOMES)]
    (SAIDA / "data_teste_pedro.yaml").write_text("\n".join(teste) + "\n", encoding="utf-8")


def gravar_quadro(
    frame: np.ndarray,
    caixa: tuple[int, int, int, int],
    letra: str,
    indice: int,
    divisao: str,
    video: str,
) -> str:
    nome = f"pedro_{letra}_{Path(video).stem}_{indice:06d}"
    imagem = SAIDA / "images" / divisao / f"{nome}.jpg"
    rotulo = SAIDA / "labels" / divisao / f"{nome}.txt"
    imagem.parent.mkdir(parents=True, exist_ok=True)
    rotulo.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(imagem), frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    altura, largura = frame.shape[:2]
    rotulo.write_text(linha_yolo(caixa, largura, altura, NOMES.index(letra)) + "\n", encoding="utf-8")
    return nome


def main() -> None:
    copiar_videos()
    limpar_pedro()
    ligar_publico()
    escrever_yaml()
    REVISAO.mkdir(parents=True, exist_ok=True)
    for antigo in REVISAO.glob("*.jpg"):
        antigo.unlink()

    manifestos: list[dict[str, str]] = []
    sem_caixa = 0
    for video, (letra, inicio, papel) in VIDEOS_TREINO.items():
        captura = cv2.VideoCapture(str(VIDEOS / video))
        if not captura.isOpened():
            raise RuntimeError(f"não abriu {video}")
        total = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
        grupos = escolher(quadros_estaveis(total, inicio), papel)
        vistos: set[str] = set()
        for divisao, indices in grupos.items():
            for indice in indices:
                captura.set(cv2.CAP_PROP_POS_FRAMES, indice)
                ok, frame = captura.read()
                if not ok or frame is None:
                    continue
                caixa = caixa_mao(frame)
                if caixa is None:
                    sem_caixa += 1
                    continue
                nome = gravar_quadro(frame, caixa, letra, indice, divisao, video)
                manifestos.append(
                    {"arquivo": nome, "letra": letra, "divisao": divisao, "video": video, "quadro": str(indice)}
                )
                if divisao not in vistos:
                    x1, y1, x2, y2 = caixa
                    desenhado = frame.copy()
                    cv2.rectangle(desenhado, (x1, y1), (x2, y2), (0, 180, 0), 3)
                    cv2.imwrite(
                        str(REVISAO / f"{divisao}_{letra}.jpg"),
                        desenhado,
                        [int(cv2.IMWRITE_JPEG_QUALITY), 80],
                    )
                    vistos.add(divisao)
        captura.release()
        print(
            f"{video} {letra} treino {len(grupos['train'])} teste {len(grupos['teste_pedro'])}"
        )

    with (SAIDA / "manifesto_pedro.csv").open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, ["arquivo", "letra", "divisao", "video", "quadro"])
        escritor.writeheader()
        escritor.writerows(manifestos)
    print(f"gravados {len(manifestos)}")
    print(f"sem_caixa {sem_caixa}")
    print("fora deste treino: g_1.mov g_2.mov h.mov")


if __name__ == "__main__":
    main()
