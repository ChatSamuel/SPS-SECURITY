import os
from sps_security.api import APIManager, VirusTotalAPI, MalwareBazaarAPI, ThreatFoxAPI
from sps_security.core.hasher import compute_fingerprint
from sps_security.core.cache import ScanCache

# DESATIVANDO CACHE TEMPORARIAMENTE
_cache = None


def cloud_scan(file_path: str) -> dict:

    fingerprint = compute_fingerprint(file_path)
    sha256 = fingerprint.sha256

    engines = [
        VirusTotalAPI(api_key=os.environ.get("VT_API_KEY", "")),
        MalwareBazaarAPI(),
        ThreatFoxAPI(),
    ]

    manager = APIManager(engines=engines)

    result = manager.scan(file_hash=sha256, file_path=file_path)

    return result
