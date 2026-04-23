from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.handle_bankruptcy import HandleBankruptcyUseCase
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
        self.handle_bankruptcy_use_case = HandleBankruptcyUseCase()

    def execute(self, game: Game) -> dict:
        if game.has_rolled_this_turn:
            raise ValueError("The current player has already rolled this turn.")

        player = game.current_player

        if player.in_jail:
            player.increment_jail_turn()
            game.has_rolled_this_turn = True
            game.can_buy_current_tile = False
            game.current_turn_tile_id = player.position.index
            game.last_roll = "-"
            return {
                "player": player.name,
                "dice_value": None,
                "tile_name": game.board.get_tile_at(player.position).name,
                "message": f"{player.name} is in jail.",
                "can_buy": False,
            }

        dice_value = self.random_port.roll_dice()
        game.last_roll = dice_value

        passed_start = player.move(dice_value, game.board.size())

        if passed_start:
            player.receive_money(self.GO_BONUS)

        tile = game.board.get_tile_at(player.position)

        game.has_rolled_this_turn = True
        game.current_turn_tile_id = tile.tile_id
        game.purchased_this_turn = False
        game.can_buy_current_tile = False

        action_message = self.resolve_tile_action_use_case.execute(game)

        if isinstance(tile, OwnableTile):
            if not tile.is_owned():
                game.can_buy_current_tile = True
            elif tile.owner_name != player.name:
                try:
                    self.pay_rent_use_case.execute(game, dice_value=dice_value)
                except ValueError as error:
                    self.handle_bankruptcy_use_case.execute(game, player)
                    action_message = str(error)

        return {
            "player": player.name,
            "dice_value": dice_value,
            "tile_name": tile.name,
            "message": action_message,
            "can_buy": game.can_buy_current_tile,
        }