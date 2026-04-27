"""
Advanced tests for game serialization and deserialization.
Tests edge cases and complex game states.
"""
import pytest

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.position import Position
from monopoly.infrastructure.persistence.game_serializer import GameSerializer
from monopoly.infrastructure.persistence.game_deserializer import GameDeserializer


class TestGameSerializerAdvanced:
    """Advanced serialization tests for complex game states."""

    def test_serialize_game_with_multiple_players(self) -> None:
        """Verify serialization works with multiple players."""
        game = StartGameUseCase().execute(["Alice", "Bob", "Charlie", "David"])
        serializer = GameSerializer()

        payload = serializer.serialize(game)

        assert "players" in payload
        assert len(payload["players"]) == 4
        assert all(player["name"] in ["Alice", "Bob", "Charlie", "David"] for player in payload["players"])

    def test_serialize_player_with_properties(self) -> None:
        """Verify that player properties are serialized correctly."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player

        # Assign properties
        tile1 = game.board.get_tile_at(Position(1))
        tile3 = game.board.get_tile_at(Position(3))
        tile1.buy(player.name)
        tile3.buy(player.name)
        player.add_owned_tile(1)
        player.add_owned_tile(3)

        serializer = GameSerializer()
        payload = serializer.serialize(game)

        alice_data = next(p for p in payload["players"] if p["name"] == "Alice")
        assert len(alice_data.get("owned_tile_ids", [])) >= 2

    def test_serialize_game_with_buildings(self) -> None:
        """Verify that buildings (houses and hotels) are serialized."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player

        # Setup property with houses
        tile = game.board.get_tile_at(Position(1))
        tile.buy(player.name)
        player.add_owned_tile(1)
        tile.house_count = 3

        serializer = GameSerializer()
        payload = serializer.serialize(game)

        # Find serialized board tile
        board_data = payload.get("board", {})
        tiles = board_data.get("tiles", [])
        target_tile = next((t for t in tiles if t.get("position_id") == 1), None)

        assert target_tile is not None
        assert target_tile.get("house_count") == 3

    def test_serialize_player_balance(self) -> None:
        """Verify that player balance is correctly serialized."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player
        original_balance = player.balance.amount

        serializer = GameSerializer()
        payload = serializer.serialize(game)

        alice_data = next(p for p in payload["players"] if p["name"] == "Alice")
        assert alice_data.get("balance") == original_balance

    def test_serialize_game_preserves_order(self) -> None:
        """Verify that player order is preserved during serialization."""
        game = StartGameUseCase().execute(["First", "Second", "Third"])
        serializer = GameSerializer()

        payload = serializer.serialize(game)
        player_names = [p["name"] for p in payload["players"]]

        assert player_names == ["First", "Second", "Third"]


class TestGameDeserializerAdvanced:
    """Advanced deserialization tests."""

    def test_deserialize_maintains_player_state(self) -> None:
        """Verify that deserialization restores player state."""
        original_game = StartGameUseCase().execute(["Alice", "Bob"])
        original_alice = original_game.players[0]
        original_alice.pay_rent(100)

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        restored_alice = restored_game.players[0]
        assert restored_alice.balance.amount == original_alice.balance.amount
        assert restored_alice.name == original_alice.name

    def test_deserialize_maintains_board_state(self) -> None:
        """Verify that board state is maintained during deserialization."""
        original_game = StartGameUseCase().execute(["Alice", "Bob"])

        # Modify board state
        tile1 = original_game.board.get_tile_at(Position(1))
        tile1.buy("Alice")
        tile1.house_count = 2

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        restored_tile1 = restored_game.board.get_tile_at(Position(1))
        assert restored_tile1.owner_name == "Alice"
        assert restored_tile1.house_count == 2

    def test_deserialize_restores_tile_owners(self) -> None:
        """Verify that tile ownership is correctly restored."""
        original_game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])

        # Multiple players own properties
        game_board = original_game.board
        game_board.get_tile_at(Position(1)).buy("Alice")
        game_board.get_tile_at(Position(3)).buy("Bob")
        game_board.get_tile_at(Position(6)).buy("Charlie")

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        assert restored_game.board.get_tile_at(Position(1)).owner_name == "Alice"
        assert restored_game.board.get_tile_at(Position(3)).owner_name == "Bob"
        assert restored_game.board.get_tile_at(Position(6)).owner_name == "Charlie"

    def test_deserialize_invalid_data_raises_error(self) -> None:
        """Verify that invalid data raises an appropriate error."""
        deserializer = GameDeserializer()
        invalid_payload = {"invalid": "data"}

        with pytest.raises((ValueError, KeyError, TypeError)):
            deserializer.deserialize(invalid_payload)

    def test_serialize_deserialize_roundtrip(self) -> None:
        """Verify complete roundtrip: original -> serialize -> deserialize -> matches."""
        original_game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])

        # Modify game state
        alice = original_game.players[0]
        tile = original_game.board.get_tile_at(Position(1))
        tile.buy(alice.name)
        alice.add_owned_tile(1)
        tile.house_count = 1
        alice.move_to(Position(5))
        alice.pay_rent(50)

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        # Roundtrip
        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        # Verify key state
        restored_alice = restored_game.players[0]
        restored_tile = restored_game.board.get_tile_at(Position(1))

        assert restored_alice.name == alice.name
        assert restored_alice.balance.amount == alice.balance.amount
        assert restored_alice.position.position_id == 5
        assert restored_tile.owner_name == "Alice"
        assert restored_tile.house_count == 1


class TestGameDeserializerEdgeCases:
    """Edge case tests for deserialization."""

    def test_deserialize_game_with_no_owned_properties(self) -> None:
        """Verify deserialization works when no properties are owned."""
        original_game = StartGameUseCase().execute(["Alice", "Bob"])

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        assert restored_game is not None
        assert len(restored_game.players) == 2

    def test_deserialize_game_with_all_properties_owned(self) -> None:
        """Verify deserialization works when many properties are owned."""
        original_game = StartGameUseCase().execute(["Alice", "Bob"])
        alice = original_game.players[0]
        bob = original_game.players[1]

        # Alice and Bob own multiple properties
        for i in range(1, 10):
            tile = original_game.board.get_tile_at(Position(i))
            owner = "Alice" if i % 2 == 0 else "Bob"
            tile.buy(owner)
            if owner == "Alice":
                alice.add_owned_tile(i)
            else:
                bob.add_owned_tile(i)

        serializer = GameSerializer()
        deserializer = GameDeserializer()

        payload = serializer.serialize(original_game)
        restored_game = deserializer.deserialize(payload)

        restored_alice = restored_game.players[0]
        restored_bob = restored_game.players[1]

        assert len(restored_alice.owned_tile_ids) >= 4
        assert len(restored_bob.owned_tile_ids) >= 4
