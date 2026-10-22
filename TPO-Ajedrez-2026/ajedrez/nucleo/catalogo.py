from typing import Callable, Dict, List

from .color import Color
from .movimientos import DIAGONALES, RECTAS, SALTOS_DE_CABALLO, AvancePeon, Deslizante, Salto
from .pieza import Pieza

FabricaDePieza = Callable[[Color], Pieza]


class CatalogoDePiezas:
    """Sabe cómo se arma cada tipo de pieza. Para sumar una pieza nueva se registra acá;
    no hace falta tocar Pieza, Tablero ni Partida."""

    def __init__(self) -> None:
        self._fabricas: Dict[str, FabricaDePieza] = {}

    def registrar(self, nombre: str, fabrica: FabricaDePieza) -> None:
        self._fabricas[nombre] = fabrica

    def crear(self, nombre: str, color: Color) -> Pieza:
        if nombre not in self._fabricas:
            raise KeyError(f"No hay ninguna pieza registrada como {nombre!r}")
        return self._fabricas[nombre](color)

    def nombres(self) -> List[str]:
        return sorted(self._fabricas)


def _simbolo(letra: str, color: Color) -> str:
    return letra.upper() if color is Color.BLANCO else letra.lower()


def catalogo_clasico() -> CatalogoDePiezas:
    catalogo = CatalogoDePiezas()
    catalogo.registrar("peon", lambda c: Pieza("peon", c, (AvancePeon(),), _simbolo("p", c)))
    catalogo.registrar("torre", lambda c: Pieza("torre", c, (Deslizante(RECTAS),), _simbolo("t", c)))
    catalogo.registrar("caballo", lambda c: Pieza("caballo", c, (Salto(SALTOS_DE_CABALLO),), _simbolo("c", c)))
    catalogo.registrar("alfil", lambda c: Pieza("alfil", c, (Deslizante(DIAGONALES),), _simbolo("a", c)))
    catalogo.registrar("reina", lambda c: Pieza("reina", c, (Deslizante(RECTAS + DIAGONALES),), _simbolo("d", c)))
    catalogo.registrar("rey", lambda c: Pieza("rey", c, (Salto(RECTAS + DIAGONALES),), _simbolo("r", c), es_rey=True))
    return catalogo
