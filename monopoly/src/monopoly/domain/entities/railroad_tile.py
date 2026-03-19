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
            raise ValueError("RailroadTile muss den Typ RAILROAD haben.")

        if not self.railroad_rents:
            raise ValueError("Ein Bahnhof muss Mietstufen haben.")

    def get_rent(self, owned_railroads: int) -> Money:
        if owned_railroads <= 0:
            raise ValueError("Die Anzahl besessener Bahnhöfe muss mindestens 1 sein.")

        if owned_railroads > len(self.railroad_rents):
            raise ValueError("Für diese Anzahl an Bahnhöfen ist keine Miete definiert.")

        return self.railroad_rents[owned_railroads - 1]