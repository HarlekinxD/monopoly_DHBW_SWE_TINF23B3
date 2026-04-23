from monopoly.application.ports.random_port import RandomPort
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


def test_play_turn_moves_player() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([2, 2]))  # total = 4

    result = use_case.execute(game)

    assert result["dice_value"] == 4
    assert game.current_player.position.index == 4