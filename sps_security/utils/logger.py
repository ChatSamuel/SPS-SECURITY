"""
utils/logger.py
O diário do antivírus. Tudo que acontece é anotado
com data, hora e resultado. Você pode revisar depois.
"""

import logging
import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path.home() / ".sps_security" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "sps"):
    logger = logging.getLogger(name)

    # Evita duplicar handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    log_file = LOG_DIR / f"sps_{datetime.now().strftime('%Y%m%d')}.log"

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    logger.addHandler(fh)
    return logger


def log_scan_result(result: dict) -> None:
    """Salva resultado de scan em JSON (histórico completo)."""
    json_log = LOG_DIR / "scan_history.jsonl"

    with open(json_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, default=str) + "\n")
