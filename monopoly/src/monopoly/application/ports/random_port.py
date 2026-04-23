from abc import ABC, abstractmethod


class RandomPort(ABC):
    @abstractmethod
    def roll_dice(self) -> int:
        raise NotImplementedError
    
    def roll_die(self) -> int:
        raise NotImplementedError