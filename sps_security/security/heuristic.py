import os
from sps_security.security.database import load_signatures

EICAR_SIGNATURE = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!"


def heuristic_scan(file_path):
    try:
        if not os.path.exists(file_path):
            return None

        with open(file_path, "r", errors="ignore") as f:
            content = f.read().lower()

        # 1. Detect EICAR
        if EICAR_SIGNATURE.lower() in content:
            return {
                "risk": "CRITICAL",
                "detections": 1,
                "engine": "LOCAL_HEURISTIC"
            }

        # 2. Database signatures
        signatures = load_signatures()
        for sig in signatures:
            if sig.lower() in content:
                return {
                    "risk": "CRITICAL",
                    "detections": 1,
                    "engine": "LOCAL_DATABASE"
                }

        # 3. Suspicious patterns
        suspicious = [
            "eval(",
            "exec(",
            "base64.b64decode",
            "subprocess",
            "os.system",
            "socket",
            "chmod 777",
            "wget ",
            "curl ",
            "powershell",
            "cmd.exe",
            "bash -i"
        ]

        for pattern in suspicious:
            if pattern in content:
                return {
                    "risk": "HIGH",
                    "detections": 1,
                    "engine": "LOCAL_HEURISTIC"
                }

        return None

    except Exception:
        return None
