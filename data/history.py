from datetime import datetime, date
from pathlib import Path
import time

from structure.single_linked_list import SingleLinkedList


class History:
    def __init__(self, history_path=None):
        self.history = Path(history_path) if history_path is not None else Path.home() / ".bash_history"

        self.position = 0
        self._last_seen_ts = {}

    def current_size(self):
        try:
            return self.history.stat().st_size
        except FileNotFoundError:
            return 0

    def normalize_command(self, raw_line):
        command = raw_line.strip()
        if not command or command.startswith("#"):
            return None
        return command

    def _is_command_for_day(self, timestamp, target_day):
        try:
            return datetime.fromtimestamp(timestamp).date() == target_day
        except (OverflowError, OSError, ValueError):
            return False

    def get_commands_for_day(self, target_day=None):
        if target_day is None:
            target_day = date.today()

        commands = SingleLinkedList()
        if not self.history.exists():
            return commands.to_list()

        current_timestamp = None
        with open(self.history, "r", encoding="utf-8", errors="ignore") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue

                if line.startswith("#"):
                    try:
                        current_timestamp = int(line[1:])
                    except ValueError:
                        current_timestamp = None
                    continue

                if current_timestamp is None:
                    continue

                if not self._is_command_for_day(current_timestamp, target_day):
                    continue

                command = self.normalize_command(line)
                if command is not None:
                    commands.append(command)

        return commands.to_list()

    def read_new_commands(self):
        events = []

        if not self.history.exists():
            return events

        current_size = self.current_size()

        if current_size < self.position:
            self.position = 0

        with open(self.history, "r", encoding="utf-8", errors="ignore") as file:
            file.seek(self.position)

            for line in file:
                command = self.normalize_command(line)
                if command is None:
                    continue
                events.append(command)

            self.position = file.tell()

        return events



