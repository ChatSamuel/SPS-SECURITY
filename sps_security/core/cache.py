import json
import time
from pathlib import Path


class ScanCache:

    def __init__(self, cache_path=".sps_cache.json", ttl_seconds=86400):
        self.path = Path(cache_path)
        self.ttl = ttl_seconds

    def _load(self):
        if not self.path.exists():
            return {}
        return json.loads(self.path.read_text())

    def _save(self, data):
        self.path.write_text(json.dumps(data))

    def get(self, key):
        data = self._load()
        entry = data.get(key)

        if not entry:
            return None

        if time.time() - entry["time"] > self.ttl:
            return None

        return entry["value"]

    def set(self, key, value):
        data = self._load()
        data[key] = {
            "time": time.time(),
            "value": value
        }
        self._save(data)
