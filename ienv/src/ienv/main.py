"""
Entrypoint to the module.
"""

import argparse
import sys

from ienv.squish import process_venv
from ienv.stats import print_stats
from ienv.venv import venv_dir


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="ienv - shrink your venvs down by symlinking site-packages into\n"
        "a single directory. Might get you out of a low disk space situation,\n"
        "but it's utterly reckless and not at all recommended."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stats", action="store_true", help="Display cache stats.")
    group.add_argument("venv_dir", nargs="?", type=venv_dir, help="Squish this dir.")

    return parser.parse_args(args)


def main():
    args = parse_args()

    if args.stats:
        print_stats()
    else:
        process_venv(args.venv_dir)


if __name__ == "__main__":
    main()
