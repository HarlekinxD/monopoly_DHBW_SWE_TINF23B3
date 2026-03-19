from dataclasses import dataclass, field

from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


@dataclass
class UtilityTile(OwnableTile):
    utility_multipliers: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.tile_type != TileType.UTILITY:
            raise ValueError("UtilityTile muss den Typ UTILITY haben.")

        if not self.utility_multipliers:
            raise ValueError("Ein Werk muss Multiplikatoren haben.")

    def get_rent(self, dice_value: int, owned_utilities: int) -> Money:
        if dice_value <= 0:
            raise ValueError("Der Würfelwert muss größer als 0 sein.")

        if owned_utilities <= 0:
            raise ValueError("Die Anzahl besessenen Straßen muss mindestens 1 sein.")

        if owned_utilities > len(self.utility_multipliers):
            raise ValueError("Für diese Anzahl an Straßen ist kein Multiplikator definiert.")

        multiplier = self.utility_multipliers[owned_utilities - 1]
        return Money(dice_value * multiplier)