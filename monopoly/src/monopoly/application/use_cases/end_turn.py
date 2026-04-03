from monopoly.domain.entities.game import Game


class EndTurnUseCase:
    def execute(self, game: Game) -> str:
        game.next_player()
        return game.current_player.name