import argparse
import sys


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="ienv - shrink your venvs down by symlinking site-packages."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--stats", action="store_true", help="Display cache stats.")
    group.add_argument("venv_dir", nargs="?", help="Squish this dir.")

    return parser.parse_args(args)


def main():
    args = parse_args()
    print(args)


if __name__ == "__main__":
    args = parse_args()
    print(args)
