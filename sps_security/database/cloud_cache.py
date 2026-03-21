import json
from pathlib import Path

CACHE_FILE = Path.home() / ".sps_cloud_cache.json"


def load_cache():
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text())
    except:
        return {}


def save_cache(data):
    CACHE_FILE.write_text(json.dumps(data))


def get_cached(hash_value):
    cache = load_cache()
    return cache.get(hash_value)


def set_cache(hash_value, result):
    cache = load_cache()
    cache[hash_value] = result
    save_cache(cache)
