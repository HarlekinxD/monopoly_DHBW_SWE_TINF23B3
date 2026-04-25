import pytest

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.token import Token


def test_start_game_with_two_players_creates_game() -> None:
    use_case = StartGameUseCase()

    game = use_case.execute(["Alice", "Bob"])

    assert game.is_started is True
    assert game.current_player_index == 0
    assert game.current_player.name == "Alice"
    assert game.board.size() == 40
    assert len(game.players) == 2


def test_start_game_with_seven_players_is_allowed() -> None:
    use_case = StartGameUseCase()

    game = use_case.execute(["A", "B", "C", "D", "E", "F", "G"])

    assert len(game.players) == 7


def test_start_game_with_one_player_raises_error() -> None:
    use_case = StartGameUseCase()

    with pytest.raises(ValueError, match="2 to 7 players"):
        use_case.execute(["Alice"])


def test_start_game_with_eight_players_raises_error() -> None:
    use_case = StartGameUseCase()

    with pytest.raises(ValueError, match="2 to 7 players"):
        use_case.execute(["A", "B", "C", "D", "E", "F", "G", "H"])


def test_start_game_rejects_empty_player_name() -> None:
    use_case = StartGameUseCase()

    with pytest.raises(ValueError, match="must not be empty"):
        use_case.execute(["Alice", "   "])


def test_start_game_rejects_duplicate_names() -> None:
    use_case = StartGameUseCase()

    with pytest.raises(ValueError, match="must be unique"):
        use_case.execute(["Alice", "Alice"])


def test_start_game_assigns_default_tokens_in_order() -> None:
    use_case = StartGameUseCase()

    game = use_case.execute(["A", "B", "C", "D", "E", "F", "G"])

    assert game.players[0].token == Token.SHOE
    assert game.players[1].token == Token.WHEELBARROW
    assert game.players[2].token == Token.HAT
    assert game.players[3].token == Token.CAR
    assert game.players[4].token == Token.SHIP
    assert game.players[5].token == Token.IRON
    assert game.players[6].token == Token.DOG