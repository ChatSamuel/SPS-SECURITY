import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from sps_security.core.hash_engine import hash_scan
from sps_security.core.signature_engine import signature_scan
from sps_security.core.heuristic_engine import heuristic_scan
from sps_security.core.binary_engine import binary_scan
from sps_security.utils.quarantine import quarantine
from sps_security.utils.logger import log

# extensões ignoradas
IGNORE_EXT = (".py", ".pyc")

# pastas ignoradas
IGNORE_DIRS = ["quarantine", "__pycache__", "database"]


def scan_file(file, signatures, hashes, patterns):

    # ignorar arquivos de código
    if file.endswith(IGNORE_EXT):
        return False

    try:

        # HASH detection
        if hash_scan(file, hashes):
            log(f"HASH DETECTED: {file}")
            quarantine(file)
            return True

        # SIGNATURE detection
        if signature_scan(file, signatures):
            log(f"SIGNATURE DETECTED: {file}")
            quarantine(file)
            return True

        # HEURISTIC detection
        if heuristic_scan(file):
            log(f"HEURISTIC DETECTED: {file}")
            return True

        # BINARY detection
        if file.endswith((".exe", ".dll", ".apk", ".bin")):
            if binary_scan(file, patterns):
                log(f"BINARY DETECTED: {file}")
                return True

    except Exception as e:
        log(f"ERROR scanning {file}: {e}")

    return False


def scan_folder(folder, signatures, hashes, patterns):

    files = []

    for root, dirs, names in os.walk(folder):

        # remover diretórios ignorados
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for name in names:
            files.append(os.path.join(root, name))

    print("\n[SCAN] Starting analysis...\n")

    threats = []

    with ThreadPoolExecutor() as executor:

        results = list(
            tqdm(
                executor.map(lambda f: scan_file(f, signatures, hashes, patterns), files),
                total=len(files)
            )
        )

    for i, result in enumerate(results):

        if result:
            threats.append(files[i])

    print("\n[RESULT]")
    print("Files scanned:", len(files))
    print("Threats found:", len(threats))
