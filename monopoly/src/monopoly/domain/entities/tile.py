from dataclasses import dataclass

from monopoly.domain.tile_type import TileType


@dataclass
class Tile:
    tile_id: int
    name: str
    tile_type: TileType

    def __post_init__(self) -> None:
        if self.tile_id < 0:
            raise ValueError("Die ID eines Feldes darf nicht negativ sein.")

        if not self.name.strip():
            raise ValueError("Der Name eines Feldes darf nicht leer sein.")

    def __str__(self) -> str:
        return f"Tile(id={self.tile_id}, name='{self.name}', type={self.tile_type.value})"