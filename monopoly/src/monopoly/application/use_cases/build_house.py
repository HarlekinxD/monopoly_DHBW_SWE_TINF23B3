from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.tile_color import TileColor


class BuildHouseUseCase:
    def execute(self, game: Game) -> str:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if not isinstance(tile, PropertyTile):
            raise ValueError("Houses can only be built on properties.")

        if tile.owner_name != player.name:
            raise ValueError("You can only build on your own property.")

        if tile.has_hotel():
            raise ValueError("This property already has a hotel.")

        if not self._player_owns_full_color_group(game, player.name, tile.color):
            raise ValueError("You must own the full color group before building houses.")

        if not self._can_build_evenly(game, tile):
            # Regel: nur auf strassen bauen die aktuell die niedrigste anzahl haben.
            raise ValueError("Build failed: houses must be distributed evenly in the color group.")

        if player.balance.amount < tile.house_price.amount:
            raise ValueError("You do not have enough money to build a house.")

        tile.build_house()
        player.pay_money(tile.house_price)

        if tile.has_hotel():
            return f"{player.name} built a hotel on {tile.name}."

        return f"{player.name} built a house on {tile.name}."

    def _player_owns_full_color_group(self, game: Game, owner_name: str, color: TileColor) -> bool:
        same_color_properties = self._properties_in_color_group(game, color)

        if not same_color_properties:
            return False

        return all(tile.owner_name == owner_name for tile in same_color_properties)

    def _can_build_evenly(self, game: Game, target_tile: PropertyTile) -> bool:
        color_group_properties = self._properties_in_color_group(game, target_tile.color)

        # Nur auf den "niedrigsten" feldern darf noch eins drauf.
        min_house_count = min(tile.house_count for tile in color_group_properties)
        return target_tile.house_count == min_house_count

    def _properties_in_color_group(self, game: Game, color: TileColor) -> list[PropertyTile]:
        return [
            tile
            for tile in game.board.tiles
            if isinstance(tile, PropertyTile) and tile.color == color
        ]