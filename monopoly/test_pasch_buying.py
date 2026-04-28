#!/usr/bin/env python3
"""Test Pasch logic: Buying must happen BEFORE extra roll."""

import sys
sys.path.insert(0, 'src')

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from monopoly.application.use_cases.buy_property import BuyPropertyUseCase
from monopoly.infrastructure.rng.python_random_dice import PythonRandomDice
from unittest.mock import Mock

print("=" * 70)
print("TEST: PASCH-LOGIK - Kaufen vor erneutem Würfeln")
print("=" * 70)

game = StartGameUseCase().execute(['Alice', 'Bob'])
alice = game.players[0]
bob = game.players[1]

print(f"\nStart: Alice hat {alice.balance.amount} Dollar")
print(f"Position: {alice.position.index} (LOS)")

# Würfel einen Pasch (1, 1) - Alice soll auf Position 2 landen
# ABER: Position 2 ist Gemeinschaftsfeld. Position 1 ist Badstraße (Eigenschaft)
# Also Alice von 0 zu 1: (1,1) würde zu Position 2 gehen
# Besser: Alice zu Position 1: Das geht nicht direkt mit Pasch
# Machen wir Alice von 0 zu 1 mit (0,1)? Das ist kein Pasch
# OK: Alice von 0 mit Pasch (3,3) → Position 6 (Chausseestraße)
rng_mock = Mock()
rng_mock.roll_die = Mock(side_effect=[3, 3])  # Pasch: 3+3=6, landet auf Position 6 (Chausseestraße)

play_turn = PlayTurnUseCase(rng_mock)
result = play_turn.execute(game)

print(f"\n1️⃣ Nach Pasch:")
print(f"   Position: {alice.position.index}")
print(f"   Tile: {result['tile_name']}")
print(f"   Message: {result['message']}")
print(f"   can_buy: {result['can_buy']}")  # MUSS True sein!
print(f"   has_rolled_this_turn: {game.has_rolled_this_turn}")  # MUSS False sein!

tile = game.board.get_tile_at(alice.position)
print(f"   Tile ist frei: {not tile.is_owned()}")

if result['can_buy']:
    print(f"\n✓ Spieler KANN kaufen (vor Neuroll)")
    
    # Jetzt Kaufen
    buy_use_case = BuyPropertyUseCase()
    buy_result = buy_use_case.execute(game)
    print(f"\n2️⃣ Nach Kauf:")
    print(f"   Message: {buy_result}")
    print(f"   Balance: {alice.balance.amount} (gekauft für {tile.price.amount})")
    
    # Jetzt MUSS has_rolled_this_turn noch immer False sein
    # damit der Spieler nochmal würfeln kann!
    print(f"   has_rolled_this_turn: {game.has_rolled_this_turn}")
    
    if not game.has_rolled_this_turn:
        print(f"\n✓ Spieler DARF nochmal würfeln (Pasch-Neuroll erlaubt)")
    else:
        print(f"\n✗ FEHLER: Spieler darf NICHT nochmal würfeln!")
        
else:
    print(f"\n✗ FEHLER: Spieler kann nicht kaufen!")

print()
