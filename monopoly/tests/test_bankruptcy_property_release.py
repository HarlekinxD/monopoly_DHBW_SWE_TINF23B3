from monopoly.application.use_cases.handle_bankruptcy import HandleBankruptcyUseCase
from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position


def test_bankrupt_players_properties_become_buyable_again() -> None:
    game = StartGameUseCase().execute(["Alice", "Bob"])
    alice = game.current_player

    tile = game.board.get_tile_at(Position(1))
    tile.buy("Alice")
    alice.add_owned_tile(1)
    tile.house_count = 2

    alice.is_bankrupt = True
    HandleBankruptcyUseCase().execute(game, alice)

    assert tile.owner_name is None
    assert tile.house_count == 0
    assert alice.owned_tile_ids == []