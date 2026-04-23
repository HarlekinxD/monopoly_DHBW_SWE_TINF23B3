from monopoly.application.use_cases.attempt_leave_jail import AttemptLeaveJailUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_player_leaves_jail_when_rolling_doubles() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.send_to_jail(Position(10))

    result = AttemptLeaveJailUseCase().execute(game, 3, 3)

    assert result["released"] is True
    assert player.in_jail is False
    assert player.jail_turns == 0


def test_player_stays_in_jail_without_doubles() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.send_to_jail(Position(10))

    result = AttemptLeaveJailUseCase().execute(game, 2, 3)

    assert result["released"] is False
    assert player.in_jail is True
    assert player.jail_turns == 1


def test_player_pays_after_three_failed_attempts() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.send_to_jail(Position(10))

    use_case = AttemptLeaveJailUseCase()
    use_case.execute(game, 1, 2)
    use_case.execute(game, 2, 3)
    result = use_case.execute(game, 4, 5)

    assert result["released"] is True
    assert result["must_pay"] is True
    assert player.in_jail is False
    assert player.balance.amount == 1450