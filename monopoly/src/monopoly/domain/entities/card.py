from abc import ABC, abstractmethod
from dataclasses import dataclass
from monopoly.domain.card_type import CardType
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from monopoly.domain.entities.player import Player  # Avoid circular import for type hinting
    from monopoly.domain.entities.board import Board  # Avoid circular import for type hinting

class Card(ABC):
    """
    Base class for all Cards (Ereigniskarten and Gemeinschaftskarten).
    It defines the attributes and methods of all cards in the game.
    """
    def __init__(self, card_id: int, card_type: CardType, txt: str) -> None:
        if card_id < 0:
            raise ValueError("Die Karten-ID kann nicht negativ sein.")
        
        if not txt.strip():
            raise ValueError("Der Text der Karte darf nicht leer sein.")
        
        self.card_id = card_id
        self.card_type = card_type
        self.txt = txt

    def __str__(self) -> str:
        return f"{self.card_type}: {self.txt}"
    
    @abstractmethod
    def execute(self, player: "Player", board: "Board") -> None:
        """
        Defines the action for a card when it is drawn by a player.
        It will be overridden by the subclasses of Card (MoneyCard, MoveCard, JailFreeCard) for the specific behavior.
        """
        pass
    

@dataclass
class MoneyCard(Card):
    """
    A subclass of Card that adds/withdraws money from the player balance.
    """
    amount: Money
    is_penalty: bool = False  # True = penalty, False = reward

    def __post_init__(self) -> None:
        super().__init__(self.card_id, self.card_type, self.txt)
    
    def execute(self, player: "Player", board: "Board") -> None:
        """
        Adds or withdraws money from the player's balance depending on whether the card is a penalty or a reward.
        """
        if self.is_penalty:
            player.pay_money(self.amount)
        else:
            player.receive_money(self.amount)

@dataclass
class MoveCard(Card):
    """
    A subclass of Card that moves the player to a specific position on the board.
    Important for cards like "Gehe zu LOS" or "Gehe zum Gefängnis".
    """
    target_position_index: int

    def __post_init__(self) -> None:
        if self.target_position_index < 0:
            raise ValueError("Die Zielposition darf nicht negativ sein.")
        super().__init__(self.card_id, self.card_type, self.txt)

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        # Fall 1: Ab ins Gefängnis (kein LOS-Geld)
        if self.target_position_index == 10:
            player.go_to_jail(Position(10))
            return

        # Fall 2: Normales Vorrücken
        current_index = player.position.index
        
        if self.target_position_index > current_index:
            steps = self.target_position_index - current_index
        else:
            # Spieler muss über LOS gehen (40 ist die Spielfeldgröße)
            steps = (40 - current_index) + self.target_position_index
            
        passed_start = player.move(steps, 40)
        
        if passed_start:
            player.receive_money(Money(200))

        
@dataclass
class RelativeMoveCard(Card):
    """
    Moves the player a specific number of steps forwards or backwards.
    Important for cards like "Gehe 3 Felder zurück".
    """
    steps: int

    def __post_init__(self) -> None:
        super().__init__(self.card_id, self.card_type, self.txt)

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        # Die Methode has_passed_start funktioniert auch bei negativen Zahlen, 
        # das ist aber bei "Gehe 3 Felder zurück" meist nicht erwünscht, wenn man über LOS rückwärts geht.
        # Im Standard-Monopoly zieht man kein LOS-Geld beim Rückwärtsgehen ein.
        player.position = player.position.move(self.steps, 40)
        
        # Wichtig: Im Hauptspiel muss nach diesem Move geschaut werden,
        # auf was für einem Feld der Spieler jetzt gelandet ist (z.B. Zusatzsteuer).

@dataclass
class JailFreeCard(Card):
    """
    A special card that allows the player to get out of jail for free.
    It can be stored by the player and used in a later turn.
    """
    def __post_init__(self) -> None:
        super().__init__(self.card_id, self.card_type, self.txt)
        
    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        player.give_card(self)

@dataclass
class PlayerInteractionMoneyCard(Card):
    """
    Card where money is exchanged between players (e.g., "Collect $10 from every player").
    (Benötigt später Zugriff auf die Liste aller Spieler im Spiel).
    """
    amount_per_player: Money
    player_pays_others: bool = False  # True = Zahle an jeden, False = Bekomme von jedem

    def __post_init__(self) -> None:
        super().__init__(self.card_id, self.card_type, self.txt)

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        # Diese Karte benötigt später in der Game-Loop die anderen Spieler.
        # Wir können die Logik hier nur andeuten oder müssten alle Spieler übergeben.
        pass

@dataclass
class PropertyRepairsCard(Card):
    """
    Card where the player pays based on the amount of houses and hotels they own.
    (Benötigt später Zugriff auf die bebauten Felder des Spielers).
    """
    #TODO Bitte später anpassen, wenn wir die Häuser- und Hotel-Logik haben
    cost_per_house: Money
    cost_per_hotel: Money

    def __post_init__(self) -> None:
        super().__post_init__()

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        # Auch hier: Wir brauchen das Board, um zu schauen, wie viele Häuser auf den 
        # owned_tile_ids des Spielers stehen. Das bauen wir, wenn das Board Häuser unterstützt.
        pass