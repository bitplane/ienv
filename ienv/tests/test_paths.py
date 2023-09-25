import argparse
import tempfile
from pathlib import Path

import pytest

from ienv.cache import get_cache_dir, load_venv_list, save_venv_list
from ienv.main import venv_dir
from ienv.venv import get_package_files


@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path


def test_get_cache_dir_creates_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_dir = get_cache_dir(prefix=temp_dir)
        assert cache_dir.exists()
        assert cache_dir.is_dir()


def test_get_cache_dir_returns_existing_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        cache_dir = get_cache_dir(prefix=temp_dir)
        assert cache_dir == get_cache_dir(prefix=temp_dir)


def test_get_cache_dir_with_custom_prefix():
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_path = f"{temp_dir}/custom_path"
        cache_dir = get_cache_dir(prefix=custom_path)
        assert str(cache_dir).startswith(custom_path)


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


def test_get_venv_list():
    with tempfile.NamedTemporaryFile(mode="w+") as temp_file:
        temp_file.write("venv1\nvenv2\n")
        temp_file.seek(0)
        venv_list = load_venv_list(temp_file.name)
        assert venv_list == {"venv1", "venv2"}


def test_save_venv_list():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        save_venv_list(temp_file.name, {"venv1", "venv2"})
        saved_list = load_venv_list(temp_file.name)
        assert saved_list == {"venv1", "venv2"}


def test_get_site_package_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        fake_venv = Path(temp_dir) / "lib/python3.8/site-packages"
        fake_venv.mkdir(parents=True)
        (fake_venv / "file1.txt").touch()
        (fake_venv / "file2.txt").touch()
        files = list(get_package_files(temp_dir))
        assert len(files) == 2
