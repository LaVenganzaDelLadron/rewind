#!/usr/bin/env python3

import sys

from commands import today
from commands import yesterday
from commands import search
from commands import stats


def show_help():
    print("""
Rewind - Linux Time Machine

Usage:
    rewind today
    rewind yesterday
    rewind search <keyword>
    rewind stats
    rewind help
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "today":
        today.run()

    elif command == "yesterday":
        yesterday.run()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Error: missing search keyword.")
            return

        keyword = " ".join(sys.argv[2:])
        search.run(keyword)

    elif command == "stats":
        stats.run()

    elif command == "help":
        show_help()

    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == "__main__":
    main()