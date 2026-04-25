from monopoly.domain.card_type import CardType
from monopoly.domain.value_objects.money import Money
from monopoly.domain.entities.card import (MoneyCard, MoveCard, JailFreeCard, NearestRailroadCard, PlayerInteractionMoneyCard, PropertyRepairsCard, RelativeMoveCard)
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

def create_ereigniskarten_deck() -> Deck:
    karten = [
        MoneyCard(card_id=1, card_type=CardType.EREIGNISKARTE, txt="Zahle Schulgeld 150M 💵.", amount=Money(150), is_penalty=True),
        JailFreeCard(card_id=2, card_type=CardType.EREIGNISKARTE, txt="Du kommst aus dem Gefängnis frei 🗝️. (Karte behalten)"),
        MoneyCard(card_id=3, card_type=CardType.EREIGNISKARTE, txt="Strafe für zu schnelles Fahren 🚗. Zahle 15M 💵.", amount=Money(15), is_penalty=True),
        PlayerInteractionMoneyCard(card_id=4, card_type=CardType.EREIGNISKARTE, txt="Du bist zum Vorstand gewählt worden. Zahle jedem Spieler 50M 💵.", amount_per_player=Money(50), player_pays_others=True),
        MoveCard(card_id=5, card_type=CardType.EREIGNISKARTE, txt="Gehe in das Gefängnis 🚓. Begib dich direkt dorthin. Gehe NICHT über Los und ziehe NICHT 200M 💵 ein.", target_position_index=10),
        MoneyCard(card_id=6, card_type=CardType.EREIGNISKARTE, txt="Miete und Anleihezinsen werden fällig, die Bank zahlt dir 150M 💵.", amount=Money(150), is_penalty=False),
        RelativeMoveCard(card_id=7, card_type=CardType.EREIGNISKARTE, txt="Gehe 3 Felder zurück ⬅️.", steps=-3),
        MoveCard(card_id=8, card_type=CardType.EREIGNISKARTE, txt="Rücke vor bis zum Opernplatz 🎭. Wenn du über Los kommst, ziehe 200M 💵 ein.", target_position_index=24),
        MoneyCard(card_id=9, card_type=CardType.EREIGNISKARTE, txt="Die Bank zahlt dir eine Dividende von 50M 💵.", amount=Money(50), is_penalty=False),
        MoneyCard(card_id=10, card_type=CardType.EREIGNISKARTE, txt="Du hast beim Kreuzworträtselwettbewerb gewonnen 📰✏️. Ziehe 100M 💵 ein.", amount=Money(100), is_penalty=False),
        MoveCard(card_id=11, card_type=CardType.EREIGNISKARTE, txt="Rücke vor bis zur Seestraße 🚢. Wenn du über Los kommst, ziehe 200M 💵 ein.", target_position_index=11),
        MoveCard(card_id=12, card_type=CardType.EREIGNISKARTE, txt="Mache einen Ausflug zum Südbahnhof 🚉. Wenn du über Los kommst, ziehe 200M 💵 ein.", target_position_index=5),
        MoveCard(card_id=13, card_type=CardType.EREIGNISKARTE, txt="Rücke vor bis auf Los 🏁.", target_position_index=0),
        MoveCard(card_id=14, card_type=CardType.EREIGNISKARTE, txt="Rücke vor bis zur Schlossallee 🏰.", target_position_index=39),
        NearestRailroadCard(card_id=15, card_type=CardType.EREIGNISKARTE, txt="Rücke vor bis zum nächsten Bahnhof 🚆. Der Eigentümer erhält die doppelte Miete."),
        PropertyRepairsCard(card_id=16, card_type=CardType.EREIGNISKARTE, txt="Lasse alle deine Häuser renovieren 🏗️. Zahle an die Bank 25M für jedes Haus und 100M für jedes Hotel.", cost_per_house=Money(25), cost_per_hotel=Money(100)),
    ]