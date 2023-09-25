import os
from pathlib import Path

from ienv.squish import replace_with_symlink


def test_replace_with_symlink_file_exists():
    src = Path("test_file.txt")
    dest = Path("dest_file.txt")

    src.write_text("Hello")
    dest.write_text("World")

    replace_with_symlink(src, dest)

    assert src.is_symlink()
    assert src.resolve() == dest.absolute()


def test_replace_with_symlink_preserve_attributes():
    src = Path("test_file.txt")
    dest = Path("dest_file.txt")

    src.write_text("Hello")
    dest.write_text("World")

    # Give it some custom time
    os.utime(src, (1629388471, 1629388472))

    replace_with_symlink(src, dest)

    assert src.is_symlink()
    assert os.path.getatime(src) == 1629388471
    assert os.path.getmtime(src) == 1629388472
