from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.value_objects.money import Money


class PayRentUseCase:
    def execute(self, game: Game, dice_value: int | None = None) -> None:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        # Not ownable → nothing happens
        if not hasattr(tile, "is_owned"):
            return

        if not tile.is_owned():
            return

        # Player owns the tile → nothing happens
        if tile.owner_name == player.name:
            return

        owner = self._find_owner(game, tile.owner_name)

        rent = self._calculate_rent(tile, game, owner, dice_value)

        player.pay_money(rent)
        owner.receive_money(rent)

    def _find_owner(self, game: Game, owner_name: str):
        for player in game.players:
            if player.name == owner_name:
                return player
        raise ValueError("Owner not found.")

    def _calculate_rent(self, tile, game, owner, dice_value):
        if isinstance(tile, PropertyTile):
            return tile.get_current_rent()

        if isinstance(tile, RailroadTile):
            owned = self._count_owned_type(owner, RailroadTile, game)
            return tile.get_rent(owned)

        if isinstance(tile, UtilityTile):
            owned = self._count_owned_type(owner, UtilityTile, game)
            if dice_value is None:
                raise ValueError("Dice value required for utility rent.")
            return tile.get_rent(dice_value, owned)

        return Money(0)

    def _count_owned_type(self, owner, tile_type, game):
        count = 0
        for tile in game.board.tiles:
            if isinstance(tile, tile_type) and tile.owner_name == owner.name:
                count += 1
        return count