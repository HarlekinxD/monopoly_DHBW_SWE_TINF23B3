import pytest

from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
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


def test_cannot_buy_before_roll() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    with pytest.raises(ValueError, match="cannot buy"):
        BuyPropertyUseCase().execute(game)


def test_player_can_buy_only_once_per_turn() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)  # lands on tile 3

    use_case = BuyPropertyUseCase()
    use_case.execute(game)

    with pytest.raises(ValueError, match="already bought"):
        use_case.execute(game)


def test_cannot_buy_owned_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)  # Alice -> tile 3
    BuyPropertyUseCase().execute(game)

    game.next_player()
    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)  # Bob -> tile 3

    with pytest.raises(ValueError, match="cannot buy"):
        BuyPropertyUseCase().execute(game)