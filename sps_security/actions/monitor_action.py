from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from sps_security.actions.cloud_action import run_cloud

IGNORED = [
    "logs",
    "quarantine",
    "__pycache__",
    ".git"
]


class MonitorHandler(FileSystemEventHandler):

    def should_ignore(self, path):
        for ignore in IGNORED:
            if ignore in path:
                return True
        return False

    def on_created(self, event):
        if event.is_directory:
            return

        if self.should_ignore(event.src_path):
            return

        print(f"File created: {event.src_path}")
        run_cloud(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        if self.should_ignore(event.src_path):
            return

        print(f"File modified: {event.src_path}")
        run_cloud(event.src_path)


def run_monitor(path="."):
    event_handler = MonitorHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    print(f"Monitoring started: {path}")
    print("Press CTRL+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped")

    observer.join()
