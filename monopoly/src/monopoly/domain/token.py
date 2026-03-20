#Enum fixed number of player tokens

from enum import Enum



class Token(Enum):
    HAT = "Hat"
    CAR = "Car"
    DOG = "Dog"
    SHIP = "Ship"
    SHOE = "Shoe"
    WHEELBARROW = "Wheelbarrow"
    CAT = "Cat"

    def __str__(self) -> str:
        return self.value