from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


class FakeRandomPort:
    def __init__(self, values: list[int]) -> None:
        self.values = values
        self.index = 0

    def roll_die(self) -> int:
        value = self.values[self.index]
        self.index += 1
        return value


def test_player_pays_after_three_failed_jail_attempts_and_moves() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.send_to_jail(Position(10))

    PlayTurnUseCase(FakeRandomPort([1, 2])).execute(game)
    game.next_player()
    game.next_player()

    PlayTurnUseCase(FakeRandomPort([2, 3])).execute(game)
    game.next_player()
    game.next_player()

    result = PlayTurnUseCase(FakeRandomPort([4, 5])).execute(game)

    assert player.in_jail is False
    assert player.balance.amount == 1450
    assert player.position.index == 19
    assert result["dice_value"] == 9