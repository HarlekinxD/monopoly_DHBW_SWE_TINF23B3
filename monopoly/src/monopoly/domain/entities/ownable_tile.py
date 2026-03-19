from dataclasses import dataclass

from monopoly.domain.entities.tile import Tile
from monopoly.domain.value_objects.money import Money


@dataclass
class OwnableTile(Tile):
    price: Money
    owner_name: str | None = None

    def is_owned(self) -> bool:
        return self.owner_name is not None

    def can_be_bought(self) -> bool:
        return not self.is_owned()

    def buy(self, owner_name: str) -> None:
        if self.is_owned():
            raise ValueError(f"Das Feld '{self.name}' gehört bereits {self.owner_name}.")

        if not owner_name.strip():
            raise ValueError("Der Besitzername darf nicht leer sein.")

        self.owner_name = owner_name

    def clear_owner(self) -> None:
        self.owner_name = None