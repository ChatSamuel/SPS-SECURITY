class ScanResult:
    def __init__(self, results):
        self.results = results

    def to_dict(self):
        total_detections = sum(r["raw_detections"] for r in self.results)
        total_engines = len(self.results)

        score = sum(
            r["confidence"] * r["weight"] for r in self.results
        ) / sum(r["weight"] for r in self.results if r["weight"] > 0)

        if total_detections == 0:
            risk = "SAFE"
        elif total_detections < 3:
            risk = "LOW"
        elif total_detections < 10:
            risk = "MEDIUM"
        elif total_detections < 30:
            risk = "HIGH"
        else:
            risk = "CRITICAL"

        return {
            "risk": risk,
            "detections": f"{total_detections}/{total_engines}",
            "confidence": score,
            "engine_results": self.results,
        }


class APIManager:
    def __init__(self, engines):
        self.engines = engines

    def scan(self, file_hash: str, file_path: str = None):
        results = []

        for engine in self.engines:
            try:
                result = engine.scan(file_hash, file_path)
                if result:
                    results.append(result)
            except Exception:
                continue

        return ScanResult(results)
