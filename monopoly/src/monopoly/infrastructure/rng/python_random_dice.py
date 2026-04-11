import random

from monopoly.application.ports.random_port import RandomPort


class PythonRandomDice(RandomPort):
    def roll_dice(self) -> int:
        return random.randint(1, 6) + random.randint(1, 6)