from dataclasses import dataclass

COLUMNAS = "abcdefghijklmnopqrstuvwxyz"


@dataclass(frozen=True)
class Posicion:
    """Casilla del tablero. fila 0 es la primera fila de las blancas."""
    fila: int
    columna: int

    def desplazar(self, d_fila: int, d_columna: int) -> "Posicion":
        return Posicion(self.fila + d_fila, self.columna + d_columna)

    @staticmethod
    def desde_notacion(texto: str) -> "Posicion":
        """'e2' -> Posicion(1, 4). Sirve para tableros de hasta 26 columnas."""
        texto = texto.strip().lower()
        if len(texto) < 2 or texto[0] not in COLUMNAS or not texto[1:].isdigit():
            raise ValueError(f"Casilla inválida: {texto!r}")
        return Posicion(int(texto[1:]) - 1, COLUMNAS.index(texto[0]))

    def notacion(self) -> str:
        return f"{COLUMNAS[self.columna]}{self.fila + 1}"

    def __str__(self) -> str:
        return self.notacion()
