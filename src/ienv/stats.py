"""
Stats will go here eventually
"""

from ienv.cache import CACHE_FILE, get_cache_dir, load_venv_list


def print_stats():
    """
    Doesn't do much yet really.
    """
    cache_dir = get_cache_dir()
    venvs = load_venv_list(cache_dir / CACHE_FILE)
    print(f"I've mangled {len(venvs)} venvs!")
    for venv in venvs:
        print("   ", venv)
