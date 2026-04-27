from __future__ import annotations

from typing import Any, Mapping

from monopoly.domain.entities.board import Board
from monopoly.domain.entities.game import Game
from monopoly.domain.entities.player import Player
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.special_tile import SpecialTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.entities.tile import Tile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.tile_color import TileColor
from monopoly.domain.tile_type import TileType
from monopoly.domain.token import Token
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


class GameDeserializer:
    def deserialize(self, payload: Mapping[str, Any]) -> Game:
        # Erst board + players rekonstruieren, dann Game bauen
        board_payload = payload["board"]
        tiles = [self._deserialize_tile(tile_data) for tile_data in board_payload["tiles"]]
        board = Board(tiles)

        players = [self._deserialize_player(player_data) for player_data in payload["players"]]

        game = Game(
            board=board,
            players=players,
            current_player_index=int(payload["current_player_index"]),
            active_view=str(payload["active_view"]),
            is_started=bool(payload["is_started"]),
            has_rolled_this_turn=bool(payload["has_rolled_this_turn"]),
            consecutive_doubles_count=int(payload.get("consecutive_doubles_count", 0)),
            can_buy_current_tile=bool(payload["can_buy_current_tile"]),
            purchased_this_turn=bool(payload["purchased_this_turn"]),
            current_turn_tile_id=payload["current_turn_tile_id"],
            eliminated_players=list(payload["eliminated_players"]),
            current_round=int(payload["current_round"]),
            last_roll=payload["last_roll"],
            last_message=str(payload["last_message"]),
        )
        return game

    def _deserialize_player(self, payload: Mapping[str, Any]) -> Player:
        # Token ist optional gespeichert
        token_name = payload["token"]
        token = Token(token_name) if token_name is not None else None

        return Player(
            name=str(payload["name"]),
            position=Position(int(payload["position"])),
            balance=Money(int(payload["balance"])),
            token=token,
            owned_tile_ids=[int(tile_id) for tile_id in payload["owned_tile_ids"]],
            is_bankrupt=bool(payload["is_bankrupt"]),
            in_jail=bool(payload["in_jail"]),
            jail_turns=int(payload["jail_turns"]),
        )

    def _deserialize_tile(self, payload: Mapping[str, Any]) -> Tile:
        # Je nach tile_class die passende Entitaet bauen
        tile_class = str(payload["tile_class"])
        tile_type = TileType(str(payload["tile_type"]))
        tile_id = int(payload["tile_id"])
        name = str(payload["name"])

        if tile_class == "PropertyTile":
            return PropertyTile(
                tile_id=tile_id,
                name=name,
                tile_type=tile_type,
                price=Money(int(payload["price"])),
                owner_name=payload["owner_name"],
                color=TileColor(str(payload["color"])),
                house_price=Money(int(payload["house_price"])),
                rent_levels=[Money(int(amount)) for amount in payload["rent_levels"]],
                house_count=int(payload["house_count"]),
            )

        if tile_class == "RailroadTile":
            return RailroadTile(
                tile_id=tile_id,
                name=name,
                tile_type=tile_type,
                price=Money(int(payload["price"])),
                owner_name=payload["owner_name"],
                railroad_rents=[Money(int(amount)) for amount in payload["railroad_rents"]],
            )

        if tile_class == "UtilityTile":
            return UtilityTile(
                tile_id=tile_id,
                name=name,
                tile_type=tile_type,
                price=Money(int(payload["price"])),
                owner_name=payload["owner_name"],
                color=TileColor(str(payload["color"])),
                utility_multipliers=[int(multiplier) for multiplier in payload["utility_multipliers"]],
            )

        if tile_class == "TaxTile":
            return TaxTile(
                tile_id=tile_id,
                name=name,
                tile_type=tile_type,
                tax_amount=Money(int(payload["tax_amount"])),
            )

        if tile_class == "SpecialTile":
            return SpecialTile(
                tile_id=tile_id,
                name=name,
                tile_type=tile_type,
            )

        raise ValueError(f"Unsupported tile class for deserialization: {tile_class}")
