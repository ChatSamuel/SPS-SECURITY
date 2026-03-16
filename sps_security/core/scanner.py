import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

from sps_security.core.hash_engine import hash_scan
from sps_security.core.signature_engine import signature_scan
from sps_security.core.heuristic_engine import heuristic_scan
from sps_security.core.binary_engine import binary_scan
from sps_security.utils.quarantine import quarantine

# extensões ignoradas
IGNORE_EXT = (".py", ".pyc")

# pastas ignoradas
IGNORE_DIRS = ["quarantine", "__pycache__", "database"]


def scan_file(file, signatures, hashes, patterns):

    # ignorar arquivos de código
    if file.endswith(IGNORE_EXT):
        return False

    # hash detection
    if hash_scan(file, hashes):
        quarantine(file)
        return True

    # signature detection
    if signature_scan(file, signatures):
        quarantine(file)
        return True

    # heuristic detection
    if heuristic_scan(file):
        return True

    # binary scan
    if file.endswith((".exe", ".dll", ".apk", ".bin")):
        if binary_scan(file, patterns):
            return True

    return False


def scan_folder(folder, signatures, hashes, patterns):

    files = []

    for root, dirs, names in os.walk(folder):

        # remover pastas ignoradas
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
