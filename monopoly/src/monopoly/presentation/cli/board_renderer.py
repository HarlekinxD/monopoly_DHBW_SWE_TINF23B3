from monopoly.domain.entities.game import Game


class BoardRenderer:
    def render(self, game: Game) -> str:
        lines: list[str] = []
        lines.append("=== BOARD VIEW ===")

        for tile in game.board.tiles:
            players_on_tile = [
                player.name for player in game.players if player.position.index == tile.tile_id
            ]

            owner = getattr(tile, "owner_name", None)
            owner_text = f" | owner={owner}" if owner else ""
            players_text = f" | players={', '.join(players_on_tile)}" if players_on_tile else ""

            lines.append(
                f"[{tile.tile_id:02d}] {tile.name} ({tile.tile_type.value}){owner_text}{players_text}"
            )

        return "\n".join(lines)