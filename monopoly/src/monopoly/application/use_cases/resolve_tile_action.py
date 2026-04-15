from monopoly.domain.entities.game import Game
from monopoly.domain.entities.special_tile import SpecialTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.value_objects.position import Position
from monopoly.application.use_cases.draw_community_card import DrawCommunityCardUseCase
from monopoly.application.use_cases.draw_chance_card import DrawChanceCardUseCase


class ResolveTileActionUseCase:
    JAIL_POSITION = Position(10)

    def __init__(self) -> None:
        self.draw_community_card_use_case = DrawCommunityCardUseCase()
        self.draw_chance_card_use_case = DrawChanceCardUseCase()

    def execute(self, game: Game) -> str:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if isinstance(tile, TaxTile):
            tax = tile.get_tax_amount()
            player.pay_money(tax)
            return f"{player.name} paid tax: {tax.amount}"

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

        if tile_name == "Im Gefängnis (Nur zu Besuch)":
            return f"{player.name} is just visiting jail."

        if tile_name == "Gemeinschaftsfeld":
            return self.draw_community_card_use_case.execute(game)
        
        if tile_name == "Ereignisfeld":
            return self.draw_chance_card_use_case.execute(game)

        return f"No action defined for tile: {tile_name}"