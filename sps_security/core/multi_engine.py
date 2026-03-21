"""
core/multi_engine.py
Executa todos os engines em paralelo e calcula o risco final.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ..engines import ALL_ENGINES


class MultiEngine:

    def __init__(self, max_workers=5):
        self.engines = [engine() for engine in ALL_ENGINES]
        self.max_workers = max_workers

    def analyze_file(self, filepath):

        filepath = Path(filepath)
        start = time.time()

        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(e.analyze, filepath) for e in self.engines]

            for future in futures:
                try:
                    results.append(future.result())
                except Exception:
                    pass

        score = sum(r.score for r in results)

        if score == 0:
            risk = "SAFE"
        elif score <= 3:
            risk = "LOW"
        elif score <= 7:
            risk = "MEDIUM"
        elif score <= 14:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        return {
            "file": str(filepath),
            "risk": risk,
            "score": score,
            "results": results,
            "time": round(time.time() - start, 2),
        }
