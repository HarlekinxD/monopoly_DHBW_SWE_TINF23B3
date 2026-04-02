import pytest

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.domain.value_objects.position import Position
from monopoly.domain.value_objects.money import Money


def test_player_pays_rent_to_owner():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    # Alice buys Badstraße
    alice = game.current_player
    alice.move_to(Position(1))
    BuyPropertyUseCase().execute(game)

    # Bob lands on it
    game.next_player()
    bob = game.current_player
    bob.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert bob.balance.amount == 1498
    assert alice.balance.amount == 1442


def test_no_rent_if_unowned():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    bob = game.current_player
    bob.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert bob.balance == Money(1500)


def test_no_rent_if_owner_lands_on_own_tile():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.current_player
    alice.move_to(Position(1))
    BuyPropertyUseCase().execute(game)

    alice.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert alice.balance.amount == 1500 - 60


def test_utility_requires_dice_value():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.current_player
    alice.move_to(Position(12))  # utility
    BuyPropertyUseCase().execute(game)

    game.next_player()
    bob = game.current_player
    bob.move_to(Position(12))

    with pytest.raises(ValueError):
        PayRentUseCase().execute(game)