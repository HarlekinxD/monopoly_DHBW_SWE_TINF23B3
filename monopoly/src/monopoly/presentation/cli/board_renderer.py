import os

from monopoly.domain.entities.game import Game
from monopoly.domain.entities.ownable_tile import OwnableTile
from monopoly.domain.entities.player import Player
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.entities.tile import Tile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.token import Token


class BoardRenderer:
    CELL_INNER_WIDTH = 12
    CELL_HEIGHT = 3

    RESET = "\033[0m"
    COLOR_CODES = {
        "PU": "\033[95m",   # purple / magenta
        "CY": "\033[96m",   # cyan
        "PI": "\033[95m",   # pink -> magenta-ish
        "OR": "\033[93m",   # orange -> gelb als Ersatz
        "RE": "\033[91m",   # red
        "YE": "\033[93m",   # yellow
        "GR": "\033[92m",   # green
        "BL": "\033[94m",   # dark blue -> blue
        "WH": "\033[97m",   # white
    }

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

    def __init__(self) -> None:
        self._enable_windows_ansi()


    def _enable_windows_ansi(self) -> None:
        if os.name == "nt":
            os.system("")
    
    def _colorize(self, text: str, color_code: str) -> str:
        if not color_code or color_code not in self.COLOR_CODES:
            return text
        return f"{self.COLOR_CODES[color_code]}{text}{self.RESET}"
    
    def render(self, game: Game) -> str:
        return self.render_square(game)

    def render_square(self, game: Game) -> str:
        tiles = game.board.tiles

        top_row = [tiles[i] for i in range(0, 11)]          # 00..10
        right_col = [tiles[i] for i in range(11, 20)]       # 11..19
        bottom_row = [tiles[i] for i in range(20, 31)]      # 20..30
        left_col = [tiles[i] for i in range(31, 40)]        # 31..39

        left_tiles = list(reversed(left_col))               # 39..31
        right_tiles = list(right_col)                       # 11..19
        bottom_tiles = list(reversed(bottom_row))           # 30..20

        top_block = self._render_horizontal_row(top_row, game)
        bottom_block = self._render_horizontal_row(bottom_tiles, game)

        side_width = self._row_width(1)
        full_width = self._row_width(11)
        center_width = full_width - (2 * side_width)

        center_panel = self._build_center_panel(
            game,
            width=center_width,
            height=len(left_tiles) * (self.CELL_HEIGHT + 1),
        )

        lines: list[str] = []
        lines.extend(top_block)

        center_index = 0
        for index, (left_tile, right_tile) in enumerate(zip(left_tiles, right_tiles)):
            include_top_border = index != 0

            left_block = self._render_single_cell(
                left_tile,
                game,
                include_top_border=include_top_border,
            )
            right_block = self._render_single_cell(
                right_tile,
                game,
                include_top_border=include_top_border,
            )

            for row in range(len(left_block)):
                lines.append(left_block[row] + center_panel[center_index] + right_block[row])
                center_index += 1

        lines.extend(bottom_block)
        return "\n".join(lines)

    def render_list(self, game: Game) -> str:
        lines = ["=" * 100, " " * 35 + "MONOPOLY BOARD LIST VIEW", "=" * 100]
        for tile in game.board.tiles:
            lines.append(self._render_tile_line(tile, game))
        lines.append("=" * 100)
        return "\n".join(lines)

    def _render_horizontal_row(self, tiles: list[Tile], game: Game) -> list[str]:
        border = "+" + "+".join("-" * self.CELL_INNER_WIDTH for _ in tiles) + "+"
        contents = [self._cell_content(tile, game) for tile in tiles]

        lines = [border]
        for row in range(self.CELL_HEIGHT):
            lines.append("|" + "|".join(content[row] for content in contents) + "|")
        return lines

    def _render_single_cell(
        self,
        tile: Tile,
        game: Game,
        include_top_border: bool = True,
    ) -> list[str]:
        border = "+" + "-" * self.CELL_INNER_WIDTH + "+"
        content = [f"|{line}|" for line in self._cell_content(tile, game)]

        if include_top_border:
            return [border] + content
        return content

    def _cell_content(self, tile: Tile, game: Game) -> list[str]:
        tile_id = f"{tile.tile_id:02}"
        players = self._players_text(tile.tile_id, game)
        owner = self._owner_text(tile)
        color = self._color_text(tile)
        houses = self._house_text(tile)
        tile_type = self._type_text(tile)

        line1 = self._fit(f"{tile_id} {self._short(tile.name, 9)}")
        line2 = self._fit(f"P:{players} O:{owner} C:{color}")

        if color != "--":
            line3_plain = self._fit(f"H:{houses} T:{tile_type}")
            color_text = self._colorize(color, color)
            # Farbe separat rechts anhängen, wenn Platz ist
            base = f"H:{houses} T:{tile_type}"
            if len(base) + 1 + len(color) <= self.CELL_INNER_WIDTH:
                line3_plain = self._fit(f"{base} {color}")
                line3 = line3_plain.replace(color, color_text, 1)
            else:
                line3 = line3_plain
        else:
            line3 = self._fit(f"H:{houses} T:{tile_type}")

        return [line1, line2, line3]

    def _build_center_panel(self, game: Game, width: int, height: int) -> list[str]:
        current_round = getattr(game, "current_round", 1)
        last_roll = getattr(game, "last_roll", "-")
        last_message = getattr(game, "last_message", "")

        player = game.current_player
        tile_name = game.board.get_tile_at(player.position).name

        panel_width = min(36, max(28, width - 8))
        left_pad = max(0, (width - panel_width) // 2)
        right_pad = width - panel_width - left_pad

        def blank() -> str:
            return " " * width

        def border() -> str:
            return (" " * left_pad) + "+" + ("-" * (panel_width - 2)) + "+" + (" " * right_pad)

        def text(value: str, align: str = "left") -> str:
            inner = panel_width - 2
            value = value[:inner]
            if align == "center":
                inner_text = value.center(inner)
            else:
                inner_text = value.ljust(inner)
            return (" " * left_pad) + "|" + inner_text + "|" + (" " * right_pad)

        status_box = [
            border(),
            text("MONOPOLY", "center"),
            text("-" * 22, "center"),
            text(f"RUNDE: {current_round}"),
            text(f"SPIELER: {player.name}"),
            text(f"FIGUR: {self._token_symbol(player)}"),
            text(f"GELD: {player.balance.amount}"),
            text(f"FELD: {player.position.index}"),
            text(f"NAME: {self._short(tile_name, panel_width - 8)}"),
            text(f"WURF: {last_roll}"),
            text(f"AKTION: {self._short(last_message, panel_width - 10)}"),
            border(),
        ]

        legend_box = [
            border(),
            text("LEGENDE", "center"),
            text("P = Spieler auf Feld"),
            text(f"FIGUREN: {self._legend_tokens()}"),
            text("O = Besitzer"),
            text("C = Farbe"),
            text("H = Haeuser / HT = Hotel"),
            text("T = Typ"),
            border(),
        ]

        # beide Boxen mit Abstand dazwischen
        content = []
        content.extend(status_box)
        content.append(blank())
        content.append(blank())
        content.extend(legend_box)

        top_blank = max(0, (height - len(content)) // 2)
        bottom_blank = max(0, height - len(content) - top_blank)

        result = []
        result.extend(blank() for _ in range(top_blank))
        result.extend(content)
        result.extend(blank() for _ in range(bottom_blank))

        return result[:height]

    def _row_width(self, tile_count: int) -> int:
        return 1 + tile_count * self.CELL_INNER_WIDTH + tile_count

    def _short(self, text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        if max_len <= 1:
            return text[:max_len]
        return text[: max_len - 1] + "…"

    def _fit(self, text: str) -> str:
        return text[: self.CELL_INNER_WIDTH].ljust(self.CELL_INNER_WIDTH)

    def _players_text(self, tile_id: int, game: Game) -> str:
        players = [
            self._token_symbol(p)
            for p in game.players
            if p.position.index == tile_id and not p.is_bankrupt
        ]
        return "".join(players) if players else "-"

    def _token_symbol(self, player: Player) -> str:
        if player.token is not None:
            return self._token_symbols().get(player.token, player.name[:1].upper())
        return player.name[:1].upper()

    def _token_symbols(self) -> dict[Token, str]:
        # Default ist ASCII damit es in praktisch jedem terminal lesbar bleibt.
        style = os.environ.get("MONOPOLY_TOKEN_STYLE", "ascii").strip().lower()
        if style == "emoji":
            return self.TOKEN_SYMBOLS_EMOJI
        return self.TOKEN_SYMBOLS_ASCII

    def _legend_tokens(self) -> str:
        symbols = self._token_symbols()
        ordered = [
            Token.SHOE,
            Token.WHEELBARROW,
            Token.HAT,
            Token.CAR,
            Token.SHIP,
            Token.IRON,
            Token.DOG,
        ]
        return " ".join(symbols[token] for token in ordered)

    def _owner_text(self, tile: Tile) -> str:
        if isinstance(tile, OwnableTile) and tile.owner_name:
            return tile.owner_name[:2].upper()
        return "--"

    def _color_text(self, tile: Tile) -> str:
        if hasattr(tile, "color"):
            return getattr(tile, "color").value[:2].upper()
        return "--"

    def _house_text(self, tile: Tile) -> str:
        if isinstance(tile, PropertyTile):
            if tile.house_count == 5:
                return "HT"
            if tile.house_count > 0:
                return str(tile.house_count)
        return "--"

    def _type_text(self, tile: Tile) -> str:
        if isinstance(tile, PropertyTile):
            return "PR"
        if isinstance(tile, RailroadTile):
            return "RR"
        if isinstance(tile, UtilityTile):
            return "UT"
        if isinstance(tile, TaxTile):
            return "TX"
        return "SP"

    def _render_horizontal_row(self, tiles: list[Tile], game: Game) -> list[str]:
        border = "+" + "+".join("-" * self.CELL_INNER_WIDTH for _ in tiles) + "+"
        contents = [self._cell_content(tile, game) for tile in tiles]

        lines = [border]
        for row in range(self.CELL_HEIGHT):
            lines.append("|" + "|".join(content[row] for content in contents) + "|")

        lines.append(border)
        return lines
    
    def _render_tile_line(self, tile: Tile, game: Game) -> str:
        players = [
            f"{p.name}({self._token_symbol(p)})"
            for p in game.players
            if p.position.index == tile.tile_id and not p.is_bankrupt
        ]
        players_text = ", ".join(players) if players else "-"

        owner_text = "-"
        if isinstance(tile, OwnableTile) and tile.owner_name:
            owner_text = tile.owner_name

        houses_text = "-"
        if isinstance(tile, PropertyTile):
            houses_text = self._house_text(tile)

        return (
            f"[{tile.tile_id:02}] {tile.name:<25} | "
            f"type={self._type_text(tile):<2} | "
            f"owner={owner_text:<10} | "
            f"houses={houses_text:<4} | "
            f"players={players_text}"
        )