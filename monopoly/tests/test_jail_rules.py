from monopoly.application.use_cases.release_from_jail import ReleaseFromJailUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_player_can_be_sent_to_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    player.send_to_jail(Position(10))

    assert player.position.index == 10
    assert player.in_jail is True
    assert player.jail_turns == 0


def test_player_can_be_released_from_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    player.send_to_jail(Position(10))

    result = ReleaseFromJailUseCase().execute(game)

    assert "released" in result
    assert player.in_jail is False
    assert player.jail_turns == 0