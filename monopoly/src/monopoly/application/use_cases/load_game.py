from monopoly.application.ports.game_repository import GameRepository
from monopoly.domain.entities.game import Game


class LoadGameUseCase:
    def __init__(self, repository: GameRepository) -> None:
        # Gleiches Repo-prinzip wie beim save
        self._repository = repository

    def execute(self) -> Game:
        # Versucht letzten Spielstand zu laden
        game = self._repository.load()
        if game is None:
            # Klarer Fehler statt None weiterzureichen
            raise ValueError("No saved game found.")
        return game
