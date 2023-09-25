import pytest

from ienv.main import parse_args


def test_parse_args_stats():
    args = parse_args(["--stats"])
    assert args.stats
    assert args.venv_dir is None


def test_parse_args_venv_dir():
    args = parse_args(["my_venv"])
    assert not args.stats
    assert args.venv_dir == "my_venv"


def test_parse_args_both_fail():
    with pytest.raises(SystemExit):
        parse_args(["--stats", "my_venv"])


def test_parse_args_none_fail():
    with pytest.raises(SystemExit):
        parse_args([])
