# collectors/shell.py

from pathlib import Path


class ShellCollector:

    def __init__(self):
        self.position = 0

        self.history_file = Path.home() / ".bash_history"

    def read_new_commands(self):
        events = []

        if not self.history_file.exists():
            return events

        with open(self.history_file) as file:
            file.seek(self.position)

            for line in file:
                command = line.strip()

                if command:
                    events.append({
                        "category": "shell",
                        "title": command
                    })

            self.position = file.tell()

        return events