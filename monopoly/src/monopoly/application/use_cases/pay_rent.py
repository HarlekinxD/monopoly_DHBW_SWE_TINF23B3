from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.value_objects.money import Money


class PayRentUseCase:
    def execute(self, game: Game, dice_value: int | None = None) -> None:
        tenant = game.current_player
        tile = game.board.get_tile_at(tenant.position)

        if not isinstance(tile, OwnableTile):
            raise ValueError("The current tile is not ownable.")

        if not tile.is_owned():
            raise ValueError("The current tile is not owned.")

        if tile.owner_name == tenant.name:
            return

        owner = self._find_player_by_name(game, tile.owner_name)

        if isinstance(tile, PropertyTile):
            rent = self._calculate_property_rent(game, tile)
        elif isinstance(tile, RailroadTile):
            rent = self._calculate_railroad_rent(game, owner.name)
        elif isinstance(tile, UtilityTile):
            if dice_value is None:
                raise ValueError("Dice value is required for utility rent.")
            rent = self._calculate_utility_rent(game, tile, owner.name, dice_value)
        else:
            raise ValueError("Unsupported ownable tile type.")

        tenant.pay_money(rent)
        owner.receive_money(rent)

    def _find_player_by_name(self, game: Game, name: str):
        for player in game.players:
            if player.name == name:
                return player
        raise ValueError(f"Owner '{name}' was not found.")

    def _calculate_property_rent(self, game: Game, tile: PropertyTile) -> Money:
        rent = tile.get_current_rent()

        if tile.house_count == 0 and self._owner_has_full_color_group(game, tile):
            return Money(rent.amount * 2)

        return rent

    def _owner_has_full_color_group(self, game: Game, tile: PropertyTile) -> bool:
        same_color_tiles = [
            current_tile
            for current_tile in game.board.tiles
            if isinstance(current_tile, PropertyTile)
            and current_tile.color == tile.color
        ]

        return all(
            current_tile.owner_name == tile.owner_name
            for current_tile in same_color_tiles
        )

    def _calculate_railroad_rent(self, game: Game, owner_name: str) -> Money:
        owned_railroads = [
            tile
            for tile in game.board.tiles
            if isinstance(tile, RailroadTile)
            and tile.owner_name == owner_name
        ]

        count = len(owned_railroads)
        current_tile = game.board.get_tile_at(game.current_player.position)

        if not isinstance(current_tile, RailroadTile):
            raise ValueError("Current tile is not a railroad.")

        return current_tile.railroad_rents[count - 1]

    def _calculate_utility_rent(
        self,
        game: Game,
        tile: UtilityTile,
        owner_name: str,
        dice_value: int,
    ) -> Money:
        owned_utilities = [
            current_tile
            for current_tile in game.board.tiles
            if isinstance(current_tile, UtilityTile)
            and current_tile.owner_name == owner_name
        ]

        multiplier_index = min(len(owned_utilities), len(tile.utility_multipliers)) - 1
        multiplier = tile.utility_multipliers[multiplier_index]

        return Money(dice_value * multiplier)