import pytest

from monopoly.presentation.cli.command_parser import CommandParser



def test_parse_simple_command() -> None:
    parser = CommandParser()

    command, arguments = parser.parse("show")

    assert command == "show"
    assert arguments == []


def test_parse_toggle_command() -> None:
    parser = CommandParser()

    command, arguments = parser.parse("toggle")

    assert command == "toggle"
    assert arguments == []

def test_parse_buy_command() -> None:
    parser = CommandParser()
    command, arguments = parser.parse("buy")

    assert command == "buy"
    assert arguments == []


def test_parse_end_command() -> None:
    parser = CommandParser()
    command, arguments = parser.parse("end")

    assert command == "end"
    assert arguments == []


def test_parse_roll_command() -> None:
    parser = CommandParser()
    command, arguments = parser.parse("roll")

    assert command == "roll"
    assert arguments == []
    
def test_parse_rejects_empty_command() -> None:
    parser = CommandParser()

    with pytest.raises(ValueError, match="must not be empty"):
        parser.parse("   ")


def test_parse_rejects_unknown_command() -> None:
    parser = CommandParser()

    with pytest.raises(ValueError, match="Unknown command"):
        parser.parse("dance")