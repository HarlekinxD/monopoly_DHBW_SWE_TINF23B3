from monopoly.application.use_cases.check_winner import CheckWinnerUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


def test_no_winner_when_multiple_players_active() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    result = CheckWinnerUseCase().execute(game)

    assert result is None


def test_winner_when_only_one_player_left() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    game.players[1].is_bankrupt = True

    result = CheckWinnerUseCase().execute(game)

    assert result == "Alice"