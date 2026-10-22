"""Genera docs/diagrama_clases.svg. Las clases y relaciones de acá tienen que coincidir con el código:
si se cambia una clase, se actualiza esta lista y se vuelve a generar (python docs/generar_uml.py)."""
from pathlib import Path
from xml.sax.saxutils import escape

ANCHO_CAR = 7.4     # ancho aprox. de un carácter en 12px monoespaciada
ALTO_LINEA = 17

# nombre: (x, y, estereotipo, atributos, métodos)
CLASES = {
    "Partida": (560, 20, "", ["catalogo: CatalogoDePiezas", "tablero: Tablero", "turno: Color", "historial: List[Jugada]"],
                ["mover(desde, hasta): Jugada", "movimientos_legales(desde): Set[Posicion]", "esta_en_jaque(color): bool",
                 "tiene_movimientos(color): bool", "es_jaque_mate(): bool",
                 "-_captura_rey_rival(hasta, color): bool", "-_deja_en_jaque(desde, hasta, color): bool"]),
    "Jugada": (1060, 40, "dataclass", ["pieza: Pieza", "desde: Posicion", "hasta: Posicion", "capturada: Pieza?", "da_jaque: bool"], []),
    "MovimientoInvalido": (1060, 230, "exception", [], []),
    "consola": (60, 20, "adaptador", [], ["jugar(entrada, salida)", "dibujar(partida): str"]),
    "Disposicion": (60, 300, "abstract", [], ["armar(catalogo): Tablero"]),
    "DisposicionClasica": (20, 470, "", [], ["armar(catalogo): Tablero"]),
    "DisposicionLibre": (250, 470, "", ["filas: int", "columnas: int", "piezas: list"], ["armar(catalogo): Tablero"]),
    "CatalogoDePiezas": (520, 330, "", ["-_fabricas: Dict[str, FabricaDePieza]"],
                         ["registrar(nombre, fabrica)", "crear(nombre, color): Pieza", "nombres(): List[str]"]),
    "Tablero": (930, 330, "", ["filas: int", "columnas: int", "-_casillas: Dict[Posicion, Pieza]"],
                ["dentro(pos): bool", "pieza_en(pos): Pieza?", "esta_vacia(pos): bool", "colocar(pieza, pos)", "quitar(pos): Pieza?",
                 "mover(desde, hasta): Pieza?", "piezas(color?): Iterator", "posicion_del_rey(color): Posicion?", "copia(): Tablero"]),
    "Pieza": (560, 600, "dataclass", ["nombre: str", "color: Color", "reglas: tuple[ReglaDeMovimiento]", "simbolo: str", "es_rey: bool"],
              ["destinos(tablero, desde): Set[Posicion]", "ataques(tablero, desde): Set[Posicion]"]),
    "Posicion": (1020, 700, "dataclass", ["fila: int", "columna: int"], ["desplazar(d_fila, d_columna): Posicion", "desde_notacion(texto): Posicion", "notacion(): str"]),
    "Color": (1020, 900, "enum", ["BLANCO", "NEGRO"], ["opuesto(): Color", "piezas: str"]),
    "ReglaDeMovimiento": (300, 860, "abstract", [], ["destinos(tablero, desde, color): Set", "ataques(tablero, desde, color): Set"]),
    "Deslizante": (60, 1060, "", ["direcciones: tuple"], ["destinos(...)"]),
    "Salto": (320, 1060, "", ["saltos: tuple"], ["destinos(...)"]),
    "AvancePeon": (560, 1060, "", ["fila_inicial_blanco: int", "fila_inicial_negro: int"], ["destinos(...)", "ataques(...)"]),
}

# (desde, hasta, tipo, etiqueta). tipos: herencia, composicion, agregacion, dependencia, asociacion
RELACIONES = [
    ("consola", "Partida", "dependencia", "usa"),
    ("Partida", "Tablero", "composicion", "1"),
    ("Partida", "CatalogoDePiezas", "asociacion", "1"),
    ("Partida", "Jugada", "composicion", "0..*"),
    ("Partida", "Disposicion", "dependencia", "arma el tablero con"),
    ("Partida", "MovimientoInvalido", "dependencia", "lanza"),
    ("DisposicionClasica", "Disposicion", "herencia", ""),
    ("DisposicionLibre", "Disposicion", "herencia", ""),
    ("Disposicion", "CatalogoDePiezas", "dependencia", "pide piezas a"),
    ("CatalogoDePiezas", "Pieza", "dependencia", "crea"),
    ("Tablero", "Pieza", "agregacion", "0..*"),
    ("Pieza", "ReglaDeMovimiento", "composicion", "1..*"),
    ("Pieza", "Color", "asociacion", ""),
    ("Deslizante", "ReglaDeMovimiento", "herencia", ""),
    ("Salto", "ReglaDeMovimiento", "herencia", ""),
    ("AvancePeon", "ReglaDeMovimiento", "herencia", ""),
    ("Tablero", "Posicion", "dependencia", "indexa por"),
]


DESPLAZAMIENTO_NUCLEO = 130   # todo lo que no es adaptador va dentro del recuadro del núcleo


def caja(nombre):
    x, y, est, attrs, mets = CLASES[nombre]
    if est != "adaptador":
        y += DESPLAZAMIENTO_NUCLEO
    lineas = [nombre] + attrs + mets + ([f"«{est}»"] if est else [])
    ancho = max(len(t) for t in lineas) * ANCHO_CAR + 24
    alto_titulo = ALTO_LINEA * (2 if est else 1) + 10
    alto = alto_titulo + max(1, len(attrs)) * ALTO_LINEA + 8 + max(1, len(mets)) * ALTO_LINEA + 8
    return x, y, ancho, alto, alto_titulo


def svg_clase(nombre):
    x, y, w, h, ht = caja(nombre)
    _, _, est, attrs, mets = CLASES[nombre]
    colores = {}
    fondo = colores.get(est, "#FFFFFF")
    partes = [f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" fill="{fondo}" stroke="#111111" stroke-width="1.4"/>']
    ty = y + 16
    if est:
        partes.append(f'<text x="{x + w / 2:.0f}" y="{ty}" text-anchor="middle" class="est">«{est}»</text>')
        ty += ALTO_LINEA
    estilo = "nomi" if est in ("abstract",) else "nom"
    partes.append(f'<text x="{x + w / 2:.0f}" y="{ty}" text-anchor="middle" class="{estilo}">{escape(nombre)}</text>')
    y1 = y + ht
    partes.append(f'<line x1="{x}" y1="{y1}" x2="{x + w:.0f}" y2="{y1}" stroke="#111111"/>')
    for i, a in enumerate(attrs):
        vis = "-" if a.startswith("-") else "+"
        partes.append(f'<text x="{x + 8}" y="{y1 + 15 + i * ALTO_LINEA}" class="m">{vis} {escape(a.lstrip("-"))}</text>')
    y2 = y1 + max(1, len(attrs)) * ALTO_LINEA + 8
    partes.append(f'<line x1="{x}" y1="{y2}" x2="{x + w:.0f}" y2="{y2}" stroke="#182029"/>')
    for i, m in enumerate(mets):
        vis = "-" if m.startswith("-") else "+"
        partes.append(f'<text x="{x + 8}" y="{y2 + 15 + i * ALTO_LINEA}" class="m">{vis} {escape(m.lstrip("-"))}</text>')
    return "\n".join(partes)


def borde(nombre, hacia):
    """Punto del borde de la caja 'nombre' en dirección al centro de 'hacia'."""
    x, y, w, h, _ = caja(nombre)
    cx, cy = x + w / 2, y + h / 2
    X, Y, W, H, _ = caja(hacia)
    tx, ty = X + W / 2, Y + H / 2
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    escala = min((w / 2) / abs(dx) if dx else 1e9, (h / 2) / abs(dy) if dy else 1e9)
    return cx + dx * escala, cy + dy * escala


def svg_relacion(a, b, tipo, etiqueta):
    x1, y1 = borde(a, b)
    x2, y2 = borde(b, a)
    guiones = ' stroke-dasharray="6 4"' if tipo == "dependencia" else ""
    if tipo == "herencia":
        fin = 'marker-end="url(#herencia)"'
        ini = ""
    elif tipo in ("composicion", "agregacion"):
        ini = f'marker-start="url(#{tipo})"'
        fin = 'marker-end="url(#flecha)"'
    else:
        ini, fin = "", 'marker-end="url(#flecha)"'
    partes = [f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#111111" stroke-width="1.3"{guiones} {ini} {fin}/>']
    if etiqueta:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        partes.append(f'<text x="{mx + 6:.0f}" y="{my - 5:.0f}" class="et">{escape(etiqueta)}</text>')
    return "\n".join(partes)


def generar():
    ancho = max(caja(n)[0] + caja(n)[2] for n in CLASES) + 30
    alto = max(caja(n)[1] + caja(n)[3] for n in CLASES) + 80
    defs = """<defs>
<marker id="flecha" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto"><path d="M0,0 L11,5 L0,10" fill="none" stroke="#111111" stroke-width="1.3"/></marker>
<marker id="herencia" markerWidth="16" markerHeight="14" refX="15" refY="7" orient="auto"><path d="M0,0 L15,7 L0,14 z" fill="#fff" stroke="#4A5568" stroke-width="1.3"/></marker>
<marker id="composicion" markerWidth="20" markerHeight="12" refX="1" refY="6" orient="auto"><path d="M1,6 L10,1 L19,6 L10,11 z" fill="#111111"/></marker>
<marker id="agregacion" markerWidth="20" markerHeight="12" refX="1" refY="6" orient="auto"><path d="M1,6 L10,1 L19,6 L10,11 z" fill="#fff" stroke="#182029"/></marker>
</defs>
<style>.m{font:12px Consolas,'Courier New',monospace;fill:#182029}.nom{font:bold 14px Arial,sans-serif;fill:#182029}
.nomi{font:italic bold 14px Arial,sans-serif;fill:#182029}.est{font:italic 11px Arial,sans-serif;fill:#4A5568}
.et{font:11px Arial,sans-serif;fill:#4A5568}.tit{font:bold 18px Arial,sans-serif;fill:#182029}.ley{font:12px Arial,sans-serif;fill:#4A5568}</style>"""
    cuerpo = [svg_relacion(*r) for r in RELACIONES] + [svg_clase(n) for n in CLASES]
    nucleo = '<rect x="5" y="{0}" width="{1}" height="{2}" fill="none" stroke="#111111" stroke-width="1.5" stroke-dasharray="10 6" rx="10"/>'.format(DESPLAZAMIENTO_NUCLEO, ancho - 15, alto - DESPLAZAMIENTO_NUCLEO - 70)
    leyenda = (f'<text x="10" y="{alto - 20}" class="ley">Recuadro punteado = núcleo (ajedrez/nucleo): no importa nada de afuera. '
               'La consola (ajedrez/adaptadores) depende del núcleo y nunca al revés.</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho:.0f} {alto:.0f}" width="{ancho:.0f}" height="{alto:.0f}">'
           f'<rect width="100%" height="100%" fill="#fff"/>{defs}'
           f'<text x="{ancho / 2:.0f}" y="{alto - 45}" text-anchor="middle" class="tit">TPO Ajedrez · Diagrama de clases</text>'
           f'{nucleo}' + "\n".join(cuerpo) + leyenda + "</svg>")
    salida = Path(__file__).with_name("diagrama_clases.svg")
    salida.write_text(svg, encoding="utf-8")
    print("generado", salida)


if __name__ == "__main__":
    generar()
