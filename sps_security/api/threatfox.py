import requests
from .base_api import BaseAPI


class ThreatFoxAPI(BaseAPI):

    name = "ThreatFox"
    weight = 0.60

    def scan(self, file_hash: str, file_path: str):

        url = "https://threatfox-api.abuse.ch/api/v1/"

        payload = {
            "query": "search_hash",
            "hash": file_hash
        }

        try:
            r = requests.post(url, json=payload)
            res = r.json()

            detected = res.get("query_status") == "ok"

            return {
                "engine_name": self.name,
                "detected": detected,
                "raw_detections": 1 if detected else 0,
                "total_scanners": 1,
                "confidence": 1.0 if detected else 0.0,
                "weight": self.weight,
                "malware_family": None
            }

        except:
            return {
                "engine_name": self.name,
                "detected": False,
                "raw_detections": 0,
                "total_scanners": 1,
                "confidence": 0.0,
                "weight": self.weight,
                "malware_family": None
            }
