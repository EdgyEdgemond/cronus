import io
from unittest import mock

import pytest

import cronus.parser
from cronus.parser import CronParser


def test_parser_init():
    parser = CronParser("crontab", "command")
    assert parser._crontab == "crontab"
    assert parser._command == "command"
    assert parser._parsed_values == {}


def test_parser_parse_populates_internal_dict():
    parser = CronParser("1 2 3 4 5", "command")
    parser.parse()

    assert parser._parsed_values == {
        "minute": {1},
        "hour": {2},
        "day of month": {3},
        "month": {4},
        "day of week": {5},
    }


def test_parser_parse_parses_correct_sections(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_section", mock.Mock())

    parser = CronParser("1 2 3 4 5", "command")
    parser.parse()

    assert cronus.parser.parse_section.call_args_list == [
        mock.call("1", 0, 59),
        mock.call("2", 0, 23),
        mock.call("3", 0, 30, True),
        mock.call("4", 0, 11, True),
        mock.call("5", 0, 6),
    ]


def test_parser_parse_replaces_weekday_strings_with_number_representation(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_section", mock.Mock())

    parser = CronParser("1 2 3 4 FRI", "command")
    parser.parse()

    assert cronus.parser.parse_section.call_args_list == [
        mock.call("1", 0, 59),
        mock.call("2", 0, 23),
        mock.call("3", 0, 30, True),
        mock.call("4", 0, 11, True),
        mock.call("5", 0, 6),
    ]


def test_parser_parse_replaces_month_strings_with_number_representation(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_section", mock.Mock())

    parser = CronParser("1 2 3 JAN-MAR 5", "command")
    parser.parse()

    assert cronus.parser.parse_section.call_args_list == [
        mock.call("1", 0, 59),
        mock.call("2", 0, 23),
        mock.call("3", 0, 30, True),
        mock.call("1-3", 0, 11, True),
        mock.call("5", 0, 6),
    ]


def test_parser_parse_replaces_first_instance_of_month_strings_with_number_representation(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_section", mock.Mock())

    parser = CronParser("1 2 3 JANJAN 5", "command")
    parser.parse()

    assert cronus.parser.parse_section.call_args_list == [
        mock.call("1", 0, 59),
        mock.call("2", 0, 23),
        mock.call("3", 0, 30, True),
        mock.call("1JAN", 0, 11, True),
        mock.call("5", 0, 6),
    ]


def test_parser_parse_raises_on_invalid_crontab(monkeypatch):
    parser = CronParser("1 2 3 4 5 6", "command")
    with pytest.raises(SyntaxError) as exc:
        parser.parse()

    assert str(exc.value) == "Invalid crontab"


def test_parser_parse_with_invalid_strings_raises_syntax_error():
    parser = CronParser("*/15 0 1,15 * MONMON", "/usr/bin/find")
    with pytest.raises(SyntaxError) as exc:
        parser.parse()

    assert str(exc.value) == "Invalid range"


def test_parser_render():
    mock_stdout = io.StringIO()

    parser = CronParser("1 2 3 4 5", "command")
    parser.parse()
    with mock.patch("sys.stdout", mock_stdout):
        parser.render()

    assert mock_stdout.getvalue().split("\n")[:-1] == [
        "minute          1",
        "hour            2",
        "day of month    3",
        "month           4",
        "day of week     5",
        "command         command",
    ]


def test_parser_render_example():
    mock_stdout = io.StringIO()

    parser = CronParser("*/15 0 1,15 * 1-5", "/usr/bin/find")
    parser.parse()
    with mock.patch("sys.stdout", mock_stdout):
        parser.render()

    assert mock_stdout.getvalue().split("\n")[:-1] == [
        "minute          0 15 30 45",
        "hour            0",
        "day of month    1 15",
        "month           1 2 3 4 5 6 7 8 9 10 11 12",
        "day of week     1 2 3 4 5",
        "command         /usr/bin/find",
    ]


def test_parser_render_example_with_strings():
    mock_stdout = io.StringIO()

    parser = CronParser("*/15 0 1,15 * MON-FRI", "/usr/bin/find")
    parser.parse()
    with mock.patch("sys.stdout", mock_stdout):
        parser.render()

    assert mock_stdout.getvalue().split("\n")[:-1] == [
        "minute          0 15 30 45",
        "hour            0",
        "day of month    1 15",
        "month           1 2 3 4 5 6 7 8 9 10 11 12",
        "day of week     1 2 3 4 5",
        "command         /usr/bin/find",
    ]
