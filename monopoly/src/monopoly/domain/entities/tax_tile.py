from dataclasses import dataclass

from monopoly.domain.entities.tile import Tile
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


@dataclass
class TaxTile(Tile):
    tax_amount: Money

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.tile_type != TileType.TAX:
            raise ValueError("TaxTile muss den Typ TAX haben.")

    def get_tax_amount(self) -> Money:
        return self.tax_amount