#!/usr/bin/env python3
"""Test script to verify money transactions work correctly."""

import sys
sys.path.insert(0, 'src')

from monopoly.application.use_cases.start_game import StartGameUseCase
from monopoly.domain.value_objects.position import Position
from monopoly.application.use_cases.resolve_tile_action import ResolveTileActionUseCase
from monopoly.application.use_cases.play_turn import PlayTurnUseCase
from unittest.mock import Mock

print("=" * 60)
print("TEST 1: 200 Dollar über LOS")
print("=" * 60)

game = StartGameUseCase().execute(['Alice', 'Bob'])
alice = game.players[0]

alice.move_to(Position(38))
print(f"Start: Alice on Position 38, Balance: {alice.balance.amount}")

rng_mock = Mock()
rng_mock.roll_die = Mock(side_effect=[3, 0])
play_turn = PlayTurnUseCase(rng_mock)
result = play_turn.execute(game)

print(f"After crossing GO: Position {alice.position.index}, Balance: {alice.balance.amount}")
if alice.balance.amount == 1700:
    print("✓ 200 Dollar korrekt erhalten!\n")
else:
    print(f"✗ Fehler: erwartet 1700, aber {alice.balance.amount}\n")

print("=" * 60)
print("TEST 2: Einkommensteuer 200 abziehen")
print("=" * 60)

game2 = StartGameUseCase().execute(['Charlie', 'Diana'])
diana = game2.players[1]

print(f"Start: Diana Balance: {diana.balance.amount}")

diana.move_to(Position(4))
game2.current_player_index = 1

resolver = ResolveTileActionUseCase()
tax_result = resolver.execute(game2)

print(f"After tax tile: Diana Balance: {diana.balance.amount}")
print(f"Message: {tax_result}")

if diana.balance.amount == 1300:
    print("✓ 200 Dollar Steuer korrekt abgezogen!\n")
else:
    print(f"✗ Fehler: erwartet 1300, aber {diana.balance.amount}\n")

print("=" * 60)
print("TEST 3: Community Card - Geld erhalten")
print("=" * 60)

game3 = StartGameUseCase().execute(['Eve', 'Frank'])
eve = game3.players[0]

print(f"Start: Eve Balance: {eve.balance.amount}")

eve.move_to(Position(2))
game3.current_player_index = 0

result_card = resolver.execute(game3)
print(f"Card result: {result_card}")
print(f"After card: Eve Balance: {eve.balance.amount}")

if eve.balance.amount > 1500:
    print("✓ Geld wurde korrekt vom Community Card erhalten!\n")
else:
    print(f"✗ Balance nicht erhöht: {eve.balance.amount}\n")

print("=" * 60)
print("TEST 4: Chance Card - Geld erhalten")
print("=" * 60)

game4 = StartGameUseCase().execute(['George', 'Helen'])
george = game4.players[0]

print(f"Start: George Balance: {george.balance.amount}")

george.move_to(Position(7))  # Ereignisfeld
game4.current_player_index = 0

result_chance = resolver.execute(game4)
print(f"Chance result: {result_chance}")
print(f"After chance: George Balance: {george.balance.amount}\n")
