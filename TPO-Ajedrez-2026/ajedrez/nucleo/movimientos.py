from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Iterable, Set, Tuple

from .color import Color
from .posicion import Posicion

if TYPE_CHECKING:
    from .tablero import Tablero

Direccion = Tuple[int, int]

RECTAS: Tuple[Direccion, ...] = ((1, 0), (-1, 0), (0, 1), (0, -1))
DIAGONALES: Tuple[Direccion, ...] = ((1, 1), (1, -1), (-1, 1), (-1, -1))
SALTOS_DE_CABALLO: Tuple[Direccion, ...] = ((2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2))


class ReglaDeMovimiento(ABC):
    """Una forma de moverse. Las piezas se arman combinando reglas."""

    @abstractmethod
    def destinos(self, tablero: "Tablero", desde: Posicion, color: Color) -> Set[Posicion]:
        ...

    def ataques(self, tablero: "Tablero", desde: Posicion, color: Color) -> Set[Posicion]:
        return self.destinos(tablero, desde, color)


def _libre_o_rival(tablero: "Tablero", pos: Posicion, color: Color) -> bool:
    pieza = tablero.pieza_en(pos)
    return pieza is None or pieza.color is not color


class Deslizante(ReglaDeMovimiento):
    """Avanza en línea recta hasta chocar: torre, alfil y reina."""

    def __init__(self, direcciones: Iterable[Direccion]):
        self.direcciones = tuple(direcciones)

    def destinos(self, tablero, desde, color):
        resultado = set()
        for d_fila, d_columna in self.direcciones:
            actual = desde.desplazar(d_fila, d_columna)
            while tablero.dentro(actual):
                pieza = tablero.pieza_en(actual)
                if pieza is None:
                    resultado.add(actual)
                else:
                    if pieza.color is not color:
                        resultado.add(actual)
                    break
                actual = actual.desplazar(d_fila, d_columna)
        return resultado


class Salto(ReglaDeMovimiento):
    """Va directo a casillas fijas sin importar lo que haya en el medio: caballo y rey."""

    def __init__(self, saltos: Iterable[Direccion]):
        self.saltos = tuple(saltos)

    def destinos(self, tablero, desde, color):
        resultado = set()
        for d_fila, d_columna in self.saltos:
            destino = desde.desplazar(d_fila, d_columna)
            if tablero.dentro(destino) and _libre_o_rival(tablero, destino, color):
                resultado.add(destino)
        return resultado


class AvancePeon(ReglaDeMovimiento):
    """Avanza sin capturar, captura en diagonal y puede avanzar dos desde su fila de salida."""

    def __init__(self, fila_inicial_blanco: int = 1, fila_inicial_negro: int = -2):
        # fila_inicial_negro negativa cuenta desde el final, así sirve para cualquier tamaño de tablero
        self.fila_inicial_blanco = fila_inicial_blanco
        self.fila_inicial_negro = fila_inicial_negro

    @staticmethod
    def _sentido(color: Color) -> int:
        return 1 if color is Color.BLANCO else -1

    def _fila_inicial(self, tablero, color: Color) -> int:
        if color is Color.BLANCO:
            return self.fila_inicial_blanco
        return self.fila_inicial_negro % tablero.filas

    def destinos(self, tablero, desde, color):
        resultado = set()
        paso = self._sentido(color)
        uno = desde.desplazar(paso, 0)
        if tablero.dentro(uno) and tablero.esta_vacia(uno):
            resultado.add(uno)
            dos = desde.desplazar(2 * paso, 0)
            if desde.fila == self._fila_inicial(tablero, color) and tablero.dentro(dos) and tablero.esta_vacia(dos):
                resultado.add(dos)
        for destino in self.ataques(tablero, desde, color):
            pieza = tablero.pieza_en(destino)
            if pieza is not None and pieza.color is not color:
                resultado.add(destino)
        return resultado

    def ataques(self, tablero, desde, color):
        paso = self._sentido(color)
        diagonales = (desde.desplazar(paso, -1), desde.desplazar(paso, 1))
        return {pos for pos in diagonales if tablero.dentro(pos)}
