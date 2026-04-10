from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative.")

    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def subtract(self, other: "Money") -> "Money":
        return Money(self.amount - other.amount)

    def __str__(self) -> str:
        return f"{self.amount} M"
    