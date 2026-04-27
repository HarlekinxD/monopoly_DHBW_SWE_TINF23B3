from __future__ import annotations

from typing import Any

from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.special_tile import SpecialTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.entities.tile import Tile
from monopoly.domain.entities.utility_tile import UtilityTile


class GameSerializer:
    def serialize(self, game: Game) -> dict[str, Any]:
        # Top-level payload fuer die JSON datei
        return {
            "board": {
                "tiles": [self._serialize_tile(tile) for tile in game.board.tiles],
            },
            "players": [self._serialize_player(player) for player in game.players],
            "current_player_index": game.current_player_index,
            "active_view": game.active_view,
            "is_started": game.is_started,
            "has_rolled_this_turn": game.has_rolled_this_turn,
            "consecutive_doubles_count": game.consecutive_doubles_count,
            "can_buy_current_tile": game.can_buy_current_tile,
            "purchased_this_turn": game.purchased_this_turn,
            "current_turn_tile_id": game.current_turn_tile_id,
            "eliminated_players": list(game.eliminated_players),
            "current_round": game.current_round,
            "last_roll": game.last_roll,
            "last_message": game.last_message,
            "last_die_one": game.last_die_one,
            "last_die_two": game.last_die_two,
            "last_is_double": game.last_is_double,
        }

    def _serialize_player(self, player: Any) -> dict[str, Any]:
        # Alles was den player zustand ausmacht
        return {
            "name": player.name,
            "position": player.position.index,
            "balance": player.balance.amount,
            "token": player.token.value if player.token is not None else None,
            "owned_tile_ids": list(player.owned_tile_ids),
            "is_bankrupt": player.is_bankrupt,
            "in_jail": player.in_jail,
            "jail_turns": player.jail_turns,
        }

    def _serialize_tile(self, tile: Tile) -> dict[str, Any]:
        # Basis infos, tile-class brauchn wir fuer das zurueckbauen
        payload: dict[str, Any] = {
            "tile_class": type(tile).__name__,
            "tile_id": tile.tile_id,
            "name": tile.name,
            "tile_type": tile.tile_type.value,
        }

        if isinstance(tile, PropertyTile):
            payload.update(
                {
                    "price": tile.price.amount,
                    "owner_name": tile.owner_name,
                    "color": tile.color.value,
                    "house_price": tile.house_price.amount if tile.house_price is not None else None,
                    "rent_levels": [rent.amount for rent in tile.rent_levels],
                    "house_count": tile.house_count,
                }
            )
            return payload

        if isinstance(tile, RailroadTile):
            payload.update(
                {
                    "price": tile.price.amount,
                    "owner_name": tile.owner_name,
                    "railroad_rents": [rent.amount for rent in tile.railroad_rents],
                }
            )
            return payload

        if isinstance(tile, UtilityTile):
            payload.update(
                {
                    "price": tile.price.amount,
                    "owner_name": tile.owner_name,
                    "color": tile.color.value,
                    "utility_multipliers": list(tile.utility_multipliers),
                }
            )
            return payload

        if isinstance(tile, TaxTile):
            payload.update({"tax_amount": tile.tax_amount.amount})
            return payload

        if isinstance(tile, SpecialTile):
            return payload

        raise ValueError(f"Unsupported tile class for serialization: {type(tile).__name__}")
