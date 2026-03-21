import os

DB_FILE = "sps_security/db/signatures.txt"


def load_signatures():
    if not os.path.exists(DB_FILE):
        return []

    with open(DB_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]
