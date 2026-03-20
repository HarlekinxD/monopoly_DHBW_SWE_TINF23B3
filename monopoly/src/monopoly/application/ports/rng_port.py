from abc import ABC, abstractmethod
from monopoly.domain.entities.card import Card

class RNGPort(ABC):
    """
    Port that defines which random operations are needed in the application layer
    The implementation from random-package are later injected in the infrastructure layer. 
    This allows us to easily mock the RNG for testing purposes.
    
    """
    @abstractmethod
    def shuffle_cards(self, cards: list[Card]) -> list[Card]:
        """
        Shuffles a list of cards and returns the shuffled list.
        """
        pass