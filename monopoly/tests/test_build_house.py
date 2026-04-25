import pytest

from monopoly.application.use_cases.build_house import BuildHouseUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


def _assign_property_to_player(game: Game, tile_id: int, player_name: str) -> None:
    tile = game.board.get_tile_at(Position(tile_id))
    tile.buy(player_name)
    player = game.current_player
    if tile_id not in player.owned_tile_ids:
        player.add_owned_tile(tile_id)


def test_player_can_build_house_when_owning_full_color_group() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    player.move_to(Position(1))

    result = BuildHouseUseCase().execute(game)

    tile = game.board.get_tile_at(Position(1))
    assert tile.house_count == 1
    assert player.balance.amount == 1450
    assert "built a house" in result


def test_player_cannot_build_without_full_color_group() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    player.move_to(Position(1))

    with pytest.raises(ValueError, match="full color group"):
        BuildHouseUseCase().execute(game)


def test_player_cannot_build_on_other_players_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    game.board.get_tile_at(Position(1)).buy("Bob")

    game.current_player.move_to(Position(1))

    with pytest.raises(ValueError, match="your own property"):
        BuildHouseUseCase().execute(game)


def test_player_cannot_build_more_than_hotel() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    tile = game.board.get_tile_at(Position(1))
    tile.house_count = 5
    player.move_to(Position(1))

    with pytest.raises(ValueError, match="already has a hotel"):
        BuildHouseUseCase().execute(game)


def test_player_cannot_build_without_enough_money() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    player.balance = Money(10)
    player.move_to(Position(1))

    with pytest.raises(ValueError, match="enough money"):
        BuildHouseUseCase().execute(game)


def test_fifth_building_becomes_hotel() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    tile = game.board.get_tile_at(Position(1))
    other_tile = game.board.get_tile_at(Position(3))
    tile.house_count = 4
    other_tile.house_count = 4
    player.move_to(Position(1))

    result = BuildHouseUseCase().execute(game)

    assert tile.house_count == 5
    assert tile.has_hotel() is True
    assert "hotel" in result.lower()


def test_player_cannot_build_if_target_is_not_lowest_in_color_group() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    # Cyan gruppe hat 3 strassen: 6, 8, 9
    _assign_property_to_player(game, 6, "Alice")
    _assign_property_to_player(game, 8, "Alice")
    _assign_property_to_player(game, 9, "Alice")

    tile_6 = game.board.get_tile_at(Position(6))
    tile_8 = game.board.get_tile_at(Position(8))
    tile_9 = game.board.get_tile_at(Position(9))

    tile_6.house_count = 1
    tile_8.house_count = 0
    tile_9.house_count = 0

    player.move_to(Position(6))

    with pytest.raises(ValueError, match="distributed evenly"):
        BuildHouseUseCase().execute(game)


def test_player_can_build_when_target_has_lowest_house_count() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 6, "Alice")
    _assign_property_to_player(game, 8, "Alice")
    _assign_property_to_player(game, 9, "Alice")

    tile_6 = game.board.get_tile_at(Position(6))
    tile_8 = game.board.get_tile_at(Position(8))
    tile_9 = game.board.get_tile_at(Position(9))

    tile_6.house_count = 1
    tile_8.house_count = 0
    tile_9.house_count = 0

    player.move_to(Position(8))

    result = BuildHouseUseCase().execute(game)

    assert tile_8.house_count == 1
    assert tile_6.house_count == 1
    assert tile_9.house_count == 0
    assert "built a house" in result