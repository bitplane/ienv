"""
The cache dir, which lives at ~/.cache/ienv

It's where all your files have been moved to.
"""
import os
from pathlib import Path

CACHE_FILE = "venvs.txt"


def get_cache_dir(prefix="~"):
    """
    Return the cache dir, creating it if it doesn't exist.
    """
    cache_dir = Path(f"{prefix}/.cache/ienv/files").expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)

    return cache_dir


def load_venv_list(file_path):
    """
    Load the list of venvs that have been squished.
    """
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r") as f:
        return set(line.strip() for line in f)


def save_venv_list(file_path, venvs):
    """
    Save the list of venvs that have been squished.
    """
    with open(file_path, "w") as f:
        for venv in venvs:
            f.write(f"{venv}\n")
