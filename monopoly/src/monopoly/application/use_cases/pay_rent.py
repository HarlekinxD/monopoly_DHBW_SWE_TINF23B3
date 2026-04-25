from monopoly.domain.entities.game import Game
from monopoly.domain.entities.player import Player
from monopoly.domain.entities.tile import Tile
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.tile_color import TileColor
from monopoly.domain.value_objects.money import Money


class PayRentUseCase:
    def execute(self, game: Game, dice_value: int | None = None) -> None:
        player = game.current_player
        tile = game.board.get_tile_at(player.position)

        # Not ownable → nothing happens
        if not hasattr(tile, "is_owned"):
            return

        if not tile.is_owned():
            return

        # Player owns the tile → nothing happens
        if tile.owner_name == player.name:
            return

        owner = self._find_owner(game, tile.owner_name)

        rent = self._calculate_rent(tile, game, owner, dice_value)

        player.pay_money(rent)
        owner.receive_money(rent)

    def _find_owner(self, game: Game, owner_name: str) -> Player:
        for player in game.players:
            if player.name == owner_name:
                return player
        raise ValueError("Owner not found.")

    def _calculate_rent(
        self,
        tile: Tile,
        game: Game,
        owner: Player,
        dice_value: int | None,
    ) -> Money:
        if isinstance(tile, PropertyTile):
            # Bei Haus/Hotel gilt immer die normale staffel-miete.
            if tile.house_count > 0:
                return tile.get_current_rent()

            base_rent = tile.get_current_rent()

            # Nur unbebaute Strassen koennen durch vollstaendige farbgruppe verdoppeln.
            if self._owner_has_full_color_group(game, owner.name, tile.color):
                return Money(base_rent.amount * 2)

            return base_rent

        if isinstance(tile, RailroadTile):
            owned = self._count_owned_type(owner, RailroadTile, game)
            return tile.get_rent(owned)

        if isinstance(tile, UtilityTile):
            owned = self._count_owned_type(owner, UtilityTile, game)
            if dice_value is None:
                raise ValueError("Dice value required for utility rent.")
            return tile.get_rent(dice_value, owned)

        return Money(0)

    def _count_owned_type(self, owner: Player, tile_type: type[OwnableTile], game: Game) -> int:
        count = 0
        for tile in game.board.tiles:
            if isinstance(tile, tile_type) and tile.owner_name == owner.name:
                count += 1
        return count

    def _owner_has_full_color_group(self, game: Game, owner_name: str, color: TileColor) -> bool:
        # Alle property-tiles derselben farbe einsammeln.
        color_group_tiles = [
            tile
            for tile in game.board.tiles
            if isinstance(tile, PropertyTile) and tile.color == color
        ]

        if not color_group_tiles:
            return False

        # Vollstaendig nur wenn alle farb-tiles den gleichen owner haben.
        return all(tile.owner_name == owner_name for tile in color_group_tiles)