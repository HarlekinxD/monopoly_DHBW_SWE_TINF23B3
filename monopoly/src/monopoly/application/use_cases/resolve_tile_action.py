from monopoly.domain.entities.game import Game
from monopoly.domain.entities.special_tile import SpecialTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.value_objects.position import Position
from monopoly.domain.value_objects.money import Money


class ResolveTileActionUseCase:
    JAIL_POSITION = Position(10)

    def execute(self, game: Game) -> str:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if isinstance(tile, TaxTile):
            player.pay_money(tile.get_tax_amount())
            return f"{player.name} paid tax: {tile.get_tax_amount().amount}"

        if isinstance(tile, SpecialTile):
            return self._handle_special_tile(game, tile.name)

        return "No special action resolved."

    def _handle_special_tile(self, game: Game, tile_name: str) -> str:
        player = game.current_player

        if tile_name == "LOS":
            return f"{player.name} is on GO."

        if tile_name == "Frei Parken":
            return f"{player.name} is on Free Parking."

        if tile_name == "Gehe ins Gefängnis":
            player.send_to_jail(self.JAIL_POSITION)
            return f"{player.name} was sent to jail."

        if tile_name in {"Gemeinschaftsfeld", "Ereignisfeld"}:
            return f"{tile_name} is not implemented yet."

        if tile_name == "Im Gefängnis (Nur zu Besuch)":
            return f"{player.name} is just visiting jail."

        return f"No action defined for tile: {tile_name}"