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

class FakeRandomPort:
    def __init__(self, values: list[int]) -> None:
        self.values = values
        self.index = 0

    def roll_die(self) -> int:
        value = self.values[self.index]
        self.index += 1
        return value


def test_player_does_not_pay_rent_to_self() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)  # tile 3
    BuyPropertyUseCase().execute(game)

    balance_before = alice.balance.amount

    PayRentUseCase().execute(game, dice_value=3)

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

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)  # tile 3
    BuyPropertyUseCase().execute(game)

    balance_before = alice.balance.amount

    PayRentUseCase().execute(game, dice_value=1)

    assert alice.balance.amount == balance_before


def test_property_without_full_color_group_uses_normal_base_rent() -> None:
    # Alice besitzt nur eine lila strasse (tile 1), also keine verdopplung.
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

    # Grundmiete auf Badstrasse ist 2.
    assert bob.balance.amount == 1498
    assert alice.balance.amount == 1442


def test_property_with_full_color_group_doubles_base_rent() -> None:
    # Alice besitzt beide lila strassen (1 und 3), ohne haeuser.
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    alice.move_to(Position(1))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 1
    BuyPropertyUseCase().execute(game)

    alice.move_to(Position(3))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.purchased_this_turn = False
    game.current_turn_tile_id = 3
    BuyPropertyUseCase().execute(game)

    game.next_player()
    bob = game.current_player
    bob.move_to(Position(1))

    PayRentUseCase().execute(game)

    # Grundmiete 2 wird auf 4 verdoppelt.
    assert bob.balance.amount == 1496
    assert alice.balance.amount == 1384


def test_utility_rent_one_utility_uses_multiplier_4() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    # Alice buys the utility at position 12
    alice.move_to(Position(12))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 12
    BuyPropertyUseCase().execute(game)

    # Bob lands on the utility and pays rent based on dice_value * 4
    game.next_player()
    bob = game.current_player
    bob.move_to(Position(12))

    dice_value = 3
    PayRentUseCase().execute(game, dice_value=dice_value)

    expected_rent = dice_value * 4
    assert bob.balance.amount == 1500 - expected_rent
    # Alice paid the utility price then received rent
    utility_price = game.board.get_tile_at(Position(12)).price.amount
    assert alice.balance.amount == 1500 - utility_price + expected_rent


def test_utility_rent_two_utilities_uses_multiplier_10() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    # Alice buys both utilities (12 and 28)
    alice.move_to(Position(12))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.current_turn_tile_id = 12
    BuyPropertyUseCase().execute(game)

    alice.move_to(Position(28))
    game.has_rolled_this_turn = True
    game.can_buy_current_tile = True
    game.purchased_this_turn = False
    game.current_turn_tile_id = 28
    BuyPropertyUseCase().execute(game)

    # Bob lands on one utility
    game.next_player()
    bob = game.current_player
    bob.move_to(Position(12))

    dice_value = 5
    PayRentUseCase().execute(game, dice_value=dice_value)

    expected_rent = dice_value * 10
    assert bob.balance.amount == 1500 - expected_rent


def test_railroad_rent_four_railroads_flat_200() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    # Buy all four railroads (positions 5,15,25,35)
    for pos in (5, 15, 25, 35):
        alice.move_to(Position(pos))
        game.has_rolled_this_turn = True
        game.can_buy_current_tile = True
        game.purchased_this_turn = False
        game.current_turn_tile_id = pos
        BuyPropertyUseCase().execute(game)

    # Bob lands on a railroad and should pay flat 200
    game.next_player()
    bob = game.current_player
    bob.move_to(Position(5))

    PayRentUseCase().execute(game)

    assert bob.balance.amount == 1500 - 200
    assert alice.balance.amount == 1500 - sum(game.board.get_tile_at(Position(p)).price.amount for p in (5,15,25,35)) + 200