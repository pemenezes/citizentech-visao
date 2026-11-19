"""Máquina da fase. Os tempos são parâmetros, não resultado medido."""

from __future__ import annotations


class Farol:
    def __init__(
        self,
        verde_minimo: float = 5.0,
        via_vazia: float = 3.0,
        espera_maxima: float = 20.0,
    ) -> None:
        self.verde_minimo = verde_minimo
        self.via_vazia = via_vazia
        self.espera_maxima = espera_maxima
        self.fase = "ABRE VIA"
        self.verde = 0.0
        self.vazia = 0.0
        self.espera = 0.0

    def atualizar(
        self,
        pessoas_na_faixa: int,
        veiculos_na_via: int,
        veiculos_na_faixa: int,
        pessoas_esperando: int,
        dt: float,
    ) -> str:
        # Alguém na pintura segura o pedestre e fura o verde mínimo.
        if pessoas_na_faixa > 0:
            self.fase = "PEDESTRE"
            self.verde = 0.0
            self.vazia = 0.0
            return self.fase

        faixa_livre = veiculos_na_faixa == 0
        if self.fase == "ABRE VIA":
            self.verde += dt
            if veiculos_na_via == 0 and faixa_livre:
                self.vazia += dt
            else:
                self.vazia = 0.0
            if pessoas_esperando > 0:
                self.espera += dt
            else:
                self.espera = 0.0
            via_ociosa = self.vazia >= self.via_vazia
            espera_estourou = self.espera >= self.espera_maxima
            if (
                self.verde >= self.verde_minimo
                and faixa_livre
                and pessoas_esperando > 0
                and (via_ociosa or espera_estourou)
            ):
                self.fase = "PEDESTRE"
                self.verde = 0.0
                self.vazia = 0.0
            return self.fase

        self.verde += dt
        if self.verde >= self.verde_minimo and (veiculos_na_via > 0 or pessoas_esperando == 0):
            self.fase = "ABRE VIA"
            self.verde = 0.0
            self.espera = 0.0
        return self.fase
