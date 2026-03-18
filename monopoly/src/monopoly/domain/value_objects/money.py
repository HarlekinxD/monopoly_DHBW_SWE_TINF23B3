# Importing dataclass für das einfachere Erstellen von Klassen (automatische Generierung von __init__, __repr__, etc.)
from dataclasses import dataclass

@dataclass(frozen=True)  # frozen=True Objekt ist unveränderlich.
class Money:
    amount: int

    # Betrag darf nicht negativ sein, 
    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Ihr Guthaben kann nicht negativ sein.")
    
    # Addition von Geldbeträgen, gibt ein neues Money-Objekt zurück.
    def add(self, other: "Money" ) -> "Money":
        return Money(self.amount + other.amount)
    
    # Subtraktion von Monopoly$ beträgen, gibt ein neues Money-Objekt zurück.
    def subtract(self, other: "Money") -> "Money":
        if other.amount > self.amount:
            raise ValueError("Sie können nicht mehr Geld ausgeben, als Sie auf der Bank haben.")
        return Money(self.amount - other.amount)
    
    # gibt True zurück, wenn self größer als other ist.
    def is_greater_than(self, other: "Money")-> bool:
        return self.amount > other.amount
    
    # gibt True zurück, wenn self kleiner als other ist.
    def is_less_than(self, other: "Money")-> bool:
        return self.amount < other.amount
    
    # gibt True zurück, wenn self gleich other ist.
    def is_equal_to(self, other: "Money")-> bool:
        return self.amount == other.amount
    
    def __str__(self) -> str:
        return f"{self.amount} M"