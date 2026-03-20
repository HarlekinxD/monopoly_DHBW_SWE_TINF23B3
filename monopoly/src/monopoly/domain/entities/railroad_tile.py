from dataclasses import dataclass, field

from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


@dataclass
class RailroadTile(OwnableTile):
    railroad_rents: list[Money] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.tile_type != TileType.RAILROAD:
            raise ValueError("RailroadTile must have type RAILROAD.")
        if not self.railroad_rents:
            raise ValueError("A railroad must have rent levels.")

    def get_rent(self, owned_railroads: int) -> Money:
        if owned_railroads <= 0:
            raise ValueError("The number of railroads must be at least 1.")
        if owned_railroads > len(self.railroad_rents):
            raise ValueError("For this number of railroads no rent is defined.")
        return self.railroad_rents[owned_railroads - 1]