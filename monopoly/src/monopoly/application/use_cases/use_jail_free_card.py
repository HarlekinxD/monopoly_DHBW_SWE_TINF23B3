from monopoly.domain.entities.game import Game


class UseJailFreeCardUseCase:
    def execute(self, game: Game) -> str:
        player = game.current_player

        if not player.in_jail:
            raise ValueError("The current player is not in jail.")

        if not player.use_jail_free_card():
            raise ValueError("The current player does not have a jail free card.")

        player.release_from_jail()

        return f"{player.name} used a 'Get out of jail free' card and left jail."
