from monopoly.application.use_cases.resolve_tile_action import ResolveTileActionUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


def test_tax_tile_reduces_player_balance() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(4))  # Einkommenssteuer

    result = ResolveTileActionUseCase().execute(game)

    assert "paid tax" in result
    assert player.balance == Money(1300)


def test_go_to_jail_moves_player_to_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(30))  # Gehe ins Gefängnis

    result = ResolveTileActionUseCase().execute(game)

    assert "sent to jail" in result
    assert player.position.index == 10
    assert player.in_jail is True


def test_free_parking_has_no_effect() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(20))  # Frei Parken

    result = ResolveTileActionUseCase().execute(game)

    assert "Free Parking" in result
    assert player.position.index == 20