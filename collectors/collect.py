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

def start():
    db = Database()

    packages = PackageCollector()
    services = ServiceCollector()
    performance = PerformanceCollector()
    shell = ShellCollector()

    print("Rewind monitor started.")

    while True:
        for event in packages.read_new_events():
            db.add_event(
                event["category"],
                event["title"]
            )

        for event in services.check_changes():
            db.add_event(
                event["category"],
                event["title"]
            )

        for event in performance.check():
            db.add_event(
                event["category"],
                event["title"]
            )

        for event in shell.read_new_commands():
            db.add_event(
                event["category"],
                event["title"]
            )

        time.sleep(10)