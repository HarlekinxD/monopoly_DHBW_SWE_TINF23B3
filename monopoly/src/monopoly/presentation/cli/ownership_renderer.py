import os

from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.token import Token


class OwnershipRenderer:
    TOKEN_SYMBOLS_ASCII: dict[Token, str] = {
        Token.SHOE: "S",
        Token.WHEELBARROW: "W",
        Token.HAT: "H",
        Token.CAR: "A",
        Token.SHIP: "K",
        Token.IRON: "I",
        Token.DOG: "D",
        Token.CAT: "C",
    }

    TOKEN_SYMBOLS_EMOJI: dict[Token, str] = {
        Token.SHOE: "👞",
        Token.WHEELBARROW: "🛒",
        Token.HAT: "🎩",
        Token.CAR: "🚗",
        Token.SHIP: "🚢",
        Token.IRON: "🧺",
        Token.DOG: "🐕",
        Token.CAT: "🐈",
    }

    def render(self, game: Game) -> str:
        lines: list[str] = []
        lines.append("=== OWNERSHIP VIEW ===")

        for player in game.players:
            tile_descriptions: list[str] = []

            for tile in game.board.tiles:
                if tile.tile_id in player.owned_tile_ids:
                    if isinstance(tile, PropertyTile):
                        if tile.house_count == 5:
                            building = "hotel"
                        elif tile.house_count > 0:
                            building = f"{tile.house_count} house(s)"
                        else:
                            building = "no houses"
                        tile_descriptions.append(f"{tile.name} ({building})")
                    else:
                        tile_descriptions.append(tile.name)

            owned = ", ".join(tile_descriptions) if tile_descriptions else "none"
            token_text = player.token.value if player.token is not None else "-"
            token_symbol = self._token_symbols().get(player.token, "?") if player.token is not None else "-"

            lines.append(
                f"{player.name} ({token_symbol} {token_text}) | money={player.balance.amount} | "
                f"position={player.position.index} | properties={owned}"
            )

        return "\n".join(lines)

    def _token_symbols(self) -> dict[Token, str]:
        style = os.environ.get("MONOPOLY_TOKEN_STYLE", "ascii").strip().lower()
        if style == "emoji":
            return self.TOKEN_SYMBOLS_EMOJI
        return self.TOKEN_SYMBOLS_ASCII