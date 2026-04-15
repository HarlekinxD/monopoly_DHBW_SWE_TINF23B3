from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.chance_card import ChanceCard
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


class DrawChanceCardUseCase:
    def __init__(self) -> None:
        self.cards = [
            ChanceCard(
                title="Advance to GO",
                action="move_to",
                target_position=0,
                amount=200,
            ),
            ChanceCard(
                title="Go back three spaces",
                action="move_relative",
                amount=-3,
            ),
            ChanceCard(
                title="Pay poor tax",
                action="pay_money",
                amount=100,
            ),
            ChanceCard(
                title="Bank pays you dividend",
                action="receive_money",
                amount=50,
            ),
            ChanceCard(
                title="Go to jail",
                action="go_to_jail",
                target_position=10,
            ),
        ]

    def execute(self, game: Game) -> str:
        if not hasattr(game, "chance_card_index"):
            game.chance_card_index = 0

        card = self.cards[game.chance_card_index]
        game.chance_card_index = (game.chance_card_index + 1) % len(self.cards)

        player = game.current_player

        if card.action == "receive_money":
            player.receive_money(Money(card.amount))
            return f"{player.name} drew '{card.title}' and received {card.amount}."

        if card.action == "pay_money":
            player.pay_money(Money(card.amount))
            return f"{player.name} drew '{card.title}' and paid {card.amount}."

        if card.action == "move_to":
            player.move_to(Position(card.target_position))
            if card.target_position == 0:
                player.receive_money(Money(card.amount))
            return f"{player.name} drew '{card.title}' and moved to GO."

        if card.action == "move_relative":
            new_position = (player.position.index + card.amount) % game.board.size()
            player.move_to(Position(new_position))
            return f"{player.name} drew '{card.title}' and moved to tile {new_position}."

        if card.action == "go_to_jail":
            player.send_to_jail(Position(card.target_position))
            return f"{player.name} drew '{card.title}' and was sent to jail."

        return f"{player.name} drew '{card.title}', but no action was applied."