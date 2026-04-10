from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_board_has_40_tiles() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    assert game.board.size() == 40


def test_board_returns_tile_at_position() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    tile = game.board.get_tile_at(Position(1))

    assert tile.tile_id == 1
    assert tile.name == "Badstraße"