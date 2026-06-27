# collectors/packages.py
import os
import re

PACMAN_LOG = "/var/log/pacman.log"


class PackageCollector:
    def __init__(self):
        self.last_position = 0

    def read_new_events(self):
        events = []

        if not os.path.exists(PACMAN_LOG):
            return events

        with open(PACMAN_LOG, "r") as file:
            file.seek(self.last_position)

            for line in file:
                line = line.strip()

                installed = re.search(
                    r"\[(.*?)\].*installed (.*?) \(",
                    line
                )

                removed = re.search(
                    r"\[(.*?)\].*removed (.*?) \(",
                    line
                )

                upgraded = re.search(
                    r"\[(.*?)\].*upgraded (.*?) \(",
                    line
                )

                if installed:
                    events.append({
                        "timestamp": installed.group(1),
                        "category": "package",
                        "title": f"Installed {installed.group(2)}"
                    })

                elif removed:
                    events.append({
                        "timestamp": removed.group(1),
                        "category": "package",
                        "title": f"Removed {removed.group(2)}"
                    })

                elif upgraded:
                    events.append({
                        "timestamp": upgraded.group(1),
                        "category": "package",
                        "title": f"Upgraded {upgraded.group(2)}"
                    })

            self.last_position = file.tell()

        return events