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

    def execute(self, game: Game) -> dict[str, str | int | bool]:
        if game.has_rolled_this_turn:
            raise ValueError("The current player has already rolled this turn.")

        player = game.current_player
        started_turn_in_jail = player.in_jail

        die_one = self.random_port.roll_die()
        die_two = self.random_port.roll_die()
        dice_value = die_one + die_two
        rolled_doubles = die_one == die_two
        game.last_roll = dice_value

        if player.in_jail:
            jail_result = self.attempt_leave_jail_use_case.execute(game, die_one, die_two)
            game.consecutive_doubles_count = 0

            game.has_rolled_this_turn = True
            game.can_buy_current_tile = False

            if not jail_result["released"]:
                return {
                    "player": player.name,
                    "dice_value": dice_value,
                    "tile_name": game.board.get_tile_at(player.position).name,
                    "message": jail_result["message"],
                    "can_buy": False,
                }

        # Pasch-Zaehler nur fuer normale turns (nicht jail-turn)
        if not started_turn_in_jail:
            if rolled_doubles:
                game.consecutive_doubles_count += 1
            else:
                game.consecutive_doubles_count = 0

            if game.consecutive_doubles_count >= 3:
                # 3x Pasch am stueck -> direkt ins Gefaengnis
                player.send_to_jail(self.JAIL_POSITION)
                game.has_rolled_this_turn = True
                game.can_buy_current_tile = False
                game.current_turn_tile_id = player.position.index
                game.purchased_this_turn = False
                game.consecutive_doubles_count = 0

                return {
                    "player": player.name,
                    "dice_value": dice_value,
                    "tile_name": game.board.get_tile_at(player.position).name,
                    "message": f"{player.name} rolled 3 doubles in a row and was sent to jail.",
                    "can_buy": False,
                }

        passed_start = player.move(dice_value, game.board.size())

        if passed_start:
            player.receive_money(self.GO_BONUS)

        tile = game.board.get_tile_at(player.position)

        # Bei Pasch darf man nochmal rollen (ausser jail-turn)
        game.has_rolled_this_turn = not (rolled_doubles and not started_turn_in_jail)
        game.current_turn_tile_id = tile.tile_id
        game.purchased_this_turn = False
        game.can_buy_current_tile = False

        action_message = self.resolve_tile_action_use_case.execute(game)

        # Wichtig: Sonderfelder können die Position geändert haben
        tile = game.board.get_tile_at(player.position)
        game.current_turn_tile_id = tile.tile_id

        # Falls man auf "Gehe ins Gefaengnis" kam, endet der Zug hier.
        if player.in_jail:
            game.has_rolled_this_turn = True
            game.consecutive_doubles_count = 0
            game.can_buy_current_tile = False

        if isinstance(tile, OwnableTile):
            if not tile.is_owned():
                game.can_buy_current_tile = True
            elif tile.owner_name != player.name:
                try:
                    self.pay_rent_use_case.execute(game, dice_value=dice_value)
                except ValueError as error:
                    self.handle_bankruptcy_use_case.execute(game, player)
                    action_message = str(error)

        if rolled_doubles and not started_turn_in_jail and not player.in_jail:
            action_message = f"{action_message} Rolled doubles: you may roll again."

        return {
            "player": player.name,
            "dice_value": dice_value,
            "tile_name": tile.name,
            "message": action_message,
            "can_buy": game.can_buy_current_tile,
        }