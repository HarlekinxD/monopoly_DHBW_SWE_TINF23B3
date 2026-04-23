from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.money import Money


class AttemptLeaveJailUseCase:
    JAIL_FINE = Money(50)

    def execute(self, game: Game, die_one: int, die_two: int) -> dict:
        player = game.current_player

        if not player.in_jail:
            raise ValueError("The current player is not in jail.")

        if die_one == die_two:
            player.release_from_jail()
            total = die_one + die_two
            return {
                "released": True,
                "must_pay": False,
                "dice_total": total,
                "message": f"{player.name} rolled doubles and left jail.",
            }

        player.increment_jail_turn()

        if player.jail_turns >= 3:
            player.pay_money(self.JAIL_FINE)
            player.release_from_jail()
            total = die_one + die_two
            return {
                "released": True,
                "must_pay": True,
                "dice_total": total,
                "message": f"{player.name} paid 50 after 3 failed attempts and left jail.",
            }

        return {
            "released": False,
            "must_pay": False,
            "dice_total": None,
            "message": f"{player.name} did not roll doubles and stays in jail.",
        }