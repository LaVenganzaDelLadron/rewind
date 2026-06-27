# collectors/performance.py

import psutil


class PerformanceCollector:
    def __init__(self):
        self.cpu_limit = 90
        self.memory_limit = 90
        self.disk_limit = 90

    def check(self):
        events = []

        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        if cpu >= self.cpu_limit:
            events.append({
                "category": "performance",
                "title": f"CPU usage reached {cpu}%"
            })

        if memory >= self.memory_limit:
            events.append({
                "category": "performance",
                "title": f"Memory usage reached {memory}%"
            })

        if disk >= self.disk_limit:
            events.append({
                "category": "performance",
                "title": f"Disk usage reached {disk}%"
            })

        return events