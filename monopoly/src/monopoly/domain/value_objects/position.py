from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    index: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("Position cant be negative.")