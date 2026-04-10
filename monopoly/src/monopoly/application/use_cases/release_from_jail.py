from monopoly.domain.entities.game import Game


class ReleaseFromJailUseCase:
    def execute(self, game: Game) -> str:
        player = game.current_player

        if not player.in_jail:
            return f"{player.name} is not in jail."

        player.release_from_jail()
        return f"{player.name} was released from jail."