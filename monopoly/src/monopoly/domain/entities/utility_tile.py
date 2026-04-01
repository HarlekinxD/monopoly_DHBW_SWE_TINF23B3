from dataclasses import dataclass, field

from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


@dataclass
class UtilityTile(OwnableTile):
    color: TileColor = TileColor.WHITE
    utility_multipliers: list[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.tile_type != TileType.UTILITY:
            raise ValueError("UtilityTile must have the type UTILITY.")
        if not self.utility_multipliers:
            raise ValueError("A utility must have multiplicators.")

    def get_rent(self, dice_value: int, owned_utilities: int) -> Money:
        if dice_value <= 0:
            raise ValueError("The value of the dice cast must be bigger than 0.")
        if owned_utilities <= 0:
            raise ValueError("The number of owned utilities must be at least 1:")
        if owned_utilities > len(self.utility_multipliers):
            raise ValueError("For this number of utilities no multiplicator is defined")

        multiplier = self.utility_multipliers[owned_utilities - 1]
        return Money(dice_value * multiplier)