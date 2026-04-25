#Enum feste Menge von Werten hier: die Spielfiguren im Monopoly-Spiel
from enum import Enum



class Token(Enum):
<<<<<<< Updated upstream
    HAT = "Hut"
    CAR = "Auto"
    DOG = "Hund"
    SHIP = "Schiff"
    SHOE = "Schuh"
    WHEELBARROW = "Schubkarre"
    CAT = "Katze"
=======
    HAT = "Hat"
    CAR = "Car"
    DOG = "Dog"
    SHIP = "Ship"
    SHOE = "Shoe"
    WHEELBARROW = "Wheelbarrow"
    IRON = "Iron"
    # Legacy token bleibt fuer alte savegames kompatibel.
    CAT = "Cat"
>>>>>>> Stashed changes

    def __str__(self) -> str:
        return self.value