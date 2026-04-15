from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.value_objects.money import Money


class RentCalculator:
    def calculate_property_rent(self, tile: PropertyTile) -> Money:
        return tile.get_current_rent()

    def calculate_railroad_rent(self, tile: RailroadTile, owned_railroads: int) -> Money:
        return tile.get_rent(owned_railroads)

    def calculate_utility_rent(self, tile: UtilityTile, dice_value: int, owned_utilities: int) -> Money:
        return tile.get_rent(dice_value, owned_utilities)