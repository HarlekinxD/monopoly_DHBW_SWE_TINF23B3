from dataclasses import dataclass, field #Für Standarwerte wie Arrays oder komplexe Objekte
from monopoly.domain.value_objects import Money #aus money.py
from monopoly.domain.value_objects import Position #aus position.py
from monopoly.domain.entities.card import Card, JailFreeCard #from card.py

@dataclass
class Player:
    name: str
    position: Position = field(default_factory=lambda: Position(0))  # Startposition is 0
    balance: Money = field(default_factory=lambda: Money(1500))  # Startguthaben ist 1500 Monopoly$
    owned_tile_ids: list[int] = field(default_factory=list)  # Liste der IDs der Felder die ein Spieler besitzt
    in_jail: bool = False  # Gibt an, ob der Spieler im Gefängnis ist
    jail_turns: int = 0  # Anzahl der Runden, die der Spieler im Gefängnis verbracht hat
    retained_cards: list[Card] = field(default_factory=list)  # List of Cards who stored to a player for more than one turn (z.B. "Du kommst aus dem Gefängnis frei")
    
    # Bewegt den spieler um Anzahl "x" und aktualisiert die Position. Gibt zurück, ob der Spieler über LOS gegangen ist
    def move(self, steps: int, board_size: int) -> bool:
        passed_start = self.position.has_passed_start(steps, board_size)
        self.position = self.position.move(steps, board_size)
        return passed_start
    
    def receive_money(self, amount: Money) -> None:
        self.balance = self.balance.add(amount)
    
    # Logik die angibt, ob ein Spieler genug Geld hat eine Strafe-/Miete zu bezahlen.
    def pay_money(self, amount: Money) -> None:
        self.balance = self.balance.subtract(amount)
    
    # Logik für den Kauf eines Feldes aktuallisert die Balance des Spielers und fügt die ID des gekauften Tiles zur Liste der besessenen Tiles hinzu
    def buy_tile(self, tile_id: int, price: Money) -> None:
        self.pay_money(price)
        self.owned_tile_ids.append(tile_id)
    
    # Logik für den Verkauf eines Felds aktuallisiert die Balance, entfernt die ID des verkauften Tiles aus dem Array
    def sell_tile(self, tile_id: int, price: Money) -> None:
        if self.owns_tile(tile_id):
            self.owned_tile_ids.remove(tile_id)
            self.receive_money(price)

    def owns_tile(self, tile_id: int) -> bool:
        return tile_id in self.owned_tile_ids

    # Logik für das Gefängnis setzt die Position des Spielers auf Gefängnisund setzt die Anzahl der Gefängnisrunden auf 0
    def go_to_jail(self, jail_position: Position) -> None:
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0
    
    def __str__(self)-> str:
        return (
            f"Player(name={self.name}, position={self.position}, "
            f"balance={self.balance}, in_jail={self.in_jail})"
        )
    
    #  Gives the player a card that he can keep
    def give_card(self, card: Card) -> None:
        self.retained_cards.append(card)
    
    def use_jail_free_card(self) -> Card:
        """
        Use the 'Gefängnis frei' Card and return it so that it can be put back under the deck.
        
        Raises:
            ValueError: If player is not in jail or doesn't have a JailFreeCard.
        """
        if not self.in_jail:
            raise ValueError(f"{self.name} ist gar nicht im Gefängnis!")
        
        for i, card in enumerate(self.retained_cards):
            if isinstance(card, JailFreeCard):  # Only one JailFreeCard could be used at a time
                used_card = self.retained_cards.pop(i)  # delete the card from the retained cards of the player
                self.in_jail = False  # The player is not in jail anymore
                self.jail_turns = 0  # reset the jail turns
                return used_card  # Gives the card back to the Deck
        
        raise ValueError(f"Der Spieler {self.name} besitzt keine 'Gefängnis frei' Karte!")