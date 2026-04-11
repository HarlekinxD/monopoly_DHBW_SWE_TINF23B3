from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    index: int

    def __post_init__(self) -> None:
        if self.index < 0:
            raise ValueError("Position cannot be negative.")

    def move(self, steps: int, board_size: int) -> "Position":
        if board_size <= 0:
            raise ValueError("Board size must be greater than zero.")
        if steps < 0:
            raise ValueError("Steps cannot be negative.")

        return Position((self.index + steps) % board_size)

    def has_passed_start(self, steps: int, board_size: int) -> bool:
        if board_size <= 0:
            raise ValueError("Board size must be greater than zero.")
        if steps < 0:
            raise ValueError("Steps cannot be negative.")

        return self.index + steps >= board_size