"""
multi_scan.py
Sistema multi-antivírus paralelo + cache inteligente
"""

import requests
import hashlib
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from sps_security.config import Config

# 🔥 CACHE
import json
from pathlib import Path as P

CACHE_FILE = P.home() / ".sps_cloud_cache.json"


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


class MultiAPI:

    def __init__(self):
        self.vt_key = Config.VIRUSTOTAL_API_KEY

    # ==============================
    # 🔹 VIRUSTOTAL
    # ==============================
    def scan_virustotal(self, filepath):

        url = "https://www.virustotal.com/api/v3/files"
        headers = {"x-apikey": self.vt_key}

        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        r = requests.get(f"{url}/{file_hash}", headers=headers)

        if r.status_code != 200:
            with open(filepath, "rb") as f:
                requests.post(url, headers=headers, files={"file": f})

            time.sleep(15)
            r = requests.get(f"{url}/{file_hash}", headers=headers)

        data = r.json()
        stats = data["data"]["attributes"]["last_analysis_stats"]

        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        total = sum(stats.values())

        return {
            "engine": "VirusTotal",
            "detections": malicious + suspicious,
            "total": total
        }

    # ==============================
    # 🔹 MOCK (placeholder p/ mais APIs)
    # ==============================
    def scan_mock(self, filepath):
        return {
            "engine": "MockEngine",
            "detections": 0,
            "total": 1
        }

    # ==============================
    # 🔥 SCAN PRINCIPAL
    # ==============================
    def scan(self, filepath):

        filepath = Path(filepath)

        if not filepath.exists():
            return {
                "risk": "ERROR",
                "detections": 0,
                "engines": 0
            }

        # 🔥 HASH DO ARQUIVO
        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # 🔥 CACHE CHECK
        cached = get_cached(file_hash)
        if cached:
            print("[CACHE] Resultado instantâneo ⚡")
            return cached

        # 🔥 ENGINES
        engines = [
            self.scan_virustotal,
            self.scan_mock,
        ]

        results = []

        # 🚀 EXECUÇÃO PARALELA
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(e, filepath) for e in engines]

            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception:
                    pass

        total_detections = sum(r["detections"] for r in results)
        total_engines = sum(r["total"] for r in results)

        # 🎯 CLASSIFICAÇÃO FINAL
        if total_detections == 0:
            risk = "SAFE"
        elif total_detections < 5:
            risk = "LOW"
        elif total_detections < 20:
            risk = "MEDIUM"
        elif total_detections < 50:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        result = {
            "risk": risk,
            "detections": total_detections,
            "engines": total_engines
        }

        # 🔥 SALVA CACHE
        set_cache(file_hash, result)

        return result
