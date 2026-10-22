from dataclasses import dataclass
from typing import List, Optional, Set

from .catalogo import CatalogoDePiezas, catalogo_clasico
from .color import Color
from .disposicion import Disposicion, DisposicionClasica
from .excepciones import MovimientoInvalido
from .pieza import Pieza
from .posicion import Posicion
from .tablero import Tablero


@dataclass(frozen=True)
class Jugada:
    pieza: Pieza
    desde: Posicion
    hasta: Posicion
    capturada: Optional[Pieza]
    da_jaque: bool


class Partida:
    """Reglas del juego: turnos, validación, captura y jaque. No imprime ni lee nada."""

    def __init__(self, disposicion: Optional[Disposicion] = None,
                 catalogo: Optional[CatalogoDePiezas] = None,
                 empieza: Color = Color.BLANCO):
        self.catalogo = catalogo or catalogo_clasico()
        self.tablero: Tablero = (disposicion or DisposicionClasica()).armar(self.catalogo)
        self.turno = empieza
        self.historial: List[Jugada] = []

    # ---------- consultas ----------

    def esta_en_jaque(self, color: Color, tablero: Optional[Tablero] = None) -> bool:
        tablero = tablero or self.tablero
        rey = tablero.posicion_del_rey(color)
        if rey is None:
            return False
        return any(rey in pieza.ataques(tablero, pos) for pos, pieza in tablero.piezas(color.opuesto()))

    def movimientos_legales(self, desde: Posicion) -> Set[Posicion]:
        pieza = self.tablero.pieza_en(desde)
        if pieza is None or pieza.color is not self.turno:
            return set()
        return {hasta for hasta in pieza.destinos(self.tablero, desde)
                if not self._captura_rey_rival(hasta, pieza.color)
                and not self._deja_en_jaque(desde, hasta, pieza.color)}

    def tiene_movimientos(self, color: Color) -> bool:
        for pos, pieza in self.tablero.piezas(color):
            for hasta in pieza.destinos(self.tablero, pos):
                if (not self._captura_rey_rival(hasta, color)
                        and not self._deja_en_jaque(pos, hasta, color)):
                    return True
        return False

    def es_jaque_mate(self) -> bool:
        return self.esta_en_jaque(self.turno) and not self.tiene_movimientos(self.turno)

    # ---------- acciones ----------

    def mover(self, desde: Posicion, hasta: Posicion) -> Jugada:
        pieza = self.tablero.pieza_en(desde)
        if pieza is None:
            raise MovimientoInvalido(f"No hay ninguna pieza en {desde}")
        if pieza.color is not self.turno:
            raise MovimientoInvalido(f"Le toca mover a las {self.turno.piezas}")
        if hasta not in pieza.destinos(self.tablero, desde):
            raise MovimientoInvalido(f"El {pieza.nombre} no puede ir de {desde} a {hasta}")
        if self._captura_rey_rival(hasta, pieza.color):
            raise MovimientoInvalido("El rey no se captura; la partida termina con jaque mate")
        if self._deja_en_jaque(desde, hasta, pieza.color):
            raise MovimientoInvalido("Ese movimiento deja a tu rey en jaque")

        capturada = self.tablero.mover(desde, hasta)
        self.turno = self.turno.opuesto()
        jugada = Jugada(pieza, desde, hasta, capturada, self.esta_en_jaque(self.turno))
        self.historial.append(jugada)
        return jugada

    # ---------- interno ----------

    def _captura_rey_rival(self, hasta: Posicion, color: Color) -> bool:
        objetivo = self.tablero.pieza_en(hasta)
        return objetivo is not None and objetivo.es_rey and objetivo.color is not color

    def _deja_en_jaque(self, desde: Posicion, hasta: Posicion, color: Color) -> bool:
        prueba = self.tablero.copia()
        prueba.mover(desde, hasta)
        return self.esta_en_jaque(color, prueba)
