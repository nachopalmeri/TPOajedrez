"""Adaptador de consola: el único lugar que lee del teclado y escribe en pantalla."""
from ..nucleo import MovimientoInvalido, Partida, Posicion


def dibujar(partida: Partida) -> str:
    tablero = partida.tablero
    letras = "abcdefghijklmnopqrstuvwxyz"[:tablero.columnas]
    lineas = []
    for fila in range(tablero.filas - 1, -1, -1):
        casillas = []
        for columna in range(tablero.columnas):
            pieza = tablero.pieza_en(Posicion(fila, columna))
            casillas.append(pieza.simbolo if pieza else ".")
        lineas.append(f"{fila + 1:>2} " + " ".join(casillas))
    lineas.append("   " + " ".join(letras))
    return "\n".join(lineas)


def jugar(entrada=input, salida=print) -> None:
    partida = Partida()
    salida("Ajedrez. Mayúsculas = blancas, minúsculas = negras. Escribí la jugada como 'e2 e4' o 'salir'.")
    while True:
        salida(dibujar(partida))
        if partida.es_jaque_mate():
            salida(f"Jaque mate. Ganan las {partida.turno.opuesto().piezas}.")
            return
        texto = entrada(f"Juegan las {partida.turno.piezas} > ").strip()
        if texto == "salir":
            return
        try:
            partes = texto.split()
            if len(partes) != 2:
                raise ValueError("Escribí dos casillas, por ejemplo 'e2 e4'")
            desde, hasta = Posicion.desde_notacion(partes[0]), Posicion.desde_notacion(partes[1])
            jugada = partida.mover(desde, hasta)
        except (ValueError, MovimientoInvalido) as error:
            salida(f"No se puede: {error}")
            continue
        if jugada.capturada:
            salida(f"Captura: {jugada.capturada.nombre} {jugada.capturada.color.value}.")
        if jugada.da_jaque:
            salida("¡Jaque!")


if __name__ == "__main__":
    jugar()
