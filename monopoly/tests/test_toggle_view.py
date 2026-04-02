from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.toggle_view import ToggleViewUseCase


def test_toggle_view_switches_from_board_to_ownership() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    result = ToggleViewUseCase().execute(game)

    assert result == "ownership"
    assert game.active_view == "ownership"


def test_toggle_view_switches_back_to_board() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = ToggleViewUseCase()

    use_case.execute(game)
    result = use_case.execute(game)

    assert result == "board"
    assert game.active_view == "board"