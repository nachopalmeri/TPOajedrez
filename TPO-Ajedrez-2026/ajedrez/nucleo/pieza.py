from dataclasses import dataclass
from typing import TYPE_CHECKING, Set, Tuple

from .color import Color
from .posicion import Posicion

if TYPE_CHECKING:
    from .movimientos import ReglaDeMovimiento
    from .tablero import Tablero


@dataclass(frozen=True)
class Pieza:
    """Una pieza no hereda de nada: su comportamiento son las reglas de movimiento que se le componen."""
    nombre: str
    color: Color
    reglas: Tuple["ReglaDeMovimiento", ...]
    simbolo: str
    es_rey: bool = False

    def destinos(self, tablero: "Tablero", desde: Posicion) -> Set[Posicion]:
        """Casillas a las que puede ir según sus propias reglas (sin mirar el jaque)."""
        resultado: Set[Posicion] = set()
        for regla in self.reglas:
            resultado |= regla.destinos(tablero, desde, self.color)
        return resultado

    def ataques(self, tablero: "Tablero", desde: Posicion) -> Set[Posicion]:
        """Casillas que amenaza. Casi siempre coinciden con los destinos; el peón es la excepción."""
        resultado: Set[Posicion] = set()
        for regla in self.reglas:
            resultado |= regla.ataques(tablero, desde, self.color)
        return resultado
