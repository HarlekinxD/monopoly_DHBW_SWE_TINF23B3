from abc import ABC, abstractmethod

from monopoly.domain.entities.game import Game


class Presenter(ABC):
    @abstractmethod
    def present(self, game: Game) -> str:
        raise NotImplementedError