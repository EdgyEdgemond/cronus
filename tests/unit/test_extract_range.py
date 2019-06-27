import pytest

from cronus.parser import extract_range


@pytest.mark.parametrize("piece,has_step,is_range,one_index,min_range,max_range,expected", [
    ("1-9", False, True, False, 0, 10, (1, 9)),
    ("1-9", False, True, True, 0, 10, (0, 8)),
    ("*", False, False, False, 0, 10, (0, 10)),
    ("1", False, False, False, 0, 10, (1, 1)),
    ("1", True, False, False, 0, 10, (1, 10)),
    ("1", False, False, True, 1, 10, (0, 0)),
    ("1", True, False, True, 1, 10, (0, 9)),
])
def test_extract_range(
    piece, has_step, is_range, one_index, min_range, max_range, expected,
):
    assert extract_range(piece, has_step, is_range, one_index, min_range, max_range) == expected


def test_extract_range_returns_zero_index_for_one_index_ranges():
    start, stop = extract_range("1-12", False, True, True, 0, 11)
    assert start == 0
    assert stop == 11


def test_extract_range_uses_min_max_for_asterisk():
    start, stop = extract_range("*", False, False, False, 0, 11)
    assert start == 0
    assert stop == 11
