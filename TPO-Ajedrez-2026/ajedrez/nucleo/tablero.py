from typing import Dict, Iterator, Optional, Tuple

from .color import Color
from .pieza import Pieza
from .posicion import Posicion


class Tablero:
    """Guarda qué pieza hay en cada casilla. No sabe nada de reglas ni de turnos."""

    def __init__(self, filas: int = 8, columnas: int = 8):
        if filas < 1 or columnas < 1:
            raise ValueError("El tablero necesita al menos una fila y una columna")
        self.filas = filas
        self.columnas = columnas
        self._casillas: Dict[Posicion, Pieza] = {}

    def dentro(self, pos: Posicion) -> bool:
        return 0 <= pos.fila < self.filas and 0 <= pos.columna < self.columnas

    def pieza_en(self, pos: Posicion) -> Optional[Pieza]:
        return self._casillas.get(pos)

    def esta_vacia(self, pos: Posicion) -> bool:
        return pos not in self._casillas

    def colocar(self, pieza: Pieza, pos: Posicion) -> None:
        if not self.dentro(pos):
            raise ValueError(f"{pos} está fuera del tablero")
        self._casillas[pos] = pieza

    def quitar(self, pos: Posicion) -> Optional[Pieza]:
        return self._casillas.pop(pos, None)

    def mover(self, desde: Posicion, hasta: Posicion) -> Optional[Pieza]:
        """Mueve la pieza y devuelve la que estaba en el destino (la capturada), si había."""
        pieza = self.quitar(desde)
        if pieza is None:
            raise ValueError(f"No hay ninguna pieza en {desde}")
        capturada = self.quitar(hasta)
        self.colocar(pieza, hasta)
        return capturada

    def piezas(self, color: Optional[Color] = None) -> Iterator[Tuple[Posicion, Pieza]]:
        for pos, pieza in list(self._casillas.items()):
            if color is None or pieza.color is color:
                yield pos, pieza

    def posicion_del_rey(self, color: Color) -> Optional[Posicion]:
        for pos, pieza in self.piezas(color):
            if pieza.es_rey:
                return pos
        return None

    def copia(self) -> "Tablero":
        otro = Tablero(self.filas, self.columnas)
        otro._casillas = dict(self._casillas)
        return otro
