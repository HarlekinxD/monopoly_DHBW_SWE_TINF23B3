# Enum for the colors of the roads

from enum import Enum


class TileColor(Enum):
    CYAN = "cyan"
    DARK_BLUE = "blue"
    GREEN = "green"
    ORANGE = "orange"
    PINK = "pink"
    PURPLE = "purple"
    RED = "red"
    YELLOW = "yellow"
    WHITE = "white"
    NONE = "none"

    def __str__(self) -> str:
        return self.value