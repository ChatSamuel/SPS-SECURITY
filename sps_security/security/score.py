def calculate_score(local=None, cloud=None):
    score = 0

    # Local heuristic
    if isinstance(local, dict):
        risk = local.get("risk", "SAFE")

        if risk == "CRITICAL":
            score += 70
        elif risk == "HIGH":
            score += 40
        elif risk == "MEDIUM":
            score += 20

    # Cloud result
    if isinstance(cloud, dict):

        detections = cloud.get("detections", 0)
        confidence = cloud.get("confidence", 0)

        # fix detections
        if isinstance(detections, str):
            try:
                detections = int(detections)
            except:
                detections = 0

        # fix confidence
        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except:
                confidence = 0

        score += int(detections) * 5
        score += int(float(confidence) * 10)

    # Final classification
    if score >= 80:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 25:
        return "MEDIUM"
    else:
        return "SAFE"
