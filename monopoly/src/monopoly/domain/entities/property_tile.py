from dataclasses import dataclass, field

from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.tile_color import TileColor
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


@dataclass
class PropertyTile(OwnableTile):
    color: TileColor = TileColor.NONE
    house_price: Money | None = None
    rent_levels: list[Money] = field(default_factory=list)
    house_count: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.tile_type != TileType.PROPERTY:
            raise ValueError("PropertyTile muss den Typ PROPERTY haben.")

        if self.house_price is None:
            raise ValueError("Eine Straße muss Hauskosten haben.")

        if not self.rent_levels:
            raise ValueError("Eine Straße muss Mietstufen haben.")

        if self.house_count < 0:
            raise ValueError("Die Anzahl der Häuser darf nicht negativ sein.")

        if self.house_count >= len(self.rent_levels):
            raise ValueError("Die Hausanzahl passt nicht zu den Mietstufen.")

    def get_current_rent(self) -> Money:
        return self.rent_levels[self.house_count]

    def can_build_house(self) -> bool:
        return self.is_owned() and self.house_count < 5

    def build_house(self) -> None:
        if not self.can_build_house():
            raise ValueError(f"Auf dem Feld '{self.name}' kann kein Haus gebaut werden.")

        self.house_count += 1

    def clear_owner(self) -> None:
        super().clear_owner()
        self.house_count = 0