from monopoly.application.use_cases.draw_community_card import DrawCommunityCardUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_community_card_can_give_money() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawCommunityCardUseCase()

    result = use_case.execute(game)

    assert "received 200" in result
    assert game.current_player.balance.amount == 1700


def test_community_card_can_take_money() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawCommunityCardUseCase()

    use_case.execute(game)  # +200
    result = use_case.execute(game)  # -50

    assert "paid 50" in result
    assert game.current_player.balance.amount == 1650


def test_community_card_can_send_player_to_jail() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    use_case = DrawCommunityCardUseCase()

    use_case.execute(game)  # +200
    use_case.execute(game)  # -50
    use_case.execute(game)  # move to GO
    result = use_case.execute(game)  # go to jail

    assert "sent to jail" in result
    assert game.current_player.position.index == 10
    assert game.current_player.in_jail is True