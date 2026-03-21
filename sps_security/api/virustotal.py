import requests


class VirusTotalAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.virustotal.com/api/v3/files"

    def scan(self, file_hash: str, file_path: str = None):
        headers = {
            "x-apikey": self.api_key
        }

        url = f"{self.base_url}/{file_hash}"

        try:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return {
                    "engine_name": "VirusTotal",
                    "detected": False,
                    "raw_detections": 0,
                    "total_scanners": 0,
                    "confidence": 0.0,
                    "weight": 0.95,
                }

            data = response.json()

            stats = data["data"]["attributes"]["last_analysis_stats"]

            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            total = sum(stats.values())

            detections = malicious + suspicious

            confidence = detections / total if total > 0 else 0

            return {
                "engine_name": "VirusTotal",
                "detected": detections > 0,
                "raw_detections": detections,
                "total_scanners": total,
                "confidence": confidence,
                "weight": 0.95,
            }

        except Exception:
            return {
                "engine_name": "VirusTotal",
                "detected": False,
                "raw_detections": 0,
                "total_scanners": 0,
                "confidence": 0.0,
                "weight": 0.95,
            }
