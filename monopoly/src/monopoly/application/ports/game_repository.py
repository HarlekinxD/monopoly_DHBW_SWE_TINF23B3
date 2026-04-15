from abc import ABC, abstractmethod

from monopoly.domain.entities.game import Game


class GameRepository(ABC):
    @abstractmethod
    def save(self, game: Game) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self) -> Game | None:
        raise NotImplementedError