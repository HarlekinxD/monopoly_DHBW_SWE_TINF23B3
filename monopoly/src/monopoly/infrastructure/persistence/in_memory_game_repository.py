from monopoly.application.ports.game_repository import GameRepository
from monopoly.domain.entities.game import Game


class InMemoryGameRepository(GameRepository):
    def __init__(self) -> None:
        self._game: Game | None = None

    def save(self, game: Game) -> None:
        self._game = game

    def load(self) -> Game | None:
        return self._game