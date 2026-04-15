import pytest

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.domain.value_objects.position import Position
from monopoly.domain.value_objects.money import Money

from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


class FakeRandomPort(RandomPort):
    def __init__(self, value: int) -> None:
        self.value = value

    def roll_dice(self) -> int:
        return self.value


def test_player_does_not_pay_rent_to_self() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    PlayTurnUseCase(FakeRandomPort(1)).execute(game)
    BuyPropertyUseCase().execute(game)

    balance_before = alice.balance.amount

    PayRentUseCase().execute(game, dice_value=1)

    assert alice.balance.amount == balance_before

def test_player_pays_rent_to_owner():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.current_player
    alice.move_to(Position(1))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 1

    BuyPropertyUseCase().execute(game)

    game.next_player()
    bob = game.current_player
    bob.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert bob.balance.amount == 1498
    assert alice.balance.amount == 1442


def test_no_rent_if_owner_lands_on_own_tile():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.current_player
    alice.move_to(Position(1))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 1

    BuyPropertyUseCase().execute(game)

    alice.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert alice.balance.amount == 1500 - 60


def test_utility_requires_dice_value():
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.current_player
    alice.move_to(Position(12))  # utility
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 12

    BuyPropertyUseCase().execute(game)

    game.next_player()
    bob = game.current_player
    bob.move_to(Position(12))

    with pytest.raises(ValueError):
        PayRentUseCase().execute(game)

def test_player_does_not_pay_rent_to_self() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    PlayTurnUseCase(FakeRandomPort(1)).execute(game)
    BuyPropertyUseCase().execute(game)

    balance_before = alice.balance.amount

    PayRentUseCase().execute(game, dice_value=1)

    assert alice.balance.amount == balance_before