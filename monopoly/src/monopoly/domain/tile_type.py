# Space for railroads and utilities.

from enum import Enum


class TileType(Enum):
    PROPERTY = "property"
    RAILROAD = "railroad"
    UTILITY = "utility"
    TAX = "tax"
    SPECIAL = "special"

    def __str__(self) -> str:
        return self.value