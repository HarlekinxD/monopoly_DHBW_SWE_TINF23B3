from monopoly.domain.entities.game import Game
from monopoly.domain.entities.property_tile import PropertyTile


class OwnershipRenderer:
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

            lines.append(
                f"{player.name} | money={player.balance.amount} | "
                f"position={player.position.index} | properties={owned}"
            )

        return "\n".join(lines)