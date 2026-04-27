from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.attempt_leave_jail import AttemptLeaveJailUseCase
from monopoly.application.use_cases.handle_bankruptcy import HandleBankruptcyUseCase
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.application.use_cases.resolve_tile_action import ResolveTileActionUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


class PlayTurnUseCase:
    GO_BONUS = Money(200)
    JAIL_POSITION = Position(10)

    def __init__(self, random_port: RandomPort) -> None:
        self.random_port = random_port
        self.resolve_tile_action_use_case = ResolveTileActionUseCase()
        self.pay_rent_use_case = PayRentUseCase()
        self.handle_bankruptcy_use_case = HandleBankruptcyUseCase()
        self.attempt_leave_jail_use_case = AttemptLeaveJailUseCase()

    def execute(self, game: Game) -> dict:
        if game.has_rolled_this_turn:
            raise ValueError("The current player has already rolled this turn.")

        player = game.current_player

        die_one = self.random_port.roll_die()
        die_two = self.random_port.roll_die()
        dice_value = die_one + die_two
        is_double = die_one == die_two

        game.last_roll = dice_value

        if player.in_jail:
            jail_result = self.attempt_leave_jail_use_case.execute(
                game,
                die_one,
                die_two,
            )

            game.has_rolled_this_turn = True
            game.can_buy_current_tile = False
            game.consecutive_doubles_count = 0

            if not jail_result["released"]:
                return {
                    "player": player.name,
                    "dice_value": dice_value,
                    "tile_name": game.board.get_tile_at(player.position).name,
                    "message": jail_result["message"],
                    "can_buy": False,
                }

            return self._move_and_resolve_tile(
                game=game,
                dice_value=dice_value,
                is_double_from_jail=True,
                prefix_message=jail_result["message"],
            )

        if is_double:
            game.consecutive_doubles_count += 1
        else:
            game.consecutive_doubles_count = 0

        if game.consecutive_doubles_count >= 3:
            player.send_to_jail(self.JAIL_POSITION)
            game.has_rolled_this_turn = True
            game.can_buy_current_tile = False
            game.purchased_this_turn = False
            game.current_turn_tile_id = self.JAIL_POSITION.index
            game.consecutive_doubles_count = 0

            return {
                "player": player.name,
                "dice_value": dice_value,
                "tile_name": game.board.get_tile_at(player.position).name,
                "message": f"{player.name} rolled 3 doubles and was sent to jail.",
                "can_buy": False,
            }

        return self._move_and_resolve_tile(
            game=game,
            dice_value=dice_value,
            is_double_from_jail=False,
            prefix_message="",
        )

    def _move_and_resolve_tile(
        self,
        game: Game,
        dice_value: int,
        is_double_from_jail: bool,
        prefix_message: str,
    ) -> dict:
        player = game.current_player

        passed_start = player.move(dice_value, game.board.size())

        if passed_start:
            player.receive_money(self.GO_BONUS)

        tile = game.board.get_tile_at(player.position)

        game.current_turn_tile_id = tile.tile_id
        game.purchased_this_turn = False
        game.can_buy_current_tile = False

        action_message = self.resolve_tile_action_use_case.execute(game)

        tile = game.board.get_tile_at(player.position)
        game.current_turn_tile_id = tile.tile_id

        if isinstance(tile, OwnableTile):
            if not tile.is_owned():
                game.can_buy_current_tile = True
            elif tile.owner_name != player.name:
                try:
                    self.pay_rent_use_case.execute(game, dice_value=dice_value)
                except ValueError as error:
                    self.handle_bankruptcy_use_case.execute(game, player)
                    action_message = str(error)

        if prefix_message:
            action_message = f"{prefix_message} {action_message}"

        is_double = game.last_roll == dice_value and game.consecutive_doubles_count > 0

        if is_double and not is_double_from_jail and not player.in_jail:
            game.has_rolled_this_turn = False
        else:
            game.has_rolled_this_turn = True

        return {
            "player": player.name,
            "dice_value": dice_value,
            "tile_name": tile.name,
            "message": action_message,
            "can_buy": game.can_buy_current_tile,
        }