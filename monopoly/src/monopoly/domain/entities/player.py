from dataclasses import dataclass, field

from monopoly.domain.token import Token
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


@dataclass
class Player:
    name: str
    position: Position = field(default_factory=lambda: Position(0))
    balance: Money = field(default_factory=lambda: Money(1500))
    token: Token | None = None
    owned_tile_ids: list[int] = field(default_factory=list)
    is_bankrupt: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("The player's name cant be blank.")

    def move_to(self, position: Position) -> None:
        self.position = position

    def add_owned_tile(self, tile_id: int) -> None:
        if tile_id not in self.owned_tile_ids:
            self.owned_tile_ids.append(tile_id)

    def pay(self, amount: Money) -> None:
        self.balance = self.balance.subtract(amount)
        if self.balance.amount < 0:
            self.is_bankrupt = True

    def receive(self, amount: Money) -> None:
        self.balance = self.balance.add(amount)