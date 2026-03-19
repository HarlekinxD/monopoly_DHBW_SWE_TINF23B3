# Farben für die Straßen im Monopoly-Spiel, Enum für die festen Werte der Farben

from enum import Enum


class TileColor(Enum):
    CYAN = "cyan"
    DARK_BLUE = "dunkelblau"
    GREEN = "grün"
    ORANGE = "orange"
    PINK = "pink"
    PURPLE = "lila"
    RED = "rot"
    YELLOW = "gelb"
    WHITE = "weiß"
    NONE = "keine"

    def __str__(self) -> str:
        return self.value