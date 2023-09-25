import hashlib
from tempfile import NamedTemporaryFile

from ienv.ienv import hash_and_copy


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
