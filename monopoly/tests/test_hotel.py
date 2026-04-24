from monopoly.application.use_cases.build_house import BuildHouseUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def _assign_property_to_player(game, tile_id: int, player_name: str) -> None:
    tile = game.board.get_tile_at(Position(tile_id))
    tile.buy(player_name)
    player = game.current_player
    if tile_id not in player.owned_tile_ids:
        player.add_owned_tile(tile_id)


def test_fifth_build_creates_hotel() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    player = game.current_player

    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    tile = game.board.get_tile_at(Position(1))
    tile.house_count = 4
    player.move_to(Position(1))

    result = BuildHouseUseCase().execute(game)

    assert tile.house_count == 5
    assert tile.has_hotel() is True
    assert "hotel" in result.lower()