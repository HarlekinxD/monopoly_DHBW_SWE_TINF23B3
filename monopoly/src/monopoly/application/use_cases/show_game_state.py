from monopoly.domain.entities.game import Game


class ShowGameStateUseCase:
    def execute(self, game: Game) -> Game:
        return game