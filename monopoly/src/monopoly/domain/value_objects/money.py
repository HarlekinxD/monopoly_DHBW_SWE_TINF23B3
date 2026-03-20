from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int

    def __post_init__(self) -> None:
        if not isinstance(self.amount, int):
            raise TypeError("Money must be an integer.")

    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def subtract(self, other: "Money") -> "Money":
        return Money(self.amount - other.amount)

    def __str__(self) -> str:
        return f"{self.amount}$"