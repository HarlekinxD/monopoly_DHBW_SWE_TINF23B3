from abc import ABC, abstractmethod


class RandomPort(ABC):
    @abstractmethod
    def roll_dice(self) -> int:
        raise NotImplementedError