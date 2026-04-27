import os

from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.check_winner import CheckWinnerUseCase
from monopoly.application.use_cases.end_turn import EndTurnUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.show_game_state import ShowGameStateUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.toggle_view import ToggleViewUseCase
from monopoly.application.use_cases.save_game import SaveGameUseCase
from monopoly.application.use_cases.load_game import LoadGameUseCase
from monopoly.application.use_cases.sell_building import SellBuildingUseCase
from monopoly.infrastructure.rng.python_random_dice import PythonRandomDice
from monopoly.infrastructure.persistence.json_game_repository import JsonGameRepository
from monopoly.presentation.cli.board_renderer import BoardRenderer
from monopoly.presentation.cli.command_parser import CommandParser
from monopoly.presentation.cli.ownership_renderer import OwnershipRenderer
from monopoly.application.use_cases.pay_jail_fine import PayJailFineUseCase
from monopoly.application.use_cases.build_house import BuildHouseUseCase
from monopoly.application.use_cases.use_jail_free_card import UseJailFreeCardUseCase


class MenuController:
    def __init__(self) -> None:
        self.start_game_use_case = StartGameUseCase()
        self.buy_property_use_case = BuyPropertyUseCase()
        self.end_turn_use_case = EndTurnUseCase()
        self.show_game_state_use_case = ShowGameStateUseCase()
        self.toggle_view_use_case = ToggleViewUseCase()
        self.play_turn_use_case = PlayTurnUseCase(PythonRandomDice())
        self.check_winner_use_case = CheckWinnerUseCase()
        self.pay_jail_fine_use_case = PayJailFineUseCase()
        self.build_house_use_case = BuildHouseUseCase()
        self.sell_building_use_case = SellBuildingUseCase()
        self.use_jail_free_card_use_case = UseJailFreeCardUseCase()

        # Persistence - mit saves/ Verzeichnis
        save_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "saves", "game_save.json")
        self.game_repository = JsonGameRepository(save_file_path)
        self.save_game_use_case = SaveGameUseCase(self.game_repository)
        self.load_game_use_case = LoadGameUseCase(self.game_repository)

        self.command_parser = CommandParser()
        self.board_renderer = BoardRenderer()
        self.ownership_renderer = OwnershipRenderer()

    def run(self) -> None:
        game = self._create_game()
        has_rolled = False

        game.last_message = "Game created successfully."
        self._render(game)

        while True:
            winner = self.check_winner_use_case.execute(game)
            if winner is not None:
                ranking = self.check_winner_use_case.get_ranking(game)
                self._clear_screen()
                print(f"Winner: {winner}")
                print("Final ranking:")
                for index, player_name in enumerate(ranking, start=1):
                    print(f"{index}. {player_name}")
                break

            raw_command = input(
                f"\nCurrent player: {game.current_player.name} | "
                f"Command (help/show/toggle/roll/buy/build/sell/end/bail/use_card/save/load/quit): "
            )

            try:
                command, _ = self.command_parser.parse(raw_command)
            except ValueError as error:
                game.last_message = f"Error: {error}"
                self._render(game)
                continue

            if command == "help":
                game.last_message = (
                    "Commands: help, show, toggle, roll, buy, build, sell, end, bail, use_card, save, load, quit"
                )
                self._render(game)

            elif command == "show":
                game.last_message = "Refreshed current view."
                self._render(game)

            elif command == "toggle":
                self.toggle_view_use_case.execute(game)
                game.last_message = f"Switched view to '{game.active_view}'."
                self._render(game)

            elif command == "roll":
                if has_rolled:
                    game.last_message = "You already rolled this turn."
                    self._render(game)
                    continue

                try:
                    result = self.play_turn_use_case.execute(game)

                    dice_display = f"{result.get('die_one', '-')}/{result.get('die_two', '-')}"
                    message = (
                        f"{result['player']} rolled {result['dice_value']} "
                        f"({dice_display}) and landed on {result['tile_name']}. {result['message']}"
                    )

                    if result.get("is_double"):
                        if game.consecutive_doubles_count >= 3:
                            message += " You rolled 3 doubles and were sent to jail!"
                        else:
                            message += " Pasch! You may roll again."

                    if result["can_buy"]:
                        message += " This tile can be bought with 'buy'."

                    game.last_message = message

                    # Sync the has_rolled flag with game state after roll
                    has_rolled = game.has_rolled_this_turn

                except ValueError as error:
                    game.last_message = f"Turn failed: {error}"

                self._render(game)

            elif command == "buy":
                try:
                    self.buy_property_use_case.execute(game)
                    game.last_message = "Property purchased successfully."
                except ValueError as error:
                    game.last_message = f"Buy failed: {error}"

                self._render(game)

            elif command == "bail":
                try:
                    game.last_message = self.pay_jail_fine_use_case.execute(game)
                except ValueError as error:
                    game.last_message = f"Bail failed: {error}"
                self._render(game)

            elif command == "use_card":
                try:
                    game.last_message = self.use_jail_free_card_use_case.execute(game)
                except ValueError as error:
                    game.last_message = f"Use card failed: {error}"
                self._render(game)

            elif command == "build":
                try:
                    game.last_message = self.build_house_use_case.execute(game)
                except ValueError as error:
                    game.last_message = f"Build failed: {error}"
                self._render(game)

            elif command == "sell":
                try:
                    game.last_message = self.sell_building_use_case.execute(game)
                except ValueError as error:
                    game.last_message = f"Sell failed: {error}"
                self._render(game)

            elif command == "save":
                try:
                    self.save_game_use_case.execute(game)
                    game.last_message = "Game saved successfully."
                except Exception as error:
                    game.last_message = f"Save failed: {error}"
                self._render(game)

            elif command == "load":
                try:
                    game = self.load_game_use_case.execute()
                    has_rolled = game.has_rolled_this_turn
                    game.last_message = "Game loaded successfully."
                except Exception as error:
                    game.last_message = f"Load failed: {error}"
                self._render(game)

            elif command == "end":
                next_player_name = self.end_turn_use_case.execute(game)
                has_rolled = False
                game.last_message = f"Turn ended. Next player: {next_player_name}"
                self._render(game)

            elif command == "quit":
                self._clear_screen()
                print("Goodbye.")
                break

    def _create_game(self):
        self._clear_screen()
        print("=== Monopoly CLI ===")

        player_count = int(input("Number of players (2-7): ").strip())
        player_names: list[str] = []

        for index in range(player_count):
            name = input(f"Name of player {index + 1}: ").strip()
            player_names.append(name)

        return self.start_game_use_case.execute(player_names)

    def _render(self, game) -> None:
        self._clear_screen()
        game = self.show_game_state_use_case.execute(game)

        if game.active_view == "board":
            print(self.board_renderer.render(game))
        else:
            print(self.ownership_renderer.render(game))

        if game.last_message:
            print()
            print(game.last_message)

    def _clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")