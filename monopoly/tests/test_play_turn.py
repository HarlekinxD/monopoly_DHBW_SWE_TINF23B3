from monopoly.application.ports.random_port import RandomPort
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


class FakeRandomPort(RandomPort):
    def __init__(self, value: int) -> None:
        self.value = value

    def roll_dice(self) -> int:
        return self.value


def test_play_turn_moves_player() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort(4))

    result = use_case.execute(game)

    assert result["dice_value"] == 4
    assert game.current_player.position.index == 4