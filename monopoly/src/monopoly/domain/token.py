#Enum fixed number of player tokens

from enum import Enum



class Token(Enum):
    HAT = "Hat"
    CAR = "Car"
    DOG = "Dog"
    SHIP = "Ship"
    SHOE = "Shoe"
    WHEELBARROW = "Wheelbarrow"
    IRON = "Iron"
    # Legacy token bleibt fuer alte savegames kompatibel.
    CAT = "Cat"

    def __str__(self) -> str:
        return self.value