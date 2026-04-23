from monopoly.domain.entities.board import Board
from monopoly.domain.entities.property_tile import PropertyTile
from monopoly.domain.entities.railroad_tile import RailroadTile
from monopoly.domain.entities.special_tile import SpecialTile
from monopoly.domain.entities.tax_tile import TaxTile
from monopoly.domain.entities.utility_tile import UtilityTile
from monopoly.domain.tile_color import TileColor
from monopoly.domain.tile_type import TileType
from monopoly.domain.value_objects.money import Money


def create_standard_board() -> Board:
    tiles = []
    tiles.extend(_create_group_zero())
    tiles.extend(_create_group_one())
    tiles.extend(_create_group_two())
    tiles.extend(_create_group_three())
    tiles.extend(_create_group_four())
    tiles.extend(_create_group_five())
    tiles.extend(_create_group_six())
    tiles.extend(_create_group_seven())

    return Board(tiles)


def _create_group_zero() -> list:
    return [
        SpecialTile(tile_id=0, name="LOS", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=1,
            name="Badstraße",
            tile_type=TileType.PROPERTY,
            price=Money(60),
            color=TileColor.PURPLE,
            house_price=Money(50),
            rent_levels=[Money(2), Money(10), Money(30), Money(90), Money(160), Money(250)],
        ),
        SpecialTile(tile_id=2, name="Gemeinschaftsfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=3,
            name="Turmstraße",
            tile_type=TileType.PROPERTY,
            price=Money(60),
            color=TileColor.PURPLE,
            house_price=Money(50),
            rent_levels=[Money(4), Money(20), Money(60), Money(180), Money(320), Money(450)],
        ),
        TaxTile(
            tile_id=4,
            name="Einkommenssteuer",
            tile_type=TileType.TAX,
            tax_amount=Money(200),
        ),
        RailroadTile(
            tile_id=5,
            name="Südbahnhof",
            tile_type=TileType.RAILROAD,
            price=Money(200),
            railroad_rents=[Money(25), Money(50), Money(100), Money(200)],
        ),
        PropertyTile(
            tile_id=6,
            name="Chausseestraße",
            tile_type=TileType.PROPERTY,
            price=Money(100),
            color=TileColor.CYAN,
            house_price=Money(50),
            rent_levels=[Money(6), Money(30), Money(90), Money(270), Money(400), Money(550)],
        ),
        SpecialTile(tile_id=7, name="Ereignisfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=8,
            name="Elisenstraße",
            tile_type=TileType.PROPERTY,
            price=Money(100),
            color=TileColor.CYAN,
            house_price=Money(50),
            rent_levels=[Money(6), Money(30), Money(90), Money(270), Money(400), Money(550)],
        ),
        PropertyTile(
            tile_id=9,
            name="Poststraße",
            tile_type=TileType.PROPERTY,
            price=Money(120),
            color=TileColor.CYAN,
            house_price=Money(50),
            rent_levels=[Money(8), Money(40), Money(100), Money(300), Money(450), Money(600)],
        ),
    ]


def _create_group_one() -> list:
    return [
        SpecialTile(tile_id=10, name="Im Gefängnis (Nur zu Besuch)", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=11,
            name="Seestraße",
            tile_type=TileType.PROPERTY,
            price=Money(140),
            color=TileColor.PINK,
            house_price=Money(100),
            rent_levels=[Money(10), Money(50), Money(150), Money(450), Money(625), Money(750)],
        ),
        UtilityTile(
            tile_id=12,
            name="Elektrizitätswerk",
            tile_type=TileType.UTILITY,
            price=Money(150),
            color=TileColor.WHITE,
            utility_multipliers=[4, 10],
        ),
        PropertyTile(
            tile_id=13,
            name="Hafenstraße",
            tile_type=TileType.PROPERTY,
            price=Money(140),
            color=TileColor.PINK,
            house_price=Money(100),
            rent_levels=[Money(10), Money(50), Money(150), Money(450), Money(625), Money(750)],
        ),
        PropertyTile(
            tile_id=14,
            name="Neue Straße",
            tile_type=TileType.PROPERTY,
            price=Money(160),
            color=TileColor.PINK,
            house_price=Money(100),
            rent_levels=[Money(12), Money(60), Money(180), Money(500), Money(700), Money(900)],
        ),
        RailroadTile(
            tile_id=15,
            name="Westbahnhof",
            tile_type=TileType.RAILROAD,
            price=Money(200),
            railroad_rents=[Money(25), Money(50), Money(100), Money(200)],
        ),
        PropertyTile(
            tile_id=16,
            name="Münchner Straße",
            tile_type=TileType.PROPERTY,
            price=Money(180),
            color=TileColor.ORANGE,
            house_price=Money(100),
            rent_levels=[Money(14), Money(70), Money(200), Money(550), Money(750), Money(950)],
        ),
        SpecialTile(tile_id=17, name="Gemeinschaftsfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=18,
            name="Wiener Straße",
            tile_type=TileType.PROPERTY,
            price=Money(180),
            color=TileColor.ORANGE,
            house_price=Money(100),
            rent_levels=[Money(14), Money(70), Money(200), Money(550), Money(750), Money(950)],
        ),
        PropertyTile(
            tile_id=19,
            name="Berliner Straße",
            tile_type=TileType.PROPERTY,
            price=Money(200),
            color=TileColor.ORANGE,
            house_price=Money(100),
            rent_levels=[Money(16), Money(80), Money(220), Money(600), Money(800), Money(1000)],
        ),
    ]


def _create_group_two() -> list:
    return [
        SpecialTile(tile_id=20, name="Frei Parken", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=21,
            name="Theaterstraße",
            tile_type=TileType.PROPERTY,
            price=Money(220),
            color=TileColor.RED,
            house_price=Money(150),
            rent_levels=[Money(18), Money(90), Money(250), Money(700), Money(875), Money(1050)],
        ),
        SpecialTile(tile_id=22, name="Ereignisfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=23,
            name="Museumstraße",
            tile_type=TileType.PROPERTY,
            price=Money(220),
            color=TileColor.RED,
            house_price=Money(150),
            rent_levels=[Money(18), Money(90), Money(250), Money(700), Money(875), Money(1050)],
        ),
        PropertyTile(
            tile_id=24,
            name="Opernplatz",
            tile_type=TileType.PROPERTY,
            price=Money(240),
            color=TileColor.RED,
            house_price=Money(150),
            rent_levels=[Money(20), Money(100), Money(300), Money(750), Money(925), Money(1100)],
        ),
        RailroadTile(
            tile_id=25,
            name="Nordbahnhof",
            tile_type=TileType.RAILROAD,
            price=Money(200),
            railroad_rents=[Money(25), Money(50), Money(100), Money(200)],
        ),
        PropertyTile(
            tile_id=26,
            name="Lessingstraße",
            tile_type=TileType.PROPERTY,
            price=Money(260),
            color=TileColor.YELLOW,
            house_price=Money(150),
            rent_levels=[Money(22), Money(110), Money(330), Money(800), Money(975), Money(1500)],
        ),
        PropertyTile(
            tile_id=27,
            name="Schillerstraße",
            tile_type=TileType.PROPERTY,
            price=Money(260),
            color=TileColor.YELLOW,
            house_price=Money(150),
            rent_levels=[Money(22), Money(110), Money(330), Money(800), Money(975), Money(1500)],
        ),
        UtilityTile(
            tile_id=28,
            name="Wasserwerk",
            tile_type=TileType.UTILITY,
            price=Money(150),
            color=TileColor.WHITE,
            utility_multipliers=[4, 10],
        ),
        PropertyTile(
            tile_id=29,
            name="Goethestraße",
            tile_type=TileType.PROPERTY,
            price=Money(280),
            color=TileColor.YELLOW,
            house_price=Money(150),
            rent_levels=[Money(24), Money(120), Money(360), Money(850), Money(1025), Money(1200)],
        ),
    ]


def _create_group_three() -> list:
    return [
        SpecialTile(tile_id=30, name="Gehe ins Gefängnis", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=31,
            name="Rathausplatz",
            tile_type=TileType.PROPERTY,
            price=Money(300),
            color=TileColor.GREEN,
            house_price=Money(200),
            rent_levels=[Money(26), Money(130), Money(390), Money(900), Money(1100), Money(1275)],
        ),
        PropertyTile(
            tile_id=32,
            name="Hauptstraße",
            tile_type=TileType.PROPERTY,
            price=Money(300),
            color=TileColor.GREEN,
            house_price=Money(200),
            rent_levels=[Money(26), Money(130), Money(390), Money(900), Money(1100), Money(1275)],
        ),
        SpecialTile(tile_id=33, name="Gemeinschaftsfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=34,
            name="Bahnhofstraße",
            tile_type=TileType.PROPERTY,
            price=Money(320),
            color=TileColor.GREEN,
            house_price=Money(200),
            rent_levels=[Money(28), Money(150), Money(450), Money(1000), Money(1200), Money(1400)],
        ),
        RailroadTile(
            tile_id=35,
            name="Hauptbahnhof",
            tile_type=TileType.RAILROAD,
            price=Money(200),
            railroad_rents=[Money(25), Money(50), Money(100), Money(200)],
        ),
        SpecialTile(tile_id=36, name="Ereignisfeld", tile_type=TileType.SPECIAL),
        PropertyTile(
            tile_id=37,
            name="Parkstraße",
            tile_type=TileType.PROPERTY,
            price=Money(350),
            color=TileColor.DARK_BLUE,
            house_price=Money(200),
            rent_levels=[Money(35), Money(175), Money(500), Money(1100), Money(1300), Money(1500)],
        ),
        TaxTile(
            tile_id=38,
            name="Zusatzsteuer",
            tile_type=TileType.TAX,
            tax_amount=Money(100),
        ),
        PropertyTile(
            tile_id=39,
            name="Schlossallee",
            tile_type=TileType.PROPERTY,
            price=Money(400),
            color=TileColor.DARK_BLUE,
            house_price=Money(200),
            rent_levels=[Money(50), Money(200), Money(600), Money(1400), Money(1700), Money(2000)],
        ),
    ]


def _create_group_four() -> list:
    return []


def _create_group_five() -> list:
    return []


def _create_group_six() -> list:
    return []


def _create_group_seven() -> list:
    return []