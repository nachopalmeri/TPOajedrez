from enum import Enum


class Color(Enum):
    BLANCO = "blanco"
    NEGRO = "negro"

    def opuesto(self) -> "Color":
        return Color.NEGRO if self is Color.BLANCO else Color.BLANCO

    @property
    def piezas(self) -> str:
        """Cómo se nombra al bando: 'las blancas', 'las negras'."""
        return "blancas" if self is Color.BLANCO else "negras"
