from monopoly.application.use_cases.start_game import StartGameUseCase


def test_bankrupt_player_is_skipped_in_turn_order() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])

    game.players[1].is_bankrupt = True
    game.eliminate_player(game.players[1])

    game.next_player()

    assert game.current_player.name == "Charlie"

    game.next_player()

    assert game.current_player.name == "Alice"