from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.presentation.cli.menu_controller import MenuController


def main() -> None:
    print("=== Monopoly CLI ===")
    controller = MenuController()
    controller.run()


if __name__ == "__main__":
    main()


def main() -> None:
    print("=== Monopoly CLI ===")
    print("Start a new game")

    player_count = int(input("Number of players (2-7): ").strip())

    player_names: list[str] = []
    for index in range(player_count):
        name = input(f"Name of player {index + 1}: ").strip()
        player_names.append(name)

    use_case = StartGameUseCase()
    game_state = use_case.execute(player_names)

    print("\nGame created successfully.")
    print(f"Current player: {game_state.current_player_name}")
    print(f"Board size: {game_state.board_size}")
    print("Players:")
    for player in game_state.players:
        print(
            f"- {player.name} | balance={player.balance} | "
            f"position={player.position} | in_jail={player.is_in_jail}"
        )


if __name__ == "__main__":
    main()