"""
Deals with virtual environments.
"""

import argparse
import glob
import os
from pathlib import Path

MIN_FILE_SIZE = 4096  # 4k, size of a single block on most filesystems


def venv_dir(directory):
    """
    Validates a "venv_dir" and acts as a custom type. Not really needed but I like
    this sort of thing.
    """
    if not os.path.exists(directory):
        raise argparse.ArgumentTypeError(f"Directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(f"Path '{directory}' is not a directory.")

    site_packages_glob = Path(directory).joinpath("lib/*/site-packages/")
    if len(glob.glob(str(site_packages_glob))) == 0:
        raise argparse.ArgumentTypeError(f"Directory '{directory}' is not a venv.")

    return directory


def get_package_files(venv_dir):
    """
    Return all the files under site-packages in the given venv.
    """
    lib_dir = Path(venv_dir) / "lib"
    for python_dir in glob.glob(f"{lib_dir}/python*"):
        site_packages_dir = Path(python_dir) / "site-packages"
        if site_packages_dir.exists() and site_packages_dir.is_dir():
            for root, _, files in os.walk(site_packages_dir):
                for file in files:
                    yield Path(root) / file


def get_large_package_files(venv_dir):
    """
    Return all the files in a venv that are larger than MIN_FILE_SIZE.
    """
    for file_path in get_package_files(venv_dir):
        if file_path.stat().st_size >= MIN_FILE_SIZE:
            yield file_path
