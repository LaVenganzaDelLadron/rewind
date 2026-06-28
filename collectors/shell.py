from pathlib import Path
import time


class ShellCollector:
    def __init__(self):
        self.history_file = Path.home() / ".bash_history"

        # File offset for incremental reads.
        self.position = 0
        self._last_seen_ts = {}

        # Cooldown to reduce duplicates for the exact same command.
        self.cooldown_seconds = 60

    def _current_size(self):
        try:
            return self.history_file.stat().st_size
        except FileNotFoundError:
            return 0

    def read_new_commands(self):
        events = []

        if not self.history_file.exists():
            return events

        current_size = self._current_size()

        # Handle rotation/truncation: if file shrank, reset offset.
        if current_size < self.position:
            self.position = 0

        now = time.time()

        with open(self.history_file, "r", encoding="utf-8", errors="ignore") as file:
            file.seek(self.position)

            for line in file:
                command = line.strip()
                if not command:
                    continue

                last = self._last_seen_ts.get(command)
                if last is None or (now - last) >= self.cooldown_seconds:
                    self._last_seen_ts[command] = now
                    events.append({
                        "category": "shell",
                        "title": command,
                    })

            self.position = file.tell()

        return events

