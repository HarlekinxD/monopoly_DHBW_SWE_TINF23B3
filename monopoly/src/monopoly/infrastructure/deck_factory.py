from monopoly.domain.card_type import CardType
from monopoly.domain.value_objects.money import Money
from monopoly.domain.entities.card import (MoneyCard, MoveCard, JailFreeCard, PlayerInteractionMoneyCard, PropertyRepairsCard)
#import the deck class to create the decks with the cards
from monopoly.domain.entities.deck import Deck

def create_gemeinschaftskarten_deck() -> Deck:
    """
    Returns:
        Deck: returns a deck of Gemeinschaftskarten with the predefined cards and their effects
    
    """
    karten = [
        MoneyCard(card_id=1, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Arztkosten 🏥. Zahle 50M 💵.", amount=Money(50), is_penalty=True),
        MoneyCard(card_id=2, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Bank-Irrtum zu deinen Gunsten 🏦! Ziehe 200M 💵 ein.", amount=Money(200), is_penalty=False),
        MoveCard(card_id=3, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Gehe zurück auf Los ▶️.", target_position_index=0),
        MoneyCard(card_id=4, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Einkommenssteuer-Rückzahlung 🧾! Ziehe 20M 💵 ein.", amount=Money(20), is_penalty=False),
        MoneyCard(card_id=5, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Krankenhausgebühren 🚑. Zahle an das Krankenhaus 100M 💵.", amount=Money(100), is_penalty=True),
        MoveCard(card_id=6, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Gehe in das Gefängnis 🚓. Begib dich direkt dorthin. Gehe NICHT über Los und ziehe NICHT 200M 💵 ein.", target_position_index=10),
        JailFreeCard(card_id=7, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Du kommst aus dem Gefängnis frei 🗝️. (Karte behalten)"),
        PlayerInteractionMoneyCard(card_id=8, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Es ist dein Geburtstag 🎂! Ziehe von jedem Spieler 10M 💵 ein.", amount_per_player=Money(10), player_pays_others=False),
        MoneyCard(card_id=9, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Aus Verkäufen von Aktien erhältst du 50M 📈.", amount=Money(50), is_penalty=False),
        MoneyCard(card_id=10, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Jahresrente wird fällig 👵👴. Ziehe 100M 💵 ein.", amount=Money(100), is_penalty=False),
        MoneyCard(card_id=11, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Du hast den zweiten Preis in einer Schönheitskonkurrenz gewonnen 💄👑. Ziehe 10M 💵 ein.", amount=Money(10), is_penalty=False),
        MoneyCard(card_id=12, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Du erbst 100M 📜💵.", amount=Money(100), is_penalty=False),
        MoneyCard(card_id=13, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Zahle deine Versicherungssumme 🛡️: 50M 💵.", amount=Money(50), is_penalty=True),
        PropertyRepairsCard(card_id=14, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Zahle Straßenausbesserungssteuern 🚧: 40M 💵 je Haus 🏠, 115M 💵 je Hotel 🏨.", cost_per_house=Money(40), cost_per_hotel=Money(115)),
        MoneyCard(card_id=15, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Du erhältst auf Vorzugsaktien 7% Dividende 📊: 25M 💵.", amount=Money(25), is_penalty=False),
        MoneyCard(card_id=16, card_type=CardType.GEMEINSCHAFTSKARTE, txt="Du hast im Kreuzworträtselwettbewerb gewonnen 📰✏️. Ziehe 100M 💵 ein.", amount=Money(100), is_penalty=False),
    ]
    return Deck(deck_type=CardType.GEMEINSCHAFTSKARTE, cards=karten)