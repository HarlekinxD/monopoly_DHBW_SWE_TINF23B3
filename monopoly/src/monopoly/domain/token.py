#Enum feste Menge von Werten hier: die Spielfiguren im Monopoly-Spiel
from enum import Enum



class Token(Enum):
    HAT = "Hut"
    CAR = "Auto"
    DOG = "Hund"
    SHIP = "Schiff"
    SHOE = "Schuh"
    WHEELBARROW = "Schubkarre"
    CAT = "Katze"

    def __str__(self) -> str:
        return self.value