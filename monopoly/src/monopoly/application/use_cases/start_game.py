from monopoly.application.dto.game_state_dto import GameStateDTO
from monopoly.application.dto.player_state_dto import PlayerStateDTO
from monopoly.domain.entities.game import Game
from monopoly.domain.entities.player import Player
from monopoly.infrastructure.board_factory import create_standard_board


class StartGameUseCase:
    def execute(self, player_names: list[str]) -> GameStateDTO:
        self._validate_player_names(player_names)

        players = [Player(name=name.strip()) for name in player_names]
        board = create_standard_board()

        game = Game(board=board, players=players)
        game.start()

        return self._to_dto(game)

    def _validate_player_names(self, player_names: list[str]) -> None:
        if len(player_names) < 2 or len(player_names) > 7:
            raise ValueError("The game requires 2 to 7 players.")

        normalized_names = [name.strip() for name in player_names]

        if any(not name for name in normalized_names):
            raise ValueError("Player names must not be empty.")

        if len(set(normalized_names)) != len(normalized_names):
            raise ValueError("Player names must be unique.")

    def _to_dto(self, game: Game) -> GameStateDTO:
        return GameStateDTO(
            current_player_name=game.current_player.name,
            current_player_index=game.current_player_index,
            active_view=game.active_view,
            is_started=game.is_started,
            board_size=game.board.size(),
            players=[
                PlayerStateDTO(
                    name=player.name,
                    balance=player.balance.amount,
                    position=player.position.index,
                    owned_tile_ids=player.owned_tile_ids.copy(),
                    is_in_jail=player.in_jail,
                    jail_turns=player.jail_turns,
                )
                for player in game.players
            ],
        )