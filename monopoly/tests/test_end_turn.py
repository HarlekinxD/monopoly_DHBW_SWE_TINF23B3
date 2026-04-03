from monopoly.application.use_cases.end_turn import EndTurnUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


def test_end_turn_switches_to_next_player() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])

    result = EndTurnUseCase().execute(game)

    assert result == "Bob"
    assert game.current_player.name == "Bob"
    assert game.current_player_index == 1


def test_end_turn_wraps_back_to_first_player() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])
    game.current_player_index = 2

    result = EndTurnUseCase().execute(game)

    assert result == "Alice"
    assert game.current_player.name == "Alice"
    assert game.current_player_index == 0