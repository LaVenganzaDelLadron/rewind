# collect.py

import time
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import json
from pathlib import Path

from database import Database

from collectors.packages import PackageCollector
from collectors.services import ServiceCollector
from collectors.performance import PerformanceCollector
from collectors.shell import ShellCollector
from collectors.files import FileCollector


def _load_state(state_path=None):
    if state_path is None:
        state_path = Path.home() / ".rewind-state.json"
    else:
        state_path = Path(state_path)

    if not state_path.exists():
        return {}

    try:
        with state_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state_path, state):
    if state_path is None:
        return

    state_path = Path(state_path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle)


def collect_once(db=None, state_path=None):
    if db is None:
        db = Database()
        should_close = True
    else:
        should_close = False

    state = _load_state(state_path)
    package_state = state.get("package", {})
    shell_state = state.get("shell", {})

    try:
        packages = PackageCollector()
        services = ServiceCollector()
        performance = PerformanceCollector()
        shell = ShellCollector()

        if package_state:
            packages.last_position = package_state.get("last_position", 0)

        if shell_state:
            shell.position = shell_state.get("position", 0)
            shell._last_seen_ts = shell_state.get("last_seen_ts", {})

        all_events = []
        all_events.extend(packages.read_new_events())
        all_events.extend(services.check_changes())
        all_events.extend(performance.check())
        all_events.extend(shell.read_new_commands())

        if all_events:
            db.add_events(all_events)

        state["package"] = {"last_position": packages.last_position}
        state["shell"] = {
            "position": shell.position,
            "last_seen_ts": shell._last_seen_ts,
        }
        _save_state(state_path, state)
    finally:
        if should_close:
            db.close()


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

    collect_once(db)

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
