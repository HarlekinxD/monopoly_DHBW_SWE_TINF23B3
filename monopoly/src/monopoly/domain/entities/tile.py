from dataclasses import dataclass

from monopoly.domain.tile_type import TileType


@dataclass
class Tile:
    tile_id: int
    name: str
    tile_type: TileType

    def __post_init__(self) -> None:
        if self.tile_id < 0:
            raise ValueError("The ID of a Field can't be negative.")
        if not self.name.strip():
            raise ValueError("The name of a Field cant be blank.")

    def __str__(self) -> str:
        return f"Tile(id={self.tile_id}, name='{self.name}', type={self.tile_type.value})"