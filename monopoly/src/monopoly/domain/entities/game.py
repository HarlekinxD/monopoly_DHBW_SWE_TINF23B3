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

    eliminated_players: list[str] = field(default_factory=list)

    current_round: int = 1
    last_roll: int | str = "-"
    last_message: str = ""

    def __post_init__(self) -> None:
        if len(self.players) < 2 or len(self.players) > 7:
            raise ValueError("A Monopoly game requires 2 to 7 players.")

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def start(self) -> None:
        self.is_started = True

    def get_active_players(self) -> list[Player]:
        return [player for player in self.players if not player.is_bankrupt]

    def eliminate_player(self, player: Player) -> None:
        if player.is_bankrupt and player.name not in self.eliminated_players:
            self.eliminated_players.append(player.name)

    def next_player(self) -> None:
        if len(self.get_active_players()) <= 1:
            return

        old_index = self.current_player_index
        next_index = old_index

        while True:
            next_index = (next_index + 1) % len(self.players)
            if not self.players[next_index].is_bankrupt:
                self.current_player_index = next_index
                break

        if self.current_player_index <= old_index:
            self.current_round += 1

        self.has_rolled_this_turn = False
        self.can_buy_current_tile = False
        self.purchased_this_turn = False
        self.current_turn_tile_id = None
        self.last_roll = "-"

    def toggle_view(self) -> None:
        self.active_view = "ownership" if self.active_view == "board" else "board"