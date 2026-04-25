import os
from pathlib import Path

from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.check_winner import CheckWinnerUseCase
from monopoly.application.use_cases.end_turn import EndTurnUseCase
from monopoly.application.use_cases.load_game import LoadGameUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.save_game import SaveGameUseCase
from monopoly.application.use_cases.show_game_state import ShowGameStateUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.toggle_view import ToggleViewUseCase
from monopoly.infrastructure.persistence.json_game_repository import JsonGameRepository
from monopoly.infrastructure.rng.python_random_dice import PythonRandomDice
from monopoly.presentation.cli.board_renderer import BoardRenderer
from monopoly.presentation.cli.command_parser import CommandParser
from monopoly.presentation.cli.ownership_renderer import OwnershipRenderer
from monopoly.application.use_cases.pay_jail_fine import PayJailFineUseCase
from monopoly.application.use_cases.build_house import BuildHouseUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.token import Token


class MenuController:
    DEFAULT_SAVE_FILE = "savegame.json"
    TOKEN_SYMBOLS_ASCII: dict[Token, str] = {
        Token.SHOE: "S",
        Token.WHEELBARROW: "W",
        Token.HAT: "H",
        Token.CAR: "A",
        Token.SHIP: "K",
        Token.IRON: "I",
        Token.DOG: "D",
    }

    TOKEN_SYMBOLS_EMOJI: dict[Token, str] = {
        Token.SHOE: "👞",
        Token.WHEELBARROW: "🛒",
        Token.HAT: "🎩",
        Token.CAR: "🚗",
        Token.SHIP: "🚢",
        Token.IRON: "🧺",
        Token.DOG: "🐕",
    }

    def __init__(self) -> None:
        self.start_game_use_case = StartGameUseCase()
        self.buy_property_use_case = BuyPropertyUseCase()
        self.end_turn_use_case = EndTurnUseCase()
        self.show_game_state_use_case = ShowGameStateUseCase()
        self.toggle_view_use_case = ToggleViewUseCase()
        self.play_turn_use_case = PlayTurnUseCase(PythonRandomDice())
        self.check_winner_use_case = CheckWinnerUseCase()

        self.command_parser = CommandParser()
        self.board_renderer = BoardRenderer()
        self.ownership_renderer = OwnershipRenderer()
        self.pay_jail_fine_use_case = PayJailFineUseCase()
        self.build_house_use_case = BuildHouseUseCase()

    def run(self) -> None:
        game = self._create_game()

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
                f"Command (help/show/toggle/roll/buy/build/end/bail/save/load/quit): "
            )

            try:
                command, _ = self.command_parser.parse(raw_command)
            except ValueError as error:
                game.last_message = f"Error: {error}"
                self._render(game)
                continue

            if command == "help":
                game.last_message = (
                    "Commands: help, show, toggle, roll, buy, build, end, bail, save, load, quit"
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
                if game.has_rolled_this_turn:
                    game.last_message = "You already rolled this turn."
                    self._render(game)
                    continue

                try:
                    result = self.play_turn_use_case.execute(game)

                    message = (
                        f"{result['player']} rolled {result['dice_value']} "
                        f"and landed on {result['tile_name']}. {result['message']}"
                    )

                    if result["can_buy"]:
                        message += " This tile can be bought with 'buy'."

                    game.last_message = message

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

            elif command == "build":
                try:
                    game.last_message = self.build_house_use_case.execute(game)
                except ValueError as error:
                    game.last_message = f"Build failed: {error}"
                self._render(game)

            elif command == "end":
                next_player_name = self.end_turn_use_case.execute(game)
                game.last_message = f"Turn ended. Next player: {next_player_name}"
                self._render(game)

            elif command == "save":
                save_file = self._ask_save_file_name("Save file name")
                if save_file is None:
                    game.last_message = "Save aborted."
                else:
                    self._save_game_to_file(game, save_file)
                    game.last_message = f"Game saved to '{save_file}'."
                self._render(game)

            elif command == "load":
                try:
                    should_save_before_load = self._should_save_before_load()
                except ValueError as error:
                    game.last_message = str(error)
                    self._render(game)
                    continue

                if should_save_before_load:
                    save_file = self._ask_save_file_name("Save current game before load")
                    if save_file is None:
                        game.last_message = "Load aborted."
                        self._render(game)
                        continue
                    self._save_game_to_file(game, save_file)

                load_file = self._ask_save_file_name("Load file name")
                if load_file is None:
                    game.last_message = "Load aborted."
                    self._render(game)
                    continue

                try:
                    loaded_game = self._load_game_from_file(load_file)
                except ValueError as error:
                    game.last_message = f"Load failed: {error}"
                    self._render(game)
                    continue

                game = loaded_game
                game.last_message = f"Game loaded from '{load_file}'."
                self._render(game)

            elif command == "quit":
                self._clear_screen()
                print("Goodbye.")
                break

    def _create_game(self) -> Game:
        self._clear_screen()
        print("=== Monopoly CLI ===")

        player_count = int(input("Number of players (2-7): ").strip())
        player_names: list[str] = []

        for index in range(player_count):
            name = input(f"Name of player {index + 1}: ").strip()
            player_names.append(name)

        game = self.start_game_use_case.execute(player_names)
        self._choose_tokens_for_players(game)
        return game

    def _choose_tokens_for_players(self, game: Game) -> None:
        # Jeder Spieler darf seine Figur waehlen.
        available_tokens: list[Token] = [
            Token.SHOE,
            Token.WHEELBARROW,
            Token.HAT,
            Token.CAR,
            Token.SHIP,
            Token.IRON,
            Token.DOG,
        ]

        print("\nChoose tokens:")
        for player in game.players:
            token = self._ask_token_for_player(player.name, available_tokens)
            player.token = token
            available_tokens.remove(token)

    def _ask_token_for_player(self, player_name: str, available_tokens: list[Token]) -> Token:
        while True:
            print(f"\n{player_name}, choose your character:")
            for index, token in enumerate(available_tokens, start=1):
                symbol = self._token_symbols().get(token, "?")
                self._print_token_preview(token)
                print(f"{index}. {symbol} {token.value}")

            raw_choice = input("Selection: ").strip()

            if not raw_choice.isdigit():
                print("Please enter a number.")
                continue

            selected_index = int(raw_choice)
            if selected_index < 1 or selected_index > len(available_tokens):
                print("Invalid choice. Try again.")
                continue

            return available_tokens[selected_index - 1]

    def _token_symbols(self) -> dict[Token, str]:
        style = os.environ.get("MONOPOLY_TOKEN_STYLE", "ascii").strip().lower()
        if style == "emoji":
            return self.TOKEN_SYMBOLS_EMOJI
        return self.TOKEN_SYMBOLS_ASCII

    def _shoe_preview(self) -> str:
        return (
            "    ,___ ,__\n"
            "     )  `\\  `\\\n"
            "    (   _ '-._'-._\n"
            "      )_( \\____)___)"
        )

    def _print_token_preview(self, token: Token) -> None:
        preview = self._token_preview_lines(token)
        for line in preview:
            print(line)

    def _token_preview_lines(self, token: Token) -> list[str]:
        if token == Token.SHOE:
            return [
                "    ,___ ,__",
                "     )  `\\  `\\",
                "    (   _ '-._'-._",
                "      )_( \\____)___)",
            ]

        if token == Token.WHEELBARROW:
            return [
                "       ____",
                "  ____/____\\_",
                " /_____/  o  /)",
                "   o      o",
            ]

        if token == Token.HAT:
            return [
                "      ____",
                "   __/____\\__",
                "      \____/",
                "       /__\\",
            ]

        if token == Token.CAR:
            return [
                "    ______",
                " __/[] []\\__",
                "|_  _  _  _  |",
                "  O        O",
            ]

        if token == Token.SHIP:
            return [
                "        |\",
                "       /| \",
                "  _____/ |__\\_____",
                "  \______________ /",
            ]

        if token == Token.IRON:
            return [
                "      _______",
                "     / ____  \",
                "    /_/___/\__\\",
                "       ||  ||",
            ]

        if token == Token.DOG:
            return [
                "   / \__",
                "  (    @\\___",
                "  /         O",
                " /   (_____ /",
            ]

        return ["    [no preview]"]

    def _render(self, game: Game) -> None:
        self._clear_screen()
        game = self.show_game_state_use_case.execute(game)

        if game.active_view == "board":
            print(self.board_renderer.render(game))
        else:
            print(self.ownership_renderer.render(game))

    def _clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _should_save_before_load(self) -> bool:
        # Kleiner dialog vor dem laden vom neuen stand
        answer = input("Save current game before load? (y/n/cancel): ").strip().lower()

        if answer in {"y", "yes", "j", "ja"}:
            return True
        if answer in {"n", "no", "nein"}:
            return False
        if answer in {"c", "cancel", "abbrechen"}:
            raise ValueError("Load canceled by user.")

        raise ValueError("Please answer with y, n or cancel.")

    def _ask_save_file_name(self, label: str) -> str | None:
        # String eingabe fuer dateiname, cancel ist erlaubt
        raw_name = input(f"{label} (default: {self.DEFAULT_SAVE_FILE}, type 'cancel' to abort): ").strip()

        if not raw_name:
            return self.DEFAULT_SAVE_FILE
        if raw_name.lower() in {"c", "cancel", "abbrechen"}:
            return None

        if not raw_name.endswith(".json"):
            return f"{raw_name}.json"
        return raw_name

    def _save_game_to_file(self, game: Game, save_file: str) -> None:
        repository = JsonGameRepository(Path("saves") / save_file)
        SaveGameUseCase(repository).execute(game)

    def _load_game_from_file(self, save_file: str) -> Game:
        repository = JsonGameRepository(Path("saves") / save_file)
        return LoadGameUseCase(repository).execute()