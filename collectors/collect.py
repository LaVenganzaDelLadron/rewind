# collect.py

import time
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from database import Database

from collectors.packages import PackageCollector
from collectors.services import ServiceCollector
from collectors.performance import PerformanceCollector
from collectors.shell import ShellCollector
from collectors.files import FileCollector

def start(stop_event=None):
    db = Database()

    packages = PackageCollector()
    services = ServiceCollector()
    performance = PerformanceCollector()
    shell = ShellCollector()

    # Start file monitoring (queue-based) in parallel with other collectors.
    # Watching / can be noisy; change watch_root if needed.
    file_collector = FileCollector(watch_path="/", recursive=True)
    file_collector.start()


    print("Rewind monitor started.")

    while True:
        if stop_event is not None and stop_event.is_set():
            break

        all_events = []

        all_events.extend(packages.read_new_events())
        all_events.extend(services.check_changes())
        all_events.extend(performance.check())
        all_events.extend(shell.read_new_commands())
        all_events.extend(file_collector.read_new_events())

        db.add_events(all_events)

        time.sleep(10)

    file_collector.stop()
    db.close()
