from monopoly.application.use_cases.draw_chance_card import DrawChanceCardUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


def test_chance_card_can_move_player_to_go() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawChanceCardUseCase()

    result = use_case.execute(game)

    assert "moved to GO" in result
    assert game.current_player.position.index == 0
    assert game.current_player.balance.amount == 1700


def test_chance_card_can_move_player_backwards() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawChanceCardUseCase()

    use_case.execute(game)  # move to GO
    result = use_case.execute(game)  # go back 3

    assert "moved to tile" in result
    assert game.current_player.position.index == 37


def test_chance_card_can_send_player_to_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawChanceCardUseCase()

    use_case.execute(game)  # move to GO
    use_case.execute(game)  # go back 3
    use_case.execute(game)  # pay 100
    use_case.execute(game)  # receive 50
    result = use_case.execute(game)  # jail

    assert "sent to jail" in result
    assert game.current_player.position.index == 10
    assert game.current_player.in_jail is True

def test_chance_card_move_changes_player_position_persistently() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawChanceCardUseCase()

    result = use_case.execute(game)

    assert "moved to GO" in result
    assert game.current_player.position.index == 0

def test_chance_card_go_to_jail_changes_position_persistently() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawChanceCardUseCase()

    use_case.execute(game)  # GO
    use_case.execute(game)  # back 3
    use_case.execute(game)  # pay
    use_case.execute(game)  # receive
    result = use_case.execute(game)  # jail

    assert "sent to jail" in result
    assert game.current_player.position.index == 10
    assert game.current_player.in_jail is True