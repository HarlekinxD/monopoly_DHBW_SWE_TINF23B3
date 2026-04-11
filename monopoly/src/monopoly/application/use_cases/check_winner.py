from monopoly.domain.entities.game import Game


class CheckWinnerUseCase:
    def execute(self, game: Game) -> str | None:
        active_players = [player for player in game.players if not player.is_bankrupt]

        if len(active_players) == 1:
            return active_players[0].name

        return None