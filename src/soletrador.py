"""Aceita uma letra só depois de vários quadros estáveis."""

from __future__ import annotations

from collections import Counter, deque


class Soletrador:
    def __init__(self, janela: int = 12, minimo: int = 8, limiar: float = 0.60) -> None:
        if minimo > janela:
            raise ValueError("minimo não pode ser maior que a janela")
        self.janela_tamanho = janela
        self.minimo = minimo
        self.limiar = limiar
        self.quadros: deque[str | None] = deque(maxlen=janela)
        self.texto = ""
        self._letra_travada: str | None = None

    def observar(self, classe: str | None, confianca: float) -> str | None:
        token = classe if classe and confianca >= self.limiar else None
        self.quadros.append(token)
        if token is None:
            vazios = sum(item is None for item in self.quadros)
            if vazios >= self.minimo:
                self._letra_travada = None
            return None
        votos = sum(item == token for item in self.quadros)
        if votos >= self.minimo and self._letra_travada != token:
            self.texto += token
            self._letra_travada = token
            return token
        return None

    def letra_atual(self) -> str | None:
        presentes = [item for item in self.quadros if item is not None]
        if not presentes:
            return None
        letra, quantidade = Counter(presentes).most_common(1)[0]
        if quantidade >= max(1, self.minimo // 2):
            return letra
        return None

    def espaco(self) -> None:
        self.texto += " "
        self._letra_travada = None
        self.quadros.clear()

    def apagar(self) -> None:
        self.texto = self.texto[:-1]
        self._letra_travada = None
        self.quadros.clear()

    def limpar(self) -> None:
        self.texto = ""
        self._letra_travada = None
        self.quadros.clear()
