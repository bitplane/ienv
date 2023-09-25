import hashlib
import tempfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from ienv.ienv import backup_file, hash_and_copy


def test_hash_and_copy_only_hash():
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"This is a test.")
        tmp_path = tmp.name

    sha1 = hashlib.sha1()
    with open(tmp_path, "rb") as f:
        while chunk := f.read(1024):
            sha1.update(chunk)

    assert hash_and_copy(tmp_path) == sha1.hexdigest()


def test_hash_and_copy_with_dest():
    with NamedTemporaryFile(delete=False) as src_tmp, NamedTemporaryFile(
        delete=False
    ) as dest_tmp:
        src_tmp.write(b"This is another test.")
        src_path, dest_path = src_tmp.name, dest_tmp.name

    assert hash_and_copy(src_path, dest_path) == hash_and_copy(src_path)

    with open(dest_path, "rb") as f:
        assert f.read() == b"This is another test."


def test_backup_file():
    with tempfile.TemporaryDirectory() as tempdir:
        source = Path(tempdir) / "source.txt"
        dest_dir = Path(tempdir) / "backup"
        dest_dir.mkdir()

        with open(source, "w") as f:
            f.write("Hello, world!")

        original_sha1 = hash_and_copy(str(source), None)

        backup_file(str(source), str(dest_dir))

        # Verify renaming happened
        renamed_file = dest_dir / original_sha1
        assert renamed_file.exists()

        # Verify content is identical
        with open(renamed_file, "r") as f:
            assert f.read() == "Hello, world!"
