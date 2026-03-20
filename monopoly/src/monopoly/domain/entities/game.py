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

    def __post_init__(self) -> None:
        if len(self.players) < 2 or len(self.players) > 7:
            raise ValueError("A game of Monopoly needs 2 to 7 players.")

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def next_player(self) -> None:
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def toggle_view(self) -> None:
        self.active_view = "ownership" if self.active_view == "board" else "board"

    def start(self) -> None:
        self.is_started = True