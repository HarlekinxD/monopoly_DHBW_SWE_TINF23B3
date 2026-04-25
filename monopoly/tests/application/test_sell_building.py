import pytest

from monopoly.application.use_cases.sell_building import SellBuildingUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.position import Position


def _assign_property_to_current_player(game: Game, tile_id: int) -> None:
    player = game.current_player
    tile = game.board.get_tile_at(Position(tile_id))
    tile.buy(player.name)
    if tile_id not in player.owned_tile_ids:
        player.add_owned_tile(tile_id)


def test_player_can_sell_house_and_get_half_house_price() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_current_player(game, 1)
    _assign_property_to_current_player(game, 3)

    tile_1 = game.board.get_tile_at(Position(1))
    tile_3 = game.board.get_tile_at(Position(3))
    tile_1.house_count = 1
    tile_3.house_count = 1

    player.move_to(Position(1))
    balance_before = player.balance.amount

    result = SellBuildingUseCase().execute(game)

    assert tile_1.house_count == 0
    assert player.balance.amount == balance_before + 25
    assert "sold a house" in result


def test_player_cannot_sell_building_when_no_house_present() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    _assign_property_to_current_player(game, 1)
    game.current_player.move_to(Position(1))

    with pytest.raises(ValueError, match="no house or hotel"):
        SellBuildingUseCase().execute(game)


def test_player_cannot_sell_on_other_players_property() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    # Bob wird owner von tile 1
    tile = game.board.get_tile_at(Position(1))
    tile.buy("Bob")
    tile.house_count = 1

    game.current_player.move_to(Position(1))

    with pytest.raises(ValueError, match="your own property"):
        SellBuildingUseCase().execute(game)


def test_player_cannot_sell_on_special_tile() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    game.current_player.move_to(Position(0))  # LOS ist special tile

    with pytest.raises(ValueError, match="only be sold on properties"):
        SellBuildingUseCase().execute(game)


def test_hotel_is_downgraded_to_four_houses_on_sell() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_current_player(game, 1)
    _assign_property_to_current_player(game, 3)

    tile_1 = game.board.get_tile_at(Position(1))
    tile_3 = game.board.get_tile_at(Position(3))
    tile_1.house_count = 5
    tile_3.house_count = 5

    player.move_to(Position(1))
    balance_before = player.balance.amount

    result = SellBuildingUseCase().execute(game)

    assert tile_1.house_count == 4
    assert player.balance.amount == balance_before + 25
    assert "sold a hotel" in result


def test_player_cannot_sell_if_target_is_not_highest_in_color_group() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    # Cyan gruppe: 6, 8, 9
    _assign_property_to_current_player(game, 6)
    _assign_property_to_current_player(game, 8)
    _assign_property_to_current_player(game, 9)

    tile_6 = game.board.get_tile_at(Position(6))
    tile_8 = game.board.get_tile_at(Position(8))
    tile_9 = game.board.get_tile_at(Position(9))

    tile_6.house_count = 2
    tile_8.house_count = 1
    tile_9.house_count = 1

    # Verkauf von tile 8 waere ungleichmaessig (nicht hoechster stand)
    game.current_player.move_to(Position(8))

    with pytest.raises(ValueError, match="sold evenly"):
        SellBuildingUseCase().execute(game)


def test_player_can_sell_if_target_is_highest_in_color_group() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    _assign_property_to_current_player(game, 6)
    _assign_property_to_current_player(game, 8)
    _assign_property_to_current_player(game, 9)

    tile_6 = game.board.get_tile_at(Position(6))
    tile_8 = game.board.get_tile_at(Position(8))
    tile_9 = game.board.get_tile_at(Position(9))

    tile_6.house_count = 2
    tile_8.house_count = 1
    tile_9.house_count = 1

    game.current_player.move_to(Position(6))

    SellBuildingUseCase().execute(game)

    assert tile_6.house_count == 1
    assert tile_8.house_count == 1
    assert tile_9.house_count == 1
