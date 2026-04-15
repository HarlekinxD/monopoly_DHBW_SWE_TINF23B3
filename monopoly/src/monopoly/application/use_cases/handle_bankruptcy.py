from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.entities.player import Player


class HandleBankruptcyUseCase:
    def execute(self, game: Game, player: Player) -> str:
        if not player.is_bankrupt and player.balance.amount > 0:
            return f"{player.name} is still active."

        player.is_bankrupt = True

        for tile in game.board.tiles:
            if isinstance(tile, OwnableTile) and tile.owner_name == player.name:
                tile.clear_owner()

        player.owned_tile_ids.clear()
        game.eliminate_player(player)

        return f"{player.name} has been eliminated."