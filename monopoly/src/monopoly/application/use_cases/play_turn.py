from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.application.use_cases.resolve_tile_action import ResolveTileActionUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.value_objects.money import Money


class PlayTurnUseCase:
    GO_BONUS = Money(200)

    def __init__(self, random_port: RandomPort) -> None:
        self.random_port = random_port
        self.resolve_tile_action_use_case = ResolveTileActionUseCase()
        self.pay_rent_use_case = PayRentUseCase()

    def execute(self, game: Game) -> dict:
        player = game.current_player

        if player.in_jail:
            player.increment_jail_turn()
            return {
                "player": player.name,
                "dice_value": None,
                "tile_name": game.board.get_tile_at(player.position).name,
                "message": f"{player.name} is in jail.",
                "can_buy": False,
            }

        dice_value = self.random_port.roll_dice()
        passed_start = player.move(dice_value, game.board.size())

        if passed_start:
            player.receive_money(self.GO_BONUS)

        tile = game.board.get_tile_at(player.position)

        action_message = self.resolve_tile_action_use_case.execute(game)

        can_buy = False
        if isinstance(tile, OwnableTile):
            if not tile.is_owned():
                can_buy = True
            elif tile.owner_name != player.name:
                self.pay_rent_use_case.execute(game, dice_value=dice_value)

        return {
            "player": player.name,
            "dice_value": dice_value,
            "tile_name": tile.name,
            "message": action_message,
            "can_buy": can_buy,
        }