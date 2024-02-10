from pathlib import Path

from ienv.venv import get_package_files


def test_get_site_package_files(tmpdir):
    fake_venv = Path(tmpdir) / "lib/python3.8/site-packages"
    fake_venv.mkdir(parents=True)
    (fake_venv / "file1.txt").touch()
    (fake_venv / "file2.txt").touch()
    files = list(get_package_files(tmpdir))

    assert len(files) == 2
