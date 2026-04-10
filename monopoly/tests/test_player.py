from monopoly.domain.entities.player import Player
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


def test_player_moves_to_new_position() -> None:
    player = Player(name="Alice")
    player.move_to(Position(5))

    assert player.position.index == 5


def test_player_receives_money() -> None:
    player = Player(name="Alice")
    player.receive_money(Money(100))

    assert player.balance.amount == 1600


def test_player_adds_owned_tile() -> None:
    player = Player(name="Alice")
    player.add_owned_tile(3)

    assert player.owns_tile(3) is True