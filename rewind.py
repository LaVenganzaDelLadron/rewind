#!/usr/bin/env python3

import sys
import threading
import signal

from commands import today
from commands import yesterday
from commands import search
from commands import stats
from collectors import collect



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
    stop_event = threading.Event()

    def start_collector():
        collect.start(stop_event=stop_event)

    collector_thread = threading.Thread(target=start_collector, daemon=True)

    def _handle_signal(signum, frame):
        stop_event.set()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    collector_thread.start()

    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "monitor":
        collect.start()

    elif command == "today":
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