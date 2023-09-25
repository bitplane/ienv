import hashlib
import os
import random
from pathlib import Path

BUFFER_SIZE = 1024 * 1024 * 10  # 10MB chunks


def get_cache_dir(prefix="~"):
    cache_dir = Path(f"{prefix}/.cache/ienv/files").expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def load_venv_list(file_path):
    with open(file_path, "r") as f:
        return set(line.strip() for line in f)


def save_venv_list(file_path, venvs):
    with open(file_path, "w") as f:
        for venv in venvs:
            f.write(f"{venv}\n")


def get_package_files(venv_dir):
    site_packages_dir = Path(venv_dir) / "lib/python3.8/site-packages"
    for root, _, files in os.walk(site_packages_dir):
        for file in files:
            yield Path(root) / file


def hash_and_copy(source, dest=None):
    sha1 = hashlib.sha1()
    with open(source, "rb") as src_file:
        if dest:
            dest_file = open(dest, "wb")  # let the gc deal with this
        while chunk := src_file.read(BUFFER_SIZE):
            sha1.update(chunk)
            if dest:
                dest_file.write(chunk)

    return sha1.hexdigest()


def backup_file(source, dest_dir):
    dest_file = Path(dest_dir) / hex(random.getrandbits(128))
    linked = False
    try:
        # Attempt to hardlink. this might fail
        os.link(source, dest_file)
        # if we did manage to hardlink so no need to copy
        linked = True
    except OSError:
        # we have to copy the file
        pass

    sha1 = hash_and_copy(source, dest_file if not linked else None)

    os.rename(dest_file, f"{Path(dest_dir) / sha1}")
