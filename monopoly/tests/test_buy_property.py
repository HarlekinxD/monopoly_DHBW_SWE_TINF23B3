import pytest

from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_player_can_buy_an_unowned_property() -> None:
    start_game = StartGameUseCase()
    game_state = start_game.execute(["Alice", "Bob"])

    # We need the actual game object, not only the DTO
    # If your StartGameUseCase currently returns only DTOs,
    # see the note below and adapt accordingly.