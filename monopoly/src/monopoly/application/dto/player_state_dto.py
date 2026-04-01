from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerStateDTO:
    name: str
    balance: int
    position: int
    owned_tile_ids: list[int]
    is_in_jail: bool
    jail_turns: int