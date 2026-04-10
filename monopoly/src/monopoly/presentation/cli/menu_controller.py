from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.end_turn import EndTurnUseCase
from monopoly.application.use_cases.show_game_state import ShowGameStateUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.toggle_view import ToggleViewUseCase
from monopoly.presentation.cli.board_renderer import BoardRenderer
from monopoly.presentation.cli.command_parser import CommandParser
from monopoly.presentation.cli.ownership_renderer import OwnershipRenderer


class MenuController:
    def __init__(self) -> None:
        self.start_game_use_case = StartGameUseCase()
        self.buy_property_use_case = BuyPropertyUseCase()
        self.end_turn_use_case = EndTurnUseCase()
        self.show_game_state_use_case = ShowGameStateUseCase()
        self.toggle_view_use_case = ToggleViewUseCase()

        self.command_parser = CommandParser()
        self.board_renderer = BoardRenderer()
        self.ownership_renderer = OwnershipRenderer()

    def run(self) -> None:
        game = self._create_game()

        print("\nGame created successfully.")
        self._render(game)

        while True:
            raw_command = input(
                f"\nCurrent player: {game.current_player.name} | Command (help/show/toggle/buy/end/quit): "
            )

            try:
                command, arguments = self.command_parser.parse(raw_command)
            except ValueError as error:
                print(f"Error: {error}")
                continue

            if command == "help":
                self._show_help()
            elif command == "show":
                self._render(game)
            elif command == "toggle":
                self.toggle_view_use_case.execute(game)
                self._render(game)
            elif command == "buy":
                try:
                    self.buy_property_use_case.execute(game)
                    print("Property purchased successfully.")
                except ValueError as error:
                    print(f"Buy failed: {error}")
                self._render(game)
            elif command == "end":
                next_player_name = self.end_turn_use_case.execute(game)
                print(f"Turn ended. Next player: {next_player_name}")
                self._render(game)
            elif command == "roll":
                print("Roll is not connected yet. This will be integrated with play-turn.")
            elif command == "quit":
                print("Goodbye.")
                break
            else:
                print(f"Command '{command}' is not implemented yet.")

    def _create_game(self):
        player_count = int(input("Number of players (2-7): ").strip())
        player_names: list[str] = []

        for index in range(player_count):
            name = input(f"Name of player {index + 1}: ").strip()
            player_names.append(name)

        return self.start_game_use_case.execute(player_names)

    def _render(self, game) -> None:
        game = self.show_game_state_use_case.execute(game)

        if game.active_view == "board":
            print(self.board_renderer.render(game))
        else:
            print(self.ownership_renderer.render(game))

    def _show_help(self) -> None:
        print("Available commands:")
        print("- help   : show available commands")
        print("- show   : show the current view")
        print("- toggle : switch between board and ownership view")
        print("- buy    : buy the current tile if possible")
        print("- end    : end the current player's turn")
        print("- roll   : placeholder until play-turn is integrated")
        print("- quit   : exit the game")