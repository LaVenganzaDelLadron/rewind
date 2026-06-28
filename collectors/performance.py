# collectors/performance.py

import psutil
import time


class PerformanceCollector:
    def __init__(self):
        self.cpu_limit = 90
        self.memory_limit = 90
        self.disk_limit = 90

        # Prevent alert spam when the system stays above threshold.
        self.cooldown_seconds = 300  # 5 minutes
        self._last_alert_ts = {}

        # Warm up cpu_percent so subsequent calls don't block.
        try:
            psutil.cpu_percent(interval=None)
        except Exception:
            pass

    def _emit(self, key, title, now, events):
        last = self._last_alert_ts.get(key)
        if last is None or (now - last) >= self.cooldown_seconds:
            self._last_alert_ts[key] = now
            events.append({
                "category": "performance",
                "title": title,
            })

    def check(self):
        events = []
        now = time.time()

        # Non-blocking sample after warmup.
        cpu = psutil.cpu_percent(interval=None)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        if cpu >= self.cpu_limit:
            self._emit("cpu", f"CPU usage reached {cpu}%", now, events)

        if memory >= self.memory_limit:
            self._emit("memory", f"Memory usage reached {memory}%", now, events)

        if disk >= self.disk_limit:
            self._emit("disk", f"Disk usage reached {disk}%", now, events)

        return events
