from pathlib import Path

import pytest
from pytest import fixture

from ienv.main import parse_args


@fixture
def venv_fixture(tmp_path: Path):
    venv_structure = tmp_path / ".venv/lib/python3.8/site-packages/package"
    venv_structure.mkdir(parents=True)
    return str(tmp_path / ".venv")


def test_parse_args_stats():
    args = parse_args(["--stats"])
    assert args.stats
    assert args.venv_dir is None


def test_parse_args_venv_dir(venv_fixture):
    args = parse_args([venv_fixture])
    assert not args.stats
    assert args.venv_dir == venv_fixture


def test_parse_args_both_fail(venv_fixture):
    with pytest.raises(SystemExit):
        parse_args(["--stats", venv_fixture])


def test_bad_dir(venv_fixture):
    with pytest.raises(SystemExit):
        parse_args([venv_fixture + "/I don't exist"])


def test_parse_args_none_fail():
    with pytest.raises(SystemExit):
        parse_args([])
