import logging
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "scan.log")

if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message):
    logging.info(message)
