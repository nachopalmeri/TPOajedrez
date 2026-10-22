"""Tests del núcleo. Corren sin ninguna infraestructura: python -m unittest -v"""
import unittest

from ajedrez.nucleo import (Color, DisposicionLibre, MovimientoInvalido, Partida, Pieza, Posicion,
                            Salto, Deslizante, catalogo_clasico)
from ajedrez.nucleo.movimientos import RECTAS, SALTOS_DE_CABALLO

B, N = Color.BLANCO, Color.NEGRO


def p(casilla):
    return Posicion.desde_notacion(casilla)


def casillas(*nombres):
    return {p(n) for n in nombres}


def partida_con(piezas, filas=8, columnas=8, empieza=B, catalogo=None):
    return Partida(DisposicionLibre(filas, columnas, piezas), catalogo=catalogo, empieza=empieza)


class TestPosicion(unittest.TestCase):
    def test_notacion_ida_y_vuelta(self):
        self.assertEqual(p("e2"), Posicion(1, 4))
        self.assertEqual(Posicion(7, 0).notacion(), "a8")

    def test_notacion_invalida(self):
        with self.assertRaises(ValueError):
            p("z")


class TestTableroInicial(unittest.TestCase):
    def test_tablero_8x8_con_32_piezas(self):
        partida = Partida()
        self.assertEqual((partida.tablero.filas, partida.tablero.columnas), (8, 8))
        self.assertEqual(len(list(partida.tablero.piezas())), 32)

    def test_reyes_en_su_lugar(self):
        partida = Partida()
        self.assertEqual(partida.tablero.pieza_en(p("e1")).nombre, "rey")
        self.assertEqual(partida.tablero.pieza_en(p("e8")).nombre, "rey")

    def test_empiezan_las_blancas(self):
        self.assertIs(Partida().turno, B)


class TestMovimientoDeCadaPieza(unittest.TestCase):
    def test_peon_avanza_uno_o_dos_desde_su_fila(self):
        partida = partida_con([("peon", B, "e2"), ("rey", B, "a1"), ("rey", N, "a8")])
        self.assertEqual(partida.movimientos_legales(p("e2")), casillas("e3", "e4"))

    def test_peon_fuera_de_su_fila_avanza_uno(self):
        partida = partida_con([("peon", B, "e3"), ("rey", B, "a1"), ("rey", N, "a8")])
        self.assertEqual(partida.movimientos_legales(p("e3")), casillas("e4"))

    def test_peon_bloqueado_no_avanza(self):
        partida = partida_con([("peon", B, "e2"), ("caballo", N, "e3"), ("rey", B, "a1"), ("rey", N, "a8")])
        self.assertEqual(partida.movimientos_legales(p("e2")), set())

    def test_peon_captura_en_diagonal(self):
        partida = partida_con([("peon", B, "e4"), ("torre", N, "d5"), ("rey", B, "a1"), ("rey", N, "a8")])
        self.assertEqual(partida.movimientos_legales(p("e4")), casillas("e5", "d5"))

    def test_peon_negro_avanza_hacia_abajo(self):
        partida = partida_con([("peon", N, "d7"), ("rey", B, "a1"), ("rey", N, "h8")], empieza=N)
        self.assertEqual(partida.movimientos_legales(p("d7")), casillas("d6", "d5"))

    def test_torre_se_frena_con_piezas(self):
        partida = partida_con([("torre", B, "a1"), ("peon", B, "a3"), ("caballo", N, "c1"),
                               ("rey", B, "h1"), ("rey", N, "h8")])
        self.assertEqual(partida.movimientos_legales(p("a1")), casillas("a2", "b1", "c1"))

    def test_caballo_salta(self):
        partida = Partida()
        self.assertEqual(partida.movimientos_legales(p("b1")), casillas("a3", "c3"))

    def test_alfil_en_diagonal(self):
        partida = partida_con([("alfil", B, "c1"), ("rey", B, "h1"), ("rey", N, "h8")])
        self.assertEqual(partida.movimientos_legales(p("c1")), casillas("b2", "a3", "d2", "e3", "f4", "g5", "h6"))

    def test_reina_combina_torre_y_alfil(self):
        # los reyes van fuera de las líneas de la reina para que no le tapen casillas
        partida = partida_con([("reina", B, "d4"), ("rey", B, "h2"), ("rey", N, "a8")])
        destinos = partida.movimientos_legales(p("d4"))
        self.assertEqual(len(destinos), 27)
        self.assertTrue({p("d8"), p("h4"), p("a7"), p("g7")} <= destinos)

    def test_rey_una_casilla(self):
        partida = partida_con([("rey", B, "e4"), ("rey", N, "a8")])
        self.assertEqual(len(partida.movimientos_legales(p("e4"))), 8)


class TestTurnosCapturaYValidacion(unittest.TestCase):
    def test_los_turnos_se_alternan(self):
        partida = Partida()
        partida.mover(p("e2"), p("e4"))
        self.assertIs(partida.turno, N)
        partida.mover(p("e7"), p("e5"))
        self.assertIs(partida.turno, B)

    def test_no_se_puede_mover_una_pieza_ajena(self):
        partida = Partida()
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("e7"), p("e5"))

    def test_no_se_puede_mover_desde_una_casilla_vacia(self):
        with self.assertRaises(MovimientoInvalido):
            Partida().mover(p("e4"), p("e5"))

    def test_movimiento_prohibido_por_la_pieza(self):
        partida = Partida()
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("a1"), p("a5"))   # la torre está tapada por su peón

    def test_movimiento_invalido_no_cambia_nada(self):
        partida = Partida()
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("e2"), p("e5"))
        self.assertIsNotNone(partida.tablero.pieza_en(p("e2")))
        self.assertIs(partida.turno, B)

    def test_captura(self):
        partida = partida_con([("torre", B, "a1"), ("alfil", N, "a7"), ("rey", B, "h1"), ("rey", N, "h8")])
        jugada = partida.mover(p("a1"), p("a7"))
        self.assertEqual(jugada.capturada.nombre, "alfil")
        self.assertEqual(partida.tablero.pieza_en(p("a7")).color, B)
        self.assertEqual(len(list(partida.tablero.piezas(N))), 1)

    def test_no_se_puede_capturar_al_rey_rival(self):
        partida = partida_con([("torre", B, "a1"), ("rey", B, "h1"), ("rey", N, "a8")])

        self.assertNotIn(p("a8"), partida.movimientos_legales(p("a1")))
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("a1"), p("a8"))

        self.assertEqual(partida.tablero.pieza_en(p("a8")).nombre, "rey")
        self.assertIs(partida.turno, B)
        self.assertEqual(partida.historial, [])

    def test_no_se_captura_una_pieza_propia(self):
        partida = Partida()
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("d1"), p("d2"))


class TestJaque(unittest.TestCase):
    def test_detecta_jaque_de_torre(self):
        partida = partida_con([("rey", B, "e1"), ("torre", N, "e8"), ("rey", N, "a8")])
        self.assertTrue(partida.esta_en_jaque(B))

    def test_detecta_jaque_de_caballo(self):
        partida = partida_con([("rey", B, "e1"), ("caballo", N, "f3"), ("rey", N, "a8")])
        self.assertTrue(partida.esta_en_jaque(B))

    def test_el_peon_da_jaque_en_diagonal_y_no_de_frente(self):
        de_frente = partida_con([("rey", B, "e4"), ("peon", N, "e5"), ("rey", N, "a8")])
        en_diagonal = partida_con([("rey", B, "e4"), ("peon", N, "d5"), ("rey", N, "a8")])
        self.assertFalse(de_frente.esta_en_jaque(B))
        self.assertTrue(en_diagonal.esta_en_jaque(B))

    def test_una_pieza_en_el_medio_tapa_el_jaque(self):
        partida = partida_con([("rey", B, "e1"), ("alfil", B, "e4"), ("torre", N, "e8"), ("rey", N, "a8")])
        self.assertFalse(partida.esta_en_jaque(B))

    def test_la_jugada_informa_el_jaque(self):
        partida = partida_con([("torre", B, "a1"), ("rey", B, "h1"), ("rey", N, "e8")])
        self.assertTrue(partida.mover(p("a1"), p("e1")).da_jaque)

    def test_no_se_puede_dejar_al_propio_rey_en_jaque(self):
        # el alfil está clavado: si se mueve, la torre ataca al rey
        partida = partida_con([("rey", B, "e1"), ("alfil", B, "e2"), ("torre", N, "e8"), ("rey", N, "a8")])
        with self.assertRaises(MovimientoInvalido):
            partida.mover(p("e2"), p("d3"))

    def test_el_rey_no_puede_meterse_en_jaque(self):
        partida = partida_con([("rey", B, "e1"), ("torre", N, "d8"), ("rey", N, "a8")])
        self.assertNotIn(p("d1"), partida.movimientos_legales(p("e1")))

    def test_mate_del_loco(self):
        partida = Partida()
        for desde, hasta in (("f2", "f3"), ("e7", "e5"), ("g2", "g4"), ("d8", "h4")):
            partida.mover(p(desde), p(hasta))
        self.assertTrue(partida.esta_en_jaque(B))
        self.assertTrue(partida.es_jaque_mate())

    def test_jaque_que_no_es_mate(self):
        partida = partida_con([("rey", B, "e1"), ("torre", N, "e8"), ("rey", N, "a8")])
        self.assertTrue(partida.esta_en_jaque(B))
        self.assertFalse(partida.es_jaque_mate())


class TestExtensibilidad(unittest.TestCase):
    """Lo que el profe puede pedir en la defensa: una pieza nueva u otro tamaño de tablero."""

    def test_pieza_nueva_sin_tocar_clases_existentes(self):
        # Canciller: se mueve como torre y como caballo. Se registra en el catálogo y listo.
        catalogo = catalogo_clasico()
        catalogo.registrar("canciller", lambda c: Pieza("canciller", c, (Deslizante(RECTAS), Salto(SALTOS_DE_CABALLO)), "K" if c is B else "k"))
        partida = partida_con([("canciller", B, "a1"), ("rey", B, "h1"), ("rey", N, "h8")], catalogo=catalogo)
        destinos = partida.movimientos_legales(p("a1"))
        self.assertIn(p("a8"), destinos)   # como torre
        self.assertIn(p("b3"), destinos)   # como caballo
        self.assertNotIn(p("b2"), destinos)

    def test_tablero_de_otro_tamano(self):
        partida = partida_con([("torre", B, "a1"), ("rey", B, "j1"), ("rey", N, "j10")], filas=10, columnas=10)
        destinos = partida.movimientos_legales(p("a1"))
        self.assertIn(p("a10"), destinos)
        self.assertNotIn(Posicion(10, 0), destinos)

    def test_peon_en_tablero_mas_grande_usa_su_fila_de_salida(self):
        partida = partida_con([("peon", N, "c9"), ("rey", B, "a1"), ("rey", N, "j10")], filas=10, columnas=10, empieza=N)
        self.assertEqual(partida.movimientos_legales(p("c9")), casillas("c8", "c7"))


class TestConsola(unittest.TestCase):
    def test_partida_por_consola_sin_teclado_real(self):
        from ajedrez.adaptadores.consola import jugar
        entradas = iter(["e2 e4", "e2 e3", "e7 e5", "salir"])
        salidas = []
        jugar(entrada=lambda _: next(entradas), salida=salidas.append)
        texto = "\n".join(salidas)
        self.assertIn("No se puede", texto)   # e2 ya está vacía después de e2 e4

    def test_dibujo_del_tablero(self):
        from ajedrez.adaptadores.consola import dibujar
        dibujo = dibujar(Partida()).splitlines()
        self.assertEqual(dibujo[0], " 8 t c a d r a c t")
        self.assertEqual(dibujo[-1], "   a b c d e f g h")


if __name__ == "__main__":
    unittest.main()
