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
    in_jail: bool = False
    jail_turns: int = 0

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Player name must not be empty.")

    # Movement
    def move(self, steps: int, board_size: int) -> bool:
        passed_start = self.position.has_passed_start(steps, board_size)
        self.position = self.position.move(steps, board_size)
        return passed_start

    def move_to(self, position: Position) -> None:
        self.position = position

    # Money handling
    def pay_money(self, amount: Money) -> None:
        try:
            self.balance = self.balance.subtract(amount)
        except ValueError:
            # Bankrott-Logik (später ausbauen)
            self.is_bankrupt = True
            raise

    def receive_money(self, amount: Money) -> None:
        self.balance = self.balance.add(amount)

    # Ownership
    def add_owned_tile(self, tile_id: int) -> None:
        if tile_id not in self.owned_tile_ids:
            self.owned_tile_ids.append(tile_id)

    def owns_tile(self, tile_id: int) -> bool:
        return tile_id in self.owned_tile_ids

    # Jail
    def send_to_jail(self, jail_position: Position) -> None:
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0

    def release_from_jail(self) -> None:
        self.in_jail = False
        self.jail_turns = 0