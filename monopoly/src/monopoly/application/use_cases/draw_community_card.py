from monopoly.domain.entities.game import Game
from monopoly.domain.value_objects.community_card import CommunityCard
from monopoly.domain.value_objects.money import Money
from monopoly.domain.value_objects.position import Position


class DrawCommunityCardUseCase:
    def __init__(self) -> None:
        self.cards = [
            CommunityCard(
                title="Bank error in your favor",
                action="receive_money",
                amount=200,
            ),
            CommunityCard(
                title="Doctor's fees",
                action="pay_money",
                amount=50,
            ),
            CommunityCard(
                title="Advance to GO",
                action="move_to",
                target_position=0,
                amount=200,
            ),
            CommunityCard(
                title="Go to jail",
                action="go_to_jail",
                target_position=10,
            ),
            CommunityCard(
                title="You inherit 100",
                action="receive_money",
                amount=100,
            ),
        ]

    def execute(self, game: Game) -> str:
        if not hasattr(game, "community_card_index"):
            game.community_card_index = 0

        card = self.cards[game.community_card_index]
        game.community_card_index = (game.community_card_index + 1) % len(self.cards)

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

        if card.action == "go_to_jail":
            player.send_to_jail(Position(card.target_position))
            return f"{player.name} drew '{card.title}' and was sent to jail."

        return f"{player.name} drew '{card.title}', but no action was applied."