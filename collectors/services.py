# collectors/services.py

import subprocess


class ServiceCollector:
    def __init__(self):
        self.previous_states = {}

    def get_services(self):
        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--no-pager",
                "--no-legend"
            ],
            capture_output=True,
            text=True
        )

        services = {}

        for line in result.stdout.splitlines():
            parts = line.split()

            if len(parts) >= 4:
                name = parts[0]
                active = parts[2]

                services[name] = active

        return services

    def check_changes(self):
        events = []

        current = self.get_services()

        for service, state in current.items():
            old_state = self.previous_states.get(service)

            if old_state is None:
                self.previous_states[service] = state
                continue

            if old_state != state:
                events.append({
                    "category": "service",
                    "title": f"{service} changed: {old_state} → {state}"
                })

                self.previous_states[service] = state

        return events