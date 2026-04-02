from monopoly.domain.entities.game import Game


class ToggleViewUseCase:
    def execute(self, game: Game) -> str:
        game.toggle_view()
        return game.active_view