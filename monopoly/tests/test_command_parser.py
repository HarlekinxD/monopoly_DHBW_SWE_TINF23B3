import pytest

from monopoly.presentation.cli.command_parser import CommandParser


def test_parse_simple_command() -> None:
    parser = CommandParser()

    command, arguments = parser.parse("show")

    assert command == "show"
    assert arguments == []


def test_parse_command_with_arguments() -> None:
    parser = CommandParser()

    command, arguments = parser.parse("view board")

    assert command == "view"
    assert arguments == ["board"]


def test_parse_rejects_empty_command() -> None:
    parser = CommandParser()

    with pytest.raises(ValueError, match="must not be empty"):
        parser.parse("   ")


def test_parse_rejects_unknown_command() -> None:
    parser = CommandParser()

    with pytest.raises(ValueError, match="Unknown command"):
        parser.parse("dance")