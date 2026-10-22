from abc import ABC, abstractmethod

from .catalogo import CatalogoDePiezas
from .color import Color
from .posicion import Posicion
from .tablero import Tablero

FILA_TRASERA = ("torre", "caballo", "alfil", "reina", "rey", "alfil", "caballo", "torre")


class Disposicion(ABC):
    """Decide qué piezas hay al empezar y dónde van."""

    @abstractmethod
    def armar(self, catalogo: CatalogoDePiezas) -> Tablero:
        ...


class DisposicionClasica(Disposicion):
    def armar(self, catalogo: CatalogoDePiezas) -> Tablero:
        tablero = Tablero(8, 8)
        for columna, nombre in enumerate(FILA_TRASERA):
            tablero.colocar(catalogo.crear(nombre, Color.BLANCO), Posicion(0, columna))
            tablero.colocar(catalogo.crear("peon", Color.BLANCO), Posicion(1, columna))
            tablero.colocar(catalogo.crear("peon", Color.NEGRO), Posicion(6, columna))
            tablero.colocar(catalogo.crear(nombre, Color.NEGRO), Posicion(7, columna))
        return tablero


class DisposicionLibre(Disposicion):
    """Tablero de cualquier tamaño con las piezas que se indiquen. Sirve para tests y variantes."""

    def __init__(self, filas: int, columnas: int, piezas):
        # piezas: lista de (nombre, color, "e2")
        self.filas = filas
        self.columnas = columnas
        self.piezas = list(piezas)

    def armar(self, catalogo: CatalogoDePiezas) -> Tablero:
        tablero = Tablero(self.filas, self.columnas)
        for nombre, color, casilla in self.piezas:
            tablero.colocar(catalogo.crear(nombre, color), Posicion.desde_notacion(casilla))
        return tablero
