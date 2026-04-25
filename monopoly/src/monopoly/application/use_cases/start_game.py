from monopoly.domain.entities.game import Game
from monopoly.domain.entities.player import Player
from monopoly.domain.token import Token
from monopoly.infrastructure.board_factory import create_standard_board


class StartGameUseCase:
    DEFAULT_TOKENS: list[Token] = [
        Token.SHOE,
        Token.WHEELBARROW,
        Token.HAT,
        Token.CAR,
        Token.SHIP,
        Token.IRON,
        Token.DOG,
    ]

    def execute(self, player_names: list[str]) -> Game:
        self._validate_player_names(player_names)

        players = [Player(name=name.strip()) for name in player_names]
        self._assign_default_tokens(players)
        board = create_standard_board()

        game = Game(board=board, players=players)
        game.start()

        return game

    def _validate_player_names(self, player_names: list[str]) -> None:
        if len(player_names) < 2 or len(player_names) > 7:
            raise ValueError("The game requires 2 to 7 players.")

        normalized_names = [name.strip() for name in player_names]

        if any(not name for name in normalized_names):
            raise ValueError("Player names must not be empty.")

        if len(set(normalized_names)) != len(normalized_names):
            raise ValueError("Player names must be unique.")

    def _assign_default_tokens(self, players: list[Player]) -> None:
        # Einfache, feste Reihenfolge fuer CLI-start.
        for index, player in enumerate(players):
            player.token = self.DEFAULT_TOKENS[index]