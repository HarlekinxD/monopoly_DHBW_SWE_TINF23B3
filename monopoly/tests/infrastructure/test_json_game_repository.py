from pathlib import Path

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.token import Token
from monopoly.domain.value_objects.position import Position
from monopoly.infrastructure.persistence.json_game_repository import JsonGameRepository


def test_json_repository_saves_and_loads_full_game_state(tmp_path: Path) -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    game.current_player_index = 1
    game.active_view = "ownership"
    game.has_rolled_this_turn = True
    game.consecutive_doubles_count = 2
    game.can_buy_current_tile = True
    game.purchased_this_turn = True
    game.current_turn_tile_id = 12
    game.current_round = 3
    game.last_roll = 8
    game.last_message = "Bob paid rent."
    game.eliminated_players = ["Carol"]

    alice = game.players[0]
    bob = game.players[1]

    alice.move_to(Position(7))
    bob.move_to(Position(12))
    alice.token = Token.CAR
    bob.token = Token.DOG
    bob.in_jail = True
    bob.jail_turns = 2

    property_tile = game.board.tiles[1]
    railroad_tile = game.board.tiles[5]
    utility_tile = game.board.tiles[12]

    property_tile.buy("Alice")
    property_tile.house_count = 2
    railroad_tile.buy("Bob")
    utility_tile.buy("Bob")

    alice.owned_tile_ids = [1]
    bob.owned_tile_ids = [5, 12]

    file_path = tmp_path / "savegame.json"
    repository = JsonGameRepository(file_path)

    repository.save(game)
    loaded = repository.load()

    assert loaded is not None
    assert file_path.exists()

    assert loaded.current_player_index == 1
    assert loaded.active_view == "ownership"
    assert loaded.has_rolled_this_turn is True
    assert loaded.consecutive_doubles_count == 2
    assert loaded.can_buy_current_tile is True
    assert loaded.purchased_this_turn is True
    assert loaded.current_turn_tile_id == 12
    assert loaded.current_round == 3
    assert loaded.last_roll == 8
    assert loaded.last_message == "Bob paid rent."
    assert loaded.eliminated_players == ["Carol"]

    loaded_alice = loaded.players[0]
    loaded_bob = loaded.players[1]

    assert loaded_alice.position.index == 7
    assert loaded_bob.position.index == 12
    assert loaded_alice.token == Token.CAR
    assert loaded_bob.token == Token.DOG
    assert loaded_bob.in_jail is True
    assert loaded_bob.jail_turns == 2
    assert loaded_alice.owned_tile_ids == [1]
    assert loaded_bob.owned_tile_ids == [5, 12]

    loaded_property = loaded.board.tiles[1]
    loaded_railroad = loaded.board.tiles[5]
    loaded_utility = loaded.board.tiles[12]

    assert loaded_property.owner_name == "Alice"
    assert loaded_property.house_count == 2
    assert loaded_railroad.owner_name == "Bob"
    assert loaded_utility.owner_name == "Bob"


def test_json_repository_load_returns_none_when_file_missing(tmp_path: Path) -> None:
    repository = JsonGameRepository(tmp_path / "missing.json")

    assert repository.load() is None
