from unittest import mock

import cronus.parser
from cronus.parser import parse_section


def test_parse_section_calls_parse_piece_with_each_comma_separated_piece(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_piece", mock.Mock(return_value=("piece", None, False, False)))
    monkeypatch.setattr(cronus.parser, "extract_ranges", mock.Mock(return_value=[(1, 10)]))
    parse_section("1,2,3", 1, 10)

    assert cronus.parser.parse_piece.call_args_list == [
        mock.call("1"),
        mock.call("2"),
        mock.call("3"),
    ]


def test_parse_section_calls_extract_range_with_correct_args(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_piece", mock.Mock(side_effect=[
        ("first_piece", None, "has_step", "is_range"),
        ("second_piece", None, "has_step", "is_range"),
    ]))
    monkeypatch.setattr(cronus.parser, "extract_ranges", mock.Mock(return_value=[(1, 10)]))
    parse_section("1,2", 1, 10, "one_index")

    assert cronus.parser.extract_ranges.call_args_list == [
        mock.call("first_piece", "has_step", "is_range", "one_index", 1, 10),
        mock.call("second_piece", "has_step", "is_range", "one_index", 1, 10),
    ]


def test_parse_section_steps_through_range(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_piece", mock.Mock(side_effect=[
        ("*", 2, True, False),
    ]))
    monkeypatch.setattr(cronus.parser, "extract_ranges", mock.Mock(return_value=[(0, 10)]))
    assert parse_section("*/2", 0, 10, False) == {0, 2, 4, 6, 8, 10}


def test_parse_section_range(monkeypatch):
    monkeypatch.setattr(cronus.parser, "parse_piece", mock.Mock(side_effect=[
        ("*", None, False, False),
    ]))
    monkeypatch.setattr(cronus.parser, "extract_ranges", mock.Mock(return_value=[(0, 10)]))
    assert parse_section("*", 0, 10, False) == {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}


def test_parse_section():
    assert parse_section("1,15-17,*/10", 0, 30, True) == {1, 11, 15, 16, 17, 21, 31}
