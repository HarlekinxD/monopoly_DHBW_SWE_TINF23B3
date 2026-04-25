from monopoly.application.ports.random_port import RandomPort
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


def test_play_turn_moves_player() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([2, 2]))  # total = 4

    result = use_case.execute(game)

    assert result["dice_value"] == 4
    assert game.current_player.position.index == 4


def test_doubles_allow_second_roll_in_same_turn() -> None:
    # 1. Roll ist Pasch, 2. Roll ist kein Pasch
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([3, 3, 1, 2]))

    first_result = use_case.execute(game)

    assert first_result["dice_value"] == 6
    assert game.current_player.position.index == 6
    assert game.has_rolled_this_turn is False

    second_result = use_case.execute(game)

    assert second_result["dice_value"] == 3
    assert game.current_player.position.index == 9
    assert game.has_rolled_this_turn is True


def test_three_doubles_in_a_row_send_player_to_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 1, 2, 2, 3, 3]))

    use_case.execute(game)
    use_case.execute(game)
    result = use_case.execute(game)

    assert game.current_player.in_jail is True
    assert game.current_player.position.index == 10
    assert game.has_rolled_this_turn is True
    assert game.consecutive_doubles_count == 0
    assert "3 doubles" in str(result["message"])


def test_normal_tile_action_happens_before_extra_roll() -> None:
    # Pasch 2+2 landet auf Steuerfeld (tile 4), Steuer muss erst passieren
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([2, 2]))

    use_case.execute(game)

    assert game.current_player.position.index == 4
    assert game.current_player.balance.amount == 1300
    assert game.has_rolled_this_turn is False


def test_doubles_counter_resets_after_non_double() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 1, 1, 2]))

    use_case.execute(game)
    assert game.consecutive_doubles_count == 1

    use_case.execute(game)
    assert game.consecutive_doubles_count == 0


def test_jail_release_by_doubles_does_not_grant_extra_roll() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    game.current_player.send_to_jail(Position(10))
    use_case = PlayTurnUseCase(FakeRandomPort([4, 4]))

    result = use_case.execute(game)

    assert game.current_player.in_jail is False
    assert game.has_rolled_this_turn is True
    assert game.consecutive_doubles_count == 0
    assert result["dice_value"] == 8


def test_player_may_roll_again_after_double() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([2, 2, 1, 2]))

    use_case.execute(game)

    # Nach Pasch darf nochmal gewuerfelt werden.
    assert game.has_rolled_this_turn is False

    use_case.execute(game)
    assert game.has_rolled_this_turn is True


def test_turn_ends_after_non_double() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 2]))

    use_case.execute(game)

    # Kein Pasch -> Zug endet und weiterer roll ist nicht erlaubt.
    assert game.has_rolled_this_turn is True


def test_double_counter_resets_after_non_double() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 1, 2, 3]))

    use_case.execute(game)
    assert game.consecutive_doubles_count == 1

    use_case.execute(game)
    assert game.consecutive_doubles_count == 0


def test_player_goes_to_jail_after_three_doubles() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 1, 2, 2, 3, 3]))

    use_case.execute(game)
    use_case.execute(game)
    use_case.execute(game)

    assert game.current_player.in_jail is True
    assert game.current_player.position.index == 10


def test_player_does_not_move_normally_after_third_double() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = PlayTurnUseCase(FakeRandomPort([1, 1, 2, 2, 3, 3]))

    use_case.execute(game)  # auf 2
    use_case.execute(game)  # auf 6
    use_case.execute(game)  # 3. Pasch -> Gefaengnis statt auf 12

    assert game.current_player.position.index == 10