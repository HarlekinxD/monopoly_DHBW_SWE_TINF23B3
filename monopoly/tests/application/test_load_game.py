import pytest

from monopoly.application.use_cases.load_game import LoadGameUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.infrastructure.persistence.in_memory_game_repository import InMemoryGameRepository


def test_load_game_returns_saved_game() -> None:
    repository = InMemoryGameRepository()
    game = StartGameUseCase().execute(["Alice", "Bob"])
    repository.save(game)

    loaded = LoadGameUseCase(repository).execute()

    assert loaded is game


def test_load_game_raises_error_if_no_game_exists() -> None:
    repository = InMemoryGameRepository()

    with pytest.raises(ValueError, match="No saved game"):
        LoadGameUseCase(repository).execute()
