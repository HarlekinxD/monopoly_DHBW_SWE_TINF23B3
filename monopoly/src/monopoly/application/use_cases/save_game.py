from monopoly.application.ports.game_repository import GameRepository
from monopoly.domain.entities.game import Game


class SaveGameUseCase:
    def __init__(self, repository: GameRepository) -> None:
        # Repo wird von aussen reingeben (clean arch style)
        self._repository = repository

    def execute(self, game: Game) -> None:
        # Speichert den kompletten game state
        self._repository.save(game)
