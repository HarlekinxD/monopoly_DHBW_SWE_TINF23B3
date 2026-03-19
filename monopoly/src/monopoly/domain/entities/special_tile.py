from dataclasses import dataclass

from monopoly.domain.entities.tile import Tile
from monopoly.domain.tile_type import TileType


@dataclass
class SpecialTile(Tile):
    def __post_init__(self) -> None:
        super().__post_init__()

        if self.tile_type != TileType.SPECIAL:
            raise ValueError("SpecialTile muss den Typ SPECIAL haben.")
        