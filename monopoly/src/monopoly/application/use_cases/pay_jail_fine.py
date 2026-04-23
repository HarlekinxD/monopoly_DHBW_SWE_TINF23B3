from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.money import Money


class PayJailFineUseCase:
    JAIL_FINE = Money(50)

    def execute(self, game: Game) -> str:
        player = game.current_player

        if not player.in_jail:
            raise ValueError("The current player is not in jail.")

        player.pay_money(self.JAIL_FINE)
        player.release_from_jail()

        return f"{player.name} paid 50 and left jail."