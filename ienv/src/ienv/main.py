import argparse
import glob
import os
import sys
from pathlib import Path

from ienv.ienv import process_venv


def venv_dir(directory):
    """
    Validator for argparse
    """
    if not os.path.exists(directory):
        raise argparse.ArgumentTypeError(f"Directory '{directory}' does not exist.")
    if not os.path.isdir(directory):
        raise argparse.ArgumentTypeError(f"Path '{directory}' is not a directory.")

    site_packages_glob = Path(directory).joinpath("lib/*/site-packages/")
    if len(glob.glob(str(site_packages_glob))) == 0:
        raise argparse.ArgumentTypeError(f"Directory '{directory}' is not a venv.")

    return directory


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
        raise NotImplementedError("Stats not implemented yet.")
    else:
        process_venv(args.venv_dir)


if __name__ == "__main__":
    main()
