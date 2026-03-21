"""
realtime/watcher.py
Monitora arquivos em tempo real.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pathlib import Path
from ..core.multi_engine import MultiEngine


class Handler(FileSystemEventHandler):

    def __init__(self):
        self.engine = MultiEngine()

    def on_created(self, event):
        if not event.is_directory:
            self.scan(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.scan(event.src_path)

    def scan(self, filepath):
        result = self.engine.analyze_file(filepath)

        if result["risk"] in ("HIGH", "CRITICAL"):
            print(f"[REALTIME THREAT] {filepath} -> {result['risk']}")


class RealTimeScanner:

    def __init__(self, path="."):
        self.path = Path(path)
        self.observer = Observer()

    def start(self):

        handler = Handler()
        self.observer.schedule(handler, str(self.path), recursive=True)
        self.observer.start()

        print(f"\n[REALTIME] Monitoring: {self.path}\n")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
