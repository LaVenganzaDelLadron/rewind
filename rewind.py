#!/usr/bin/env python3

import sys

from commands.today import show_today
from utils.helper import show_help


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()
    if command in {"today", "t"}:
        show_today()
        return

    show_help()


if __name__ == "__main__":
    main()