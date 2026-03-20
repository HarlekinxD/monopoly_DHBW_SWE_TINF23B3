from dataclasses import dataclass


@dataclass(frozen=True)
class DiceRoll:
    value: int

    def __post_init__(self) -> None:
        if self.value < 2 or self.value > 12:
            raise ValueError("A dice roll using two dice must have a value between 2 and 12.")