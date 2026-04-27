from monopoly.application.use_cases.save_game import SaveGameUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.infrastructure.persistence.in_memory_game_repository import InMemoryGameRepository


def test_save_game_persists_game_in_repository() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    repository = InMemoryGameRepository()

    SaveGameUseCase(repository).execute(game)

    loaded = repository.load()
    assert loaded is game
