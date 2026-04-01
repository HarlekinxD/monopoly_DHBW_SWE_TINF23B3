import pytest

from monopoly.application.use_cases.start_game import StartGameUseCase


def test_start_game_with_two_players_creates_game_state() -> None:
    use_case = StartGameUseCase()

    result = use_case.execute(["Alice", "Bob"])

    assert result.is_started is True
    assert result.current_player_index == 0
    assert result.current_player_name == "Alice"
    assert result.board_size == 40
    assert len(result.players) == 2


def test_start_game_with_seven_players_is_allowed() -> None:
    use_case = StartGameUseCase()

    result = use_case.execute(
        ["A", "B", "C", "D", "E", "F", "G"]
    )

    assert len(result.players) == 7


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