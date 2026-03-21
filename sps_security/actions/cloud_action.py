from sps_security.cloud.cloud_scanner import cloud_scan
from sps_security.ui.display import show_result
from sps_security.security.quarantine import quarantine_file
from sps_security.security.heuristic import heuristic_scan
from sps_security.security.logger import log_detection
from sps_security.security.score import calculate_score

def run_cloud(file):

    # 1. Local heuristic
    local_result = heuristic_scan(file)

    if local_result:
        show_result({
            "risk": local_result["risk"],
            "detections": "LOCAL",
            "confidence": 1.0
        })

        log_detection(file, local_result["risk"], "LOCAL")
        quarantine_file(file)
        return

    # 2. Cloud scan
    result = cloud_scan(file)

    if hasattr(result, "to_dict"):
        result = result.to_dict()

    show_result(result)

def run_cloud(file):

    # 1. Local heuristic
    local_result = heuristic_scan(file)

    # 2. Cloud scan
    result = cloud_scan(file)

    if hasattr(result, "to_dict"):
        result = result.to_dict()

    # 3. Calculate intelligent score
    risk = calculate_score(local_result, result)
    result["risk"] = risk

    show_result(result)

    # 4. Quarantine if dangerous
    if risk in ["HIGH", "CRITICAL"]:
        quarantine_file(file)

    # 5. Logging
    log_detection(file, risk, "MULTI_ENGINE")
