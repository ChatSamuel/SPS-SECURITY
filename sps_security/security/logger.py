import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "sps.log")


def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def log_detection(file_path, risk, engine="unknown"):
    ensure_log_dir()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{timestamp}] {risk} | {engine} | {file_path}\n"

    with open(LOG_FILE, "a") as f:
        f.write(log_line)
