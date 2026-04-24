from monopoly.application.use_cases.build_house import BuildHouseUseCase
from monopoly.application.use_cases.pay_rent import PayRentUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def _assign_property_to_player(game, tile_id: int, player_name: str) -> None:
    tile = game.board.get_tile_at(Position(tile_id))
    tile.buy(player_name)
    player = game.players[0]
    if tile_id not in player.owned_tile_ids:
        player.add_owned_tile(tile_id)


def test_house_increases_rent_payment() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])

    alice = game.players[0]
    _assign_property_to_player(game, 1, "Alice")
    _assign_property_to_player(game, 3, "Alice")

    alice.move_to(Position(1))
    BuildHouseUseCase().execute(game)

    game.next_player()
    bob = game.current_player
    bob.move_to(Position(1))

    PayRentUseCase().execute(game)

    assert bob.balance.amount == 1490
    assert alice.balance.amount == 1460