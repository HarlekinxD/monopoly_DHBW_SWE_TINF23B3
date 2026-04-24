from monopoly.application.use_cases.draw_chance_card import DrawChanceCardUseCase
from monopoly.application.use_cases.draw_community_card import DrawCommunityCardUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase


def test_chance_card_advance_to_go_position_persists() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    DrawChanceCardUseCase().execute(game)

    assert player.position.index == 0
    assert player.balance.amount == 1700


def test_community_card_go_to_jail_position_persists() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player
    use_case = DrawCommunityCardUseCase()

    use_case.execute(game)
    use_case.execute(game)
    use_case.execute(game)
    result = use_case.execute(game)

    assert "sent to jail" in result
    assert player.position.index == 10
    assert player.in_jail is True