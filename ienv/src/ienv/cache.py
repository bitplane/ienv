import os
from pathlib import Path


def get_cache_dir(prefix="~"):
    cache_dir = Path(f"{prefix}/.cache/ienv/files").expanduser()
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def load_venv_list(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r") as f:
        return set(line.strip() for line in f)


def save_venv_list(file_path, venvs):
    with open(file_path, "w") as f:
        for venv in venvs:
            f.write(f"{venv}\n")
