# collectors/files.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileWatcher(FileSystemEventHandler):

    def on_modified(self, event):
        if not event.is_directory:
            print(
                f"Modified: {event.src_path}"
            )

    def on_created(self, event):
        if not event.is_directory:
            print(
                f"Created: {event.src_path}"
            )

    def on_deleted(self, event):
        if not event.is_directory:
            print(
                f"Deleted: {event.src_path}"
            )


def monitor(path):
    observer = Observer()

    observer.schedule(
        FileWatcher(),
        path,
        recursive=True
    )

    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()