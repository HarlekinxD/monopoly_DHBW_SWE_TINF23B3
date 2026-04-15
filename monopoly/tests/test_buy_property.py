import pytest

from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


class FakeRandomPort(RandomPort):
    def __init__(self, value: int) -> None:
        self.value = value

    def roll_dice(self) -> int:
        return self.value


def test_cannot_buy_before_roll() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    with pytest.raises(ValueError, match="must roll before"):
        BuyPropertyUseCase().execute(game)


def test_player_can_buy_only_once_per_turn() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    PlayTurnUseCase(FakeRandomPort(1)).execute(game)  # lands on tile 1

    use_case = BuyPropertyUseCase()
    use_case.execute(game)

    with pytest.raises(ValueError, match="already bought"):
        use_case.execute(game)


def test_cannot_buy_owned_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    PlayTurnUseCase(FakeRandomPort(1)).execute(game)
    BuyPropertyUseCase().execute(game)

    game.next_player()
    PlayTurnUseCase(FakeRandomPort(1)).execute(game)

    with pytest.raises(ValueError, match="cannot be bought"):
        BuyPropertyUseCase().execute(game)