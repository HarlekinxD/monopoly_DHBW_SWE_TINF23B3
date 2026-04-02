import pytest

from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


def test_player_can_buy_an_unowned_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(1))  # Badstraße

    BuyPropertyUseCase().execute(game)

    tile = game.board.get_tile_at(player.position)

    assert tile.owner_name == "Alice"
    assert 1 in player.owned_tile_ids
    assert player.balance == Money(1440)


def test_cannot_buy_a_non_ownable_tile() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(0))  # LOS

    with pytest.raises(ValueError, match="cannot be bought"):
        BuyPropertyUseCase().execute(game)


def test_cannot_buy_an_already_owned_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(1))

    use_case = BuyPropertyUseCase()
    use_case.execute(game)

    with pytest.raises(ValueError, match="already owned"):
        use_case.execute(game)


def test_cannot_buy_property_without_enough_money() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.move_to(Position(39))  # Schlossallee, cost 400
    player.balance = Money(100)

    with pytest.raises(ValueError, match="enough money"):
        BuyPropertyUseCase().execute(game)