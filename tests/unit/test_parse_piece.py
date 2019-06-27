from cronus.parser import parse_piece


def test_parse_piece_detects_range():
    piece, _step, has_step, is_range = parse_piece("1-10")
    assert piece == "1-10"
    assert is_range is True


def test_parse_piece_detects_non_range():
    piece, _step, has_step, is_range = parse_piece("1")
    assert piece == "1"
    assert is_range is False


def test_parse_piece_detects_step():
    piece, step, has_step, _is_range = parse_piece("*/2")
    assert piece == "*"
    assert has_step is True
    assert step == 2


def test_parse_piece_detects_non_step():
    piece, step, has_step, _is_range = parse_piece("*")
    assert piece == "*"
    assert has_step is False
    assert step is None


def test_parse_piece_detects_stepped_range():
    piece, step, has_step, is_range = parse_piece("1-10/2")
    assert piece == "1-10"
    assert is_range is True
    assert has_step is True
    assert step == 2
