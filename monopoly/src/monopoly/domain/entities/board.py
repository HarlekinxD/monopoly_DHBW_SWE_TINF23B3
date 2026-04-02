from dataclasses import dataclass

from monopoly.domain.entities.tile import Tile
from monopoly.domain.value_objects.position import Position

# Container für Felder im Game. 
@dataclass
class Board:
    tiles: list[Tile] # Liste von Tile Objekten
    
    def __post_init__(self) ->  None:
        if not self.tiles:
            raise ValueError("A board must contain at least one tile.")
    
    def size(self) -> int: 
        return len(self.tiles) #Anzahl der Felder auf dem Board
    
    def get_tile_at(self, position: Position) -> Tile:
        return self.tiles[position.index] #gibt das Tile an der Position zurück
    
    def __str__(self) -> str:
        return f"Board(size={self.size()})"