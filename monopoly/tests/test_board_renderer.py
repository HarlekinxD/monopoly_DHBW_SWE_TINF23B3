from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.presentation.cli.board_renderer import BoardRenderer


def test_board_renderer_contains_board_title() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    renderer = BoardRenderer()

    result = renderer.render(game)

    assert "MONOPOLY" in result


def test_board_renderer_contains_corner_tiles() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    renderer = BoardRenderer()

    result = renderer.render(game)

    assert "LOS" in result
    assert "Schlossallee" in result or "Schloss" in result


def test_board_renderer_contains_player_positions() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    renderer = BoardRenderer()

    result = renderer.render(game)

    assert "A" in result or "B" in result