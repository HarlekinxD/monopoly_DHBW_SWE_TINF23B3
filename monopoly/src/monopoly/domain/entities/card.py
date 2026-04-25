from abc import ABC, abstractmethod
from dataclasses import dataclass
from monopoly.domain.card_type import CardType
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from monopoly.domain.entities.player import Player  
    from monopoly.domain.entities.board import Board  

@dataclass
class Card(ABC):
    """
    Base class for all Cards (Ereigniskarten and Gemeinschaftskarten).
    It defines the attributes and methods of all cards in the game.
    """
    card_id: int
    card_type: CardType
    txt: str

    def __post_init__(self) -> None:
        if self.card_id < 0:
            raise ValueError("Die Karten-ID kann nicht negativ sein.")
        
        if not self.txt.strip():
            raise ValueError("Der Text der Karte darf nicht leer sein.")

    def __str__(self) -> str:
        return f"{self.card_type}: {self.txt}"
    
    @abstractmethod
    def execute(self, player: "Player", board: "Board" = None) -> None:
        """
        Defines the action for a card when it is drawn by a player.
        It will be overridden by the subclasses.
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
        super().__post_init__() # Validiert card_id und txt
    
    def execute(self, player: "Player", board: "Board" = None) -> None:
        if self.is_penalty:
            player.pay_money(self.amount)
        else:
            player.receive_money(self.amount)

@dataclass
class MoveCard(Card):
    """
    A subclass of Card that moves the player to a specific position on the board.
    """
    target_position_index: int

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.target_position_index < 0:
            raise ValueError("Die Zielposition darf nicht negativ sein.")

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        if self.target_position_index == 10:
            player.go_to_jail(Position(10))
            return

        current_index = player.position.index
        
        if self.target_position_index > current_index:
            steps = self.target_position_index - current_index
        else:
            steps = (40 - current_index) + self.target_position_index
            
        passed_start = player.move(steps, 40)
        
        if passed_start:
            player.receive_money(Money(200))

        
@dataclass
class RelativeMoveCard(Card):
    """
    Moves the player a specific number of steps forwards or backwards.
    """
    steps: int

    def __post_init__(self) -> None:
        super().__post_init__()

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        player.position = player.position.move(self.steps, 40)

@dataclass
class JailFreeCard(Card):
    """
    A special card that allows the player to get out of jail for free.
    """
    def __post_init__(self) -> None:
        super().__post_init__()
        
    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        player.give_card(self)

@dataclass
class PlayerInteractionMoneyCard(Card):
    """
    Card where money is exchanged between players.
    """
    amount_per_player: Money
    player_pays_others: bool = False  

    def __post_init__(self) -> None:
        super().__post_init__()

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        pass

@dataclass
class NearestRailroadCard(Card):
    """
    Card that moves the player to the nearest railroad.
    """
    def __post_init__(self) -> None:
        super().__post_init__()

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        current = player.position.index
        
        if current < 5 or current >= 35:
            target_tile_index = 5
        elif current < 15:
            target_tile_index = 15
        elif current < 25:
            target_tile_index = 25
        else:
            target_tile_index = 35
        
        if target_tile_index < current:
            steps = (40 - current) + target_tile_index
        else:
            steps = target_tile_index - current
            
        passed_start = player.move(steps, 40)
        if passed_start:
            player.receive_money(Money(200))
            # TODO: Double rent logic in Game Controller
            
@dataclass
class PropertyRepairsCard(Card):
    """
    Card where the player pays based on the amount of houses and hotels they own.
    """
    cost_per_house: Money
    cost_per_hotel: Money

    def __post_init__(self) -> None:
        super().__post_init__()

    def execute(self, player: 'Player', board: 'Board' = None) -> None:
        if board is None:
            return
            
        total_houses = 0
        total_hotels = 0
        
        for tile_id in player.owned_tile_ids:
            tile = board.get_tile(tile_id)
            if hasattr(tile, 'houses') and hasattr(tile, 'hotels'):
                total_houses += tile.houses
                total_hotels += tile.hotels
                
        total_cost = (total_houses * self.cost_per_house.amount) + (total_hotels * self.cost_per_hotel.amount)
        
        if total_cost > 0:
            player.pay_money(Money(total_cost))