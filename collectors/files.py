import os
import time
import threading
from pathlib import Path
from queue import Queue, Empty

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileCollector(FileSystemEventHandler):
    """Queue-based file change collector.

    Produces events into an internal Queue so the main loop can batch them.
    """

    def __init__(
        self,
        watch_path: str | Path = "/",
        recursive: bool = True,
        throttle_seconds: float = 2.0,
    ):
        super().__init__()
        self.watch_path = Path(watch_path)
        self.recursive = recursive

        self._queue: Queue = Queue()

        # Debounce by (event_type, src_path) and only emit once per throttle window.
        self.throttle_seconds = throttle_seconds
        self._last_emitted = {}

        self._observer: Observer | None = None

    def start(self):
        if self._observer is not None:
            return

        observer = Observer()
        observer.schedule(self, str(self.watch_path), recursive=self.recursive)
        observer.start()
        self._observer = observer

    def stop(self):
        if self._observer is None:
            return
        self._observer.stop()
        self._observer.join(timeout=5)
        self._observer = None

    def _enqueue(self, event_type: str, src_path: str):
        now = time.time()
        key = (event_type, src_path)
        last = self._last_emitted.get(key)
        if last is not None and (now - last) < self.throttle_seconds:
            return

        self._last_emitted[key] = now
        title = f"{event_type}: {src_path}"

        # Keep it consistent with other collectors.
        self._queue.put({
            "category": "file",
            "title": title,
        })

    def on_modified(self, event):
        if event.is_directory:
            return
        self._enqueue("Modified", event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self._enqueue("Created", event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self._enqueue("Deleted", event.src_path)

    def read_new_events(self, max_events: int = 500):
        events = []
        for _ in range(max_events):
            try:
                events.append(self._queue.get_nowait())
            except Empty:
                break
        return events


# Backwards-compatible function kept for older imports.
# This project primarily uses FileCollector.

def monitor(path: str | Path):
    collector = FileCollector(watch_path=path)
    collector.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        collector.stop()

