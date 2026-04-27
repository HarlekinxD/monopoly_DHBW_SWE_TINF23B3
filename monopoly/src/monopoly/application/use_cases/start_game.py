from monopoly.domain.entities.game import Game
from monopoly.domain.entities.player import Player
from monopoly.domain.token import Token
from monopoly.infrastructure.board_factory import create_standard_board


class StartGameUseCase:
    MIN_PLAYERS = 2
    MAX_PLAYERS = 7

    def execute(self, player_names: list[str]) -> Game:
        if len(player_names) < self.MIN_PLAYERS:
            raise ValueError("Game requires 2 to 7 players.")

        if len(player_names) > self.MAX_PLAYERS:
            raise ValueError("Game requires 2 to 7 players.")
        
        if len(set(player_names)) != len(player_names):
            raise ValueError("Player names must be unique.")

        tokens = [
            Token.SHOE,
            Token.WHEELBARROW,
            Token.HAT,
            Token.CAR,
            Token.SHIP,
            Token.IRON,
            Token.DOG,
        ]

        players = [
            Player(name=name, token=tokens[index])
            for index, name in enumerate(player_names)
        ]

        board = create_standard_board()
        game = Game(board=board, players=players)
        game.start()

        return game