from enum import Enum


class Token(Enum):
    SHOE = "Shoe"
    HAT = "Hat"
    CAR = "Car"
    DOG = "Dog"
    SHIP = "Ship"
    WHEELBARROW = "Wheelbarrow"
    IRON = "Iron"

    def __str__(self) -> str:
        return self.value