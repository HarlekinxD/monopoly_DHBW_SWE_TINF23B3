from dataclasses import dataclass

from monopoly.application.dto.player_state_dto import PlayerStateDTO


@dataclass(frozen=True)
class GameStateDTO:
    current_player_name: str
    current_player_index: int
    active_view: str
    is_started: bool
    board_size: int
    players: list[PlayerStateDTO]