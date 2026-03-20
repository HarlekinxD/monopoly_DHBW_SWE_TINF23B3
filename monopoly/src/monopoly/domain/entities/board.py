from dataclasses import dataclass

from monopoly.domain.entities.tile import Tile
from monopoly.domain.value_objects.position import Position

# Container for in game tiles. 
@dataclass
class Board:
    tiles: list[Tile]  # List of tile Objects

    def __post_init__(self) -> None:
        if not self.tiles:
            raise ValueError("Ein Board muss mindestens ein Feld haben.")

    def size(self) -> int:
        return len(self.tiles) # Number of Fields on the Board

    def get_tile_at(self, position: Position) -> Tile:
        return self.tiles[position.index] # returns tile on the Position

    def __str__(self) -> str:
        return f"Board(size={self.size()})"