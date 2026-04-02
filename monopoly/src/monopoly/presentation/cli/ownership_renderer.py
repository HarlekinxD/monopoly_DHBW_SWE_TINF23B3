from monopoly.domain.entities.game import Game


class OwnershipRenderer:
    def render(self, game: Game) -> str:
        lines: list[str] = []
        lines.append("=== OWNERSHIP VIEW ===")

        for player in game.players:
            tile_names: list[str] = []

            for tile in game.board.tiles:
                if tile.tile_id in player.owned_tile_ids:
                    tile_names.append(tile.name)

            owned = ", ".join(tile_names) if tile_names else "none"

            lines.append(
                f"{player.name} | money={player.balance.amount} | "
                f"position={player.position.index} | properties={owned}"
            )

        return "\n".join(lines)