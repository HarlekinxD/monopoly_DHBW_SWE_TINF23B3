from enum import Enum

class CardType(Enum):
    CHANCE = "Ereigniskarte"
    COMMUNITY_CHEST = "Gemeinschaftskarte"
    
    def __str__(self) -> str:
        return self
    
    
   