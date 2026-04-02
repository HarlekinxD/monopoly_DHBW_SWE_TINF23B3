from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile


class BuyPropertyUseCase:
    def execute(self, game: Game) -> None:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if not isinstance(tile, OwnableTile):
            raise ValueError("The current tile cannot be bought.")

        if tile.is_owned():
            raise ValueError("The property is already owned.")

        if player.balance.amount < tile.price.amount:
            raise ValueError("The player does not have enough money to buy this property.")

        player.pay_money(tile.price)
        tile.buy(player.name)
        player.add_owned_tile(tile.tile_id)