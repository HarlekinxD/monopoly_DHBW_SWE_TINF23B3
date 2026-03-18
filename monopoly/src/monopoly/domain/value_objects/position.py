# Das Monopoly-Spielbrett hat 40 Felder, nummeriert von 0 bis 39. 
# Das Startfeld ist 0, das Gefängnisfeld ist 10, und die anderen Felder haben ihre eigenen Nummern.
# Da der Spieler sich im Rechteck bewegt beötigt man den Modulo-Operator um die Position zu berechnen Beispiel 20:3=18 Rest 2.Es ist nur Restwert "2" relevant.
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    index: int
    
    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("Die Position kann nicht negativ sein ")
        
    #Beispiel Spiler würfelt eine 2 befindet sich auf Positon 39 (39+2) %40 = 1
    def move(self, steps: int, board_size: int) -> "Position":
                new_index = (self.index + steps) % board_size
                return Position(new_index)
    
    #Ist Spieler über-/auf LOS gegangen? 
    def has_passed_start(self, steps: int, board_size: int) -> bool:
        return (self.index + steps) >= board_size
    
    def __str__(self) -> str:
        return f"Position: ({self.index})"
    