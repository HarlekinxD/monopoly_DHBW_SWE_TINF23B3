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


def test_player_cannot_roll_twice_in_same_turn() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)

    with pytest.raises(ValueError, match="already rolled"):
        PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)


def test_turn_state_resets_after_end_turn() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)

    assert game.has_rolled_this_turn is True

    game.next_player()

    assert game.has_rolled_this_turn is False
    assert game.can_buy_current_tile is False
    assert game.purchased_this_turn is False
    assert game.current_turn_tile_id is None


def test_player_cannot_buy_twice_in_same_turn() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)

    BuyPropertyUseCase().execute(game)

    with pytest.raises(ValueError, match="already bought"):
        BuyPropertyUseCase().execute(game)