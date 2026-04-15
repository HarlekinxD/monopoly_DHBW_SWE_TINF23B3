from dataclasses import dataclass, field

from monopoly.domain.entities.board import Board
from monopoly.domain.entities.player import Player


@dataclass
class Game:
    board: Board
    players: list[Player]
    current_player_index: int = 0
    active_view: str = "board"
    is_started: bool = False

    has_rolled_this_turn: bool = False
    can_buy_current_tile: bool = False
    purchased_this_turn: bool = False
    current_turn_tile_id: int | None = None

    def __post_init__(self) -> None:
        if len(self.players) < 2 or len(self.players) > 7:
            raise ValueError("A game of Monopoly needs 2 to 7 players.")

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.has_rolled_this_turn = False
        self.can_buy_current_tile = False
        self.purchased_this_turn = False
        self.current_turn_tile_id = None

    def toggle_view(self) -> None:
        self.active_view = "ownership" if self.active_view == "board" else "board"

    def start(self) -> None:
        self.is_started = True