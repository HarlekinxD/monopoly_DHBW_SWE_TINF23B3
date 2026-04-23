from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile


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

        if player.balance.amount < tile.house_price.amount:
            raise ValueError("You do not have enough money to build a house.")

        tile.build_house()
        player.pay_money(tile.house_price)

        if tile.has_hotel():
            return f"{player.name} built a hotel on {tile.name}."

        return f"{player.name} built a house on {tile.name}."

    def _player_owns_full_color_group(self, game: Game, owner_name: str, color) -> bool:
        same_color_properties = [
            tile for tile in game.board.tiles
            if isinstance(tile, PropertyTile) and tile.color == color
        ]

        if not same_color_properties:
            return False

        return all(tile.owner_name == owner_name for tile in same_color_properties)