"""
Integration tests for CLI save/load/sell commands.
Tests that the MenuController properly handles the new game commands.
"""
import tempfile
from pathlib import Path

import pytest

from monopoly.application.use_cases.save_game import SaveGameUseCase
from monopoly.application.use_cases.load_game import LoadGameUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.sell_building import SellBuildingUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.position import Position
from monopoly.infrastructure.persistence.json_game_repository import JsonGameRepository
from monopoly.infrastructure.rng.python_random_dice import PythonRandomDice


class TestSaveLoadGameWorkflow:
    """Tests for saving and loading game state."""

    def test_save_and_load_preserves_game_state(self) -> None:
        """Verify that saving and loading preserves all game state."""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "game.json"
            repository = JsonGameRepository(save_file)

            # Create game
            original_game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])
            original_game.current_player.move_to(Position(5))
            original_game.current_player.pay_rent(100)

            # Save
            SaveGameUseCase(repository).execute(original_game)
            assert save_file.exists()

            # Load
            loaded_game = LoadGameUseCase(repository).execute()

            # Verify
            assert loaded_game is not None
            assert loaded_game.current_player.name == original_game.current_player.name
            assert loaded_game.current_player.position.position_id == 5
            assert loaded_game.current_player.balance.amount == original_game.current_player.balance.amount

    def test_save_file_is_valid_json(self) -> None:
        """Verify that save files are valid JSON."""
        import json

        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "game.json"
            repository = JsonGameRepository(save_file)

            game = StartGameUseCase().execute(["Alice", "Bob"])
            SaveGameUseCase(repository).execute(game)

            # Should be valid JSON
            content = json.loads(save_file.read_text(encoding="utf-8"))
            assert "players" in content
            assert "board" in content

    def test_load_nonexistent_save_file_raises_error(self) -> None:
        """Verify that loading a non-existent save file raises an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "nonexistent.json"
            repository = JsonGameRepository(save_file)

            with pytest.raises(ValueError, match="No saved game found"):
                LoadGameUseCase(repository).execute()

    def test_multiple_saves_overwrite_previous(self) -> None:
        """Verify that saving multiple times overwrites the previous save."""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "game.json"
            repository = JsonGameRepository(save_file)
            save_use_case = SaveGameUseCase(repository)

            # First save
            game1 = StartGameUseCase().execute(["Alice", "Bob"])
            save_use_case.execute(game1)
            first_save_time = save_file.stat().st_mtime

            # Second save with different state
            game2 = StartGameUseCase().execute(["Charlie", "David"])
            save_use_case.execute(game2)
            second_save_time = save_file.stat().st_mtime

            # Load should get second game
            loaded_game = LoadGameUseCase(repository).execute()
            assert loaded_game.players[0].name == "Charlie"
            assert second_save_time >= first_save_time


class TestSellBuildingIntegration:
    """Integration tests for selling buildings."""

    def test_sell_building_reduces_house_count(self) -> None:
        """Verify that selling a building reduces the house count."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player

        # Assign properties to player
        tile1 = game.board.get_tile_at(Position(1))
        tile3 = game.board.get_tile_at(Position(3))
        tile1.buy(player.name)
        tile3.buy(player.name)
        player.add_owned_tile(1)
        player.add_owned_tile(3)

        # Build houses evenly
        tile1.house_count = 2
        tile3.house_count = 2

        # Move to first property and sell
        player.move_to(Position(1))
        initial_balance = player.balance.amount

        message = SellBuildingUseCase().execute(game)

        assert tile1.house_count == 1
        assert player.balance.amount > initial_balance
        assert "sold" in message.lower()

    def test_sell_hotel_converts_to_houses(self) -> None:
        """Verify that selling a hotel converts it to houses."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player

        # Setup property with hotel
        tile = game.board.get_tile_at(Position(1))
        tile.buy(player.name)
        player.add_owned_tile(1)
        tile.house_count = 5  # Hotel

        # Sell hotel
        player.move_to(Position(1))
        message = SellBuildingUseCase().execute(game)

        assert tile.house_count == 4
        assert "hotel" in message.lower()

    def test_cannot_sell_when_not_owner(self) -> None:
        """Verify that players cannot sell on properties they don't own."""
        game = StartGameUseCase().execute(["Alice", "Bob"])

        # Bob owns the property
        tile = game.board.get_tile_at(Position(1))
        tile.buy("Bob")
        tile.house_count = 1

        # Alice tries to sell
        game.current_player.move_to(Position(1))

        with pytest.raises(ValueError, match="your own property"):
            SellBuildingUseCase().execute(game)

    def test_cannot_sell_unbuilt_property(self) -> None:
        """Verify that players cannot sell on properties without buildings."""
        game = StartGameUseCase().execute(["Alice", "Bob"])
        player = game.current_player

        tile = game.board.get_tile_at(Position(1))
        tile.buy(player.name)
        player.add_owned_tile(1)
        player.move_to(Position(1))

        with pytest.raises(ValueError, match="no house or hotel"):
            SellBuildingUseCase().execute(game)


class TestCommandParserIntegration:
    """Tests for command parser with new commands."""

    def test_command_parser_accepts_save_command(self) -> None:
        """Verify that the command parser accepts 'save' command."""
        from monopoly.presentation.cli.command_parser import CommandParser

        parser = CommandParser()
        command, args = parser.parse("save")
        assert command == "save"
        assert args == []

    def test_command_parser_accepts_load_command(self) -> None:
        """Verify that the command parser accepts 'load' command."""
        from monopoly.presentation.cli.command_parser import CommandParser

        parser = CommandParser()
        command, args = parser.parse("load")
        assert command == "load"
        assert args == []

    def test_command_parser_accepts_sell_command(self) -> None:
        """Verify that the command parser accepts 'sell' command."""
        from monopoly.presentation.cli.command_parser import CommandParser

        parser = CommandParser()
        command, args = parser.parse("sell")
        assert command == "sell"
        assert args == []

    def test_command_parser_all_valid_commands_defined(self) -> None:
        """Verify that all expected commands are in valid commands."""
        from monopoly.presentation.cli.command_parser import CommandParser

        parser = CommandParser()
        expected_commands = {"help", "show", "toggle", "roll", "buy", "build", "sell", "end", "quit", "bail", "save", "load"}
        assert parser.VALID_COMMANDS == expected_commands


class TestGameStatePersistence:
    """Tests for complete game state persistence."""

    def test_game_state_survives_save_load_cycle(self) -> None:
        """Verify complete game state is preserved through save/load."""
        with tempfile.TemporaryDirectory() as tmpdir:
            save_file = Path(tmpdir) / "game.json"
            repository = JsonGameRepository(save_file)

            # Setup complex game state
            game = StartGameUseCase().execute(["Alice", "Bob", "Charlie"])

            # Modify game state
            alice = game.players[0]
            bob = game.players[1]

            # Alice buys a property
            alice_tile = game.board.get_tile_at(Position(1))
            alice_tile.buy(alice.name)
            alice.add_owned_tile(1)

            # Bob pays alice rent
            alice.receive_money(50)
            bob.pay_rent(50)

            # Save
            SaveGameUseCase(repository).execute(game)

            # Load
            loaded_game = LoadGameUseCase(repository).execute()

            # Verify everything is preserved
            loaded_alice = loaded_game.players[0]
            loaded_bob = loaded_game.players[1]
            loaded_alice_tile = loaded_game.board.get_tile_at(Position(1))

            assert loaded_alice_tile.owner_name == "Alice"
            assert loaded_alice.balance.amount == alice.balance.amount
            assert loaded_bob.balance.amount == bob.balance.amount
