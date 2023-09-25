import argparse

import pytest

from ienv.main import venv_dir


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


def test_validate_directory_not_exists():
    with pytest.raises(argparse.ArgumentTypeError):
        venv_dir("no_way_this_exists")


def test_validate_directory_not_dir(temp_dir):
    temp_file = temp_dir / "temp_file.txt"
    temp_file.write_text("Hello, world!")
    with pytest.raises(argparse.ArgumentTypeError):
        venv_dir(str(temp_file))


def test_validate_directory_not_venv(temp_dir):
    with pytest.raises(argparse.ArgumentTypeError):
        venv_dir(str(temp_dir))


def test_validate_directory_is_venv(temp_dir):
    venv_structure = temp_dir / "lib/python3.8/site-packages"
    venv_structure.mkdir(parents=True)
    assert venv_dir(str(temp_dir)) == str(temp_dir)
