import hashlib
import os
import random
import shutil
from pathlib import Path

from .cache import get_cache_dir, load_venv_list, save_venv_list
from .venv import get_large_package_files

BUFFER_SIZE = 1024 * 1024 * 10  # 10MB chunks


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

    output_path = Path(dest_dir) / sha1

    os.rename(dest_file, output_path)

    return output_path


def replace_with_symlink(source, dest):
    source = Path(source).absolute()
    dest = Path(dest).absolute()
    symlink_path = source.with_suffix(".ienv.lnk")

    # Step 1: Create symlink
    symlink_path.symlink_to(dest)

    # Step 2: Copy attributes
    stat_info = source.stat()
    os.utime(symlink_path, (stat_info.st_atime, stat_info.st_mtime))

    # Linux: preserve permission bits
    if os.name != "nt":
        shutil.copymode(source, symlink_path)

    # Step 3: Move the symlink over the source file
    os.replace(symlink_path, source)


def process_venv(venv_dir):
    venv_dir = Path(venv_dir).resolve()  # Making sure it's an absolute path

    # Ensure cache directory exists and load venv list
    cache_dir = get_cache_dir()
    venv_list = load_venv_list(cache_dir / "venvs.txt")

    # Add the venv to the list and save it
    venv_list.add(str(venv_dir))
    save_venv_list(cache_dir / "venvs.txt", venv_list)

    # Process each package file in the venv
    for file_path in get_large_package_files(venv_dir):
        print("...", file_path)
        if not file_path.is_symlink() and not file_path.is_dir():
            backup_path = backup_file(file_path, cache_dir)
            replace_with_symlink(file_path, backup_path)