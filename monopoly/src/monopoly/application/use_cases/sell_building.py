from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.tile_color import TileColor
from monopoly.domain.value_objects.money import Money


class SellBuildingUseCase:
    def execute(self, game: Game) -> str:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if not isinstance(tile, PropertyTile):
            raise ValueError("Buildings can only be sold on properties.")

        if tile.owner_name != player.name:
            raise ValueError("You can only sell on your own property.")

        if tile.house_count == 0:
            raise ValueError("There is no house or hotel to sell on this property.")

        if not self._can_sell_evenly(game, tile):
            # Spiegelregel zum bauen: nur von den hoechsten strassen darf verkauft werden.
            raise ValueError("Sell failed: buildings must be sold evenly in the color group.")

        # Hotel (5) wird zu 4 haeusern, sonst einfach ein haus weniger.
        if tile.house_count == 5:
            tile.house_count = 4
            sold_label = "hotel"
        else:
            tile.house_count -= 1
            sold_label = "house"

        refund = self._refund_for_sale(tile)
        player.receive_money(refund)

        return f"{player.name} sold a {sold_label} on {tile.name} and received {refund.amount}."

    def _can_sell_evenly(self, game: Game, target_tile: PropertyTile) -> bool:
        color_group_properties = self._properties_in_color_group(game, target_tile.color)
        max_house_count = max(tile.house_count for tile in color_group_properties)
        return target_tile.house_count == max_house_count

    def _properties_in_color_group(self, game: Game, color: TileColor) -> list[PropertyTile]:
        return [
            tile
            for tile in game.board.tiles
            if isinstance(tile, PropertyTile) and tile.color == color
        ]

    def _refund_for_sale(self, tile: PropertyTile) -> Money:
        if tile.house_price is None:
            raise ValueError("Property has no house price configured.")

        # Monopoly regel: halber hauspreis beim verkauf.
        return Money(tile.house_price.amount // 2)
