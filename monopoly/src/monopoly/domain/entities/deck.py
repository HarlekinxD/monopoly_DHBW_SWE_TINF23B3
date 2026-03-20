import random
from dataclasses import dataclass, field
from monopoly.domain.entities.card import Card
from monopoly.domain.card_type import CardType

@dataclass
class Deck:
    """
    A class that represents a deck of cards (Ereigniskarten or Gemeinschaftskarten)
    Cards are stored in a list drawn from the top of the deck and returned to the bottom after being drawn
    
    """
    deck_type: CardType
    cards: list[Card] = field(default_factory=list)
    
    def __post_init__(self) -> None:
        """
        Initalizes the shuffling of the decks after they are created
        
        """
        self.shuffle()
    
    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck
        
        """
        random.shuffle(self.cards)
    
    def draw_card(self) -> Card:
        """
        Draws a card at the Top oof the Deck (index=0) 
        
        """
        if not self.cards:
            raise ValueError(f"Das {self.deck_type.name}-Deck ist leer!")
    
        # .pop(0) removing the first card of the list and it will be returned
        return self.cards.pop(0)
    
    def return_card(self, card: Card) -> None:
        """
        Returns a card to the bottom of the deck (index=15 for 16 cards)
        
        """
        self.cards.append(card)

    def __len__(self) -> int:
        """
        Returns the number of cards currently in the deck (for a debbugging purpose)
        
        """
        return len(self.cards)
    
        