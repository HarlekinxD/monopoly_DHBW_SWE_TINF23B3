from monopoly.infrastructure.board_factory import create_standard_board


def test_standard_board_has_40_tiles() -> None:
    board = create_standard_board()

    assert board.size() == 40


def test_standard_board_starts_with_go() -> None:
    board = create_standard_board()

    assert board.tiles[0].name == "LOS"


def test_standard_board_ends_with_schlossallee() -> None:
    board = create_standard_board()

    assert board.tiles[39].name == "Schlossallee"