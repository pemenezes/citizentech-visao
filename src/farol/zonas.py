"""Regiões do clipe da faixa, em pixels de 720×1280.

A faixa de pedestre fica entre y=880 e y=1040. A via é a fila de
carros parada imediatamente antes da zebra. As duas calçadas são
onde a pessoa espera, ainda fora da pintura. Este enquadramento não
mostra uma segunda via.
"""

from __future__ import annotations

import cv2
import numpy as np

FAIXA = np.array([[0, 880], [720, 880], [720, 1040], [0, 1040]], dtype=np.int32)
VIA = np.array([[80, 700], [640, 700], [700, 880], [20, 880]], dtype=np.int32)
ESPERA = (
    np.array([[0, 760], [140, 760], [100, 880], [0, 880]], dtype=np.int32),
    np.array([[580, 760], [720, 760], [720, 880], [620, 880]], dtype=np.int32),
)

# Clipe de 21 s, 1280×720. A zebra está vazia e os carros passam por ela.
# A fila de pessoas espera na calçada, acima da pintura.
FAIXA_ESPERA = np.array([[160, 640], [1200, 640], [1200, 720], [160, 720]], dtype=np.int32)
VIA_ESPERA = np.array([[0, 400], [1280, 360], [1280, 640], [0, 640]], dtype=np.int32)
ESPERA_ESPERA = (
    np.array([[220, 430], [1040, 430], [1080, 630], [180, 630]], dtype=np.int32),
)

# Clipe de 84 s, 960×540, câmera parada num cruzamento.
# A zebra da frente ocupa a metade de baixo. A de trás fica à esquerda.
FAIXA_TRANSITO = np.array(
    [[0, 250], [500, 250], [560, 320], [960, 330], [960, 540], [0, 540]],
    dtype=np.int32,
)
VIA_TRANSITO = np.array(
    [[520, 230], [960, 210], [960, 330], [620, 340]],
    dtype=np.int32,
)
ESPERA_TRANSITO = (
    np.array([[0, 180], [200, 180], [220, 250], [0, 270]], dtype=np.int32),
)

# Clipe de 55 s, 1366×720. Câmera parada, uma zebra grande na frente.
# A via é a fila à direita, fora da pintura. As calçadas ficam acima e abaixo.
FAIXA_ESQUINA = np.array(
    [[0, 385], [1040, 350], [1120, 530], [740, 660], [0, 655]],
    dtype=np.int32,
)
VIA_ESQUINA = np.array(
    [[980, 320], [1366, 300], [1366, 490], [1120, 530], [1040, 390]],
    dtype=np.int32,
)
ESPERA_ESQUINA = (
    np.array([[0, 670], [820, 675], [1366, 620], [1366, 720], [0, 720]], dtype=np.int32),
    np.array([[0, 220], [1100, 200], [1240, 330], [0, 340]], dtype=np.int32),
    np.array([[1140, 500], [1366, 470], [1366, 640], [1160, 660]], dtype=np.int32),
)

# Clipe de 26 s, 960×540, câmera parada. As pessoas atravessam no começo
# e a faixa fica vazia enquanto os carros passam.
FAIXA_LONDRES = np.array(
    [[40, 350], [760, 330], [800, 460], [20, 480]],
    dtype=np.int32,
)
VIA_LONDRES = np.array([[0, 430], [960, 400], [960, 540], [0, 540]], dtype=np.int32)
ESPERA_LONDRES = (
    np.array([[0, 380], [140, 350], [100, 520], [0, 530]], dtype=np.int32),
)

CENAS = {
    "faixa": {"tamanho": (720, 1280), "faixa": FAIXA, "via": VIA, "espera": ESPERA},
    "espera": {
        "tamanho": (1280, 720),
        "faixa": FAIXA_ESPERA,
        "via": VIA_ESPERA,
        "espera": ESPERA_ESPERA,
    },
    "transito": {
        "tamanho": (960, 540),
        "faixa": FAIXA_TRANSITO,
        "via": VIA_TRANSITO,
        "espera": ESPERA_TRANSITO,
    },
    "esquina": {
        "tamanho": (1366, 720),
        "faixa": FAIXA_ESQUINA,
        "via": VIA_ESQUINA,
        "espera": ESPERA_ESQUINA,
    },
    "londres": {
        "tamanho": (960, 540),
        "faixa": FAIXA_LONDRES,
        "via": VIA_LONDRES,
        "espera": ESPERA_LONDRES,
    },
}

VEICULOS = {"car", "motorcycle", "bus", "truck"}


def contem(zona: np.ndarray, ponto: tuple[float, float]) -> bool:
    return cv2.pointPolygonTest(zona, ponto, False) >= 0


def dentro_de_alguma(zonas: tuple[np.ndarray, ...], ponto: tuple[float, float]) -> bool:
    return any(contem(zona, ponto) for zona in zonas)
