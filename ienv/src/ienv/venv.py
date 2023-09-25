import glob
import os
from pathlib import Path

MIN_FILE_SIZE = 4096  # 4k, size of a single block on most filesystems


def get_package_files(venv_dir):
    lib_dir = Path(venv_dir) / "lib"
    for python_dir in glob.glob(f"{lib_dir}/python*"):
        site_packages_dir = Path(python_dir) / "site-packages"
        if site_packages_dir.exists() and site_packages_dir.is_dir():
            for root, _, files in os.walk(site_packages_dir):
                for file in files:
                    yield Path(root) / file


def get_large_package_files(venv_dir):
    for file_path in get_package_files(venv_dir):
        if file_path.stat().st_size >= MIN_FILE_SIZE:
            yield file_path
