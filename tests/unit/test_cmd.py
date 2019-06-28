import io
from unittest import mock

import pytest

import cronus.parser
from cronus.cmd import main


def test_main_no_args():
    mock_stderr = io.StringIO()

    with mock.patch("sys.stderr", mock_stderr):
        with mock.patch("sys.argv", ["cronparse"]):
            with pytest.raises(SystemExit):
                main()

    assert mock_stderr.getvalue().split("\n")[:-1] == [
        "usage: pytest [-h] crontab command",
        "pytest: error: the following arguments are required: crontab, command",
    ]


def test_main_uses_parser(monkeypatch):
    monkeypatch.setattr(cronus.parser.CronParser, "__init__", mock.Mock(return_value=None))
    monkeypatch.setattr(cronus.parser.CronParser, "parse", mock.Mock())
    monkeypatch.setattr(cronus.parser.CronParser, "render", mock.Mock())

    with mock.patch("sys.argv", ["cronparse", "crontab", "command"]):
        main()

    assert cronus.parser.CronParser.__init__.call_args == mock.call("crontab", "command")


def test_main():
    mock_stdout = io.StringIO()

    with mock.patch("sys.argv", ["cronparse", "*/15 0 1,15 * 1-5", "/usr/bin/find"]):
        with mock.patch("sys.stdout", mock_stdout):
            main()

    assert mock_stdout.getvalue().split("\n")[:-1] == [
        "minute          0 15 30 45",
        "hour            0",
        "day of month    1 15",
        "month           1 2 3 4 5 6 7 8 9 10 11 12",
        "day of week     1 2 3 4 5",
        "command         /usr/bin/find",
    ]
