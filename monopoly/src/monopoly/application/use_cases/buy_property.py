from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile


class BuyPropertyUseCase:
    def execute(self, game: Game) -> None:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        if not game.has_rolled_this_turn:
            raise ValueError("You must roll before you can buy a property.")

        if game.purchased_this_turn:
            raise ValueError("You have already bought a property this turn.")

        if not game.can_buy_current_tile:
            raise ValueError("The current tile cannot be bought.")

        if game.current_turn_tile_id != tile.tile_id:
            raise ValueError("You can only buy the tile you landed on this turn.")

        if not isinstance(tile, OwnableTile):
            raise ValueError("The current tile cannot be bought.")

        if tile.is_owned():
            raise ValueError("The property is already owned.")

        if player.owns_tile(tile.tile_id):
            raise ValueError("The player already owns this property.")

        if player.balance.amount < tile.price.amount:
            raise ValueError("The player does not have enough money to buy this property.")

        player.pay_money(tile.price)
        tile.buy(player.name)
        player.add_owned_tile(tile.tile_id)

        game.purchased_this_turn = True
        game.can_buy_current_tile = False