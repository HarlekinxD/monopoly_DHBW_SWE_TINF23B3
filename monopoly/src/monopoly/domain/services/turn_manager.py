from monopoly.domain.entities.game import Game


class TurnManager:
    def advance_to_next_player(self, game: Game) -> None:
        game.next_player()