import os
import json
import hashlib
import shutil
import argparse
import requests
from tqdm import tqdm
from colorama import Fore, init
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

logo = f"""
{Fore.CYAN}
 ███████╗██████╗ ███████╗
 ██╔════╝██╔══██╗██╔════╝
 ███████╗██████╔╝███████╗
 ╚════██║██╔═══╝ ╚════██║
 ███████║██║     ███████║
 ╚══════╝╚═╝     ╚══════╝
{Fore.GREEN}
        SPS - SECURITY
    Malware Detection Tool
        by Samuel Pontes
"""

QUARANTINE_FOLDER = "quarantine"

IGNORE_FILES = [
    "sps_security.py",
    "signatures.txt",
    "malware_hash_db.txt",
    "scan_report.json",
    "README.md"
]

IGNORE_FOLDERS = [
    "quarantine",
    "__pycache__",
    ".git"
]

HEURISTIC_PATTERNS = [
    "powershell -enc",
    "cmd.exe /c",
    "nc -e",
    "wget http",
    "curl http",
    "base64 -d"
]


def load_signatures():
    try:
        with open("signatures.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []


def load_hashes():
    try:
        with open("malware_hash_db.txt") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []


signatures = load_signatures()
malware_hashes = load_hashes()


def get_hash(file):

    sha256 = hashlib.sha256()

    try:
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    except:
        return None


def quarantine(file):

    if not os.path.exists(QUARANTINE_FOLDER):
        os.mkdir(QUARANTINE_FOLDER)

    try:
        shutil.move(file, QUARANTINE_FOLDER)
        print(Fore.MAGENTA + f"[QUARANTINE] {file}")

    except:
        pass


def heuristic_scan(content):

    for pattern in HEURISTIC_PATTERNS:
        if pattern in content:
            return pattern

    return None


def scan_file(file):

    name = os.path.basename(file)

    # ignore project files
    if name in IGNORE_FILES:
        return None

    # ignore python source files
    if file.endswith((".py", ".pyc", ".pyo", ".p")):
        return None

    # ignore hidden files
    if name.startswith("."):
        return None

    try:

        if os.path.getsize(file) < 20:
            return None

        file_hash = get_hash(file)

        if file_hash in malware_hashes:

            print(Fore.RED + f"[HASH ALERT] {file}")
            quarantine(file)

            return file

        with open(file, "r", errors="ignore") as f:

            content = f.read()

            suspicious = heuristic_scan(content)

            if suspicious:

                print(Fore.YELLOW + f"[HEURISTIC ALERT] {suspicious} in {file}")
                return file

            for sig in signatures:

                if sig in content:

                    print(Fore.RED + f"[SIGNATURE ALERT] {sig} in {file}")
                    quarantine(file)

                    return file

    except:
        pass

    return None


def generate_report(total, threats):

    report = {
        "files_scanned": total,
        "threats_found": len(threats),
        "threat_files": threats
    }

    with open("scan_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print(Fore.BLUE + "Report saved to scan_report.json")


def scan_folder(folder):

    files = []

    for root, dirs, names in os.walk(folder):

        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        for n in names:
            files.append(os.path.join(root, n))

    print(Fore.CYAN + "\n[SCAN] Starting analysis...\n")

    threats = []

    with ThreadPoolExecutor() as ex:

        results = list(tqdm(ex.map(scan_file, files), total=len(files)))

    for r in results:
        if r:
            threats.append(r)

    print(Fore.GREEN + "\n[RESULT]")
    print("Files scanned:", len(files))
    print("Threats found:", len(threats))

    generate_report(len(files), threats)


def update_signatures():

    url = "https://raw.githubusercontent.com/ChatSamuel/SPS-SECURITY/main/signatures.txt"

    try:

        r = requests.get(url)

        with open("signatures.txt", "w") as f:
            f.write(r.text)

        print("Signatures updated")

    except:

        print("Update failed")


def cli():

    parser = argparse.ArgumentParser()

    parser.add_argument("command")
    parser.add_argument("target", nargs="?")

    args = parser.parse_args()

    if args.command == "scan":

        if os.path.isdir(args.target):
            scan_folder(args.target)

        elif os.path.isfile(args.target):
            scan_file(args.target)

    elif args.command == "update":

        update_signatures()


if __name__ == "__main__":

    print(logo)

    cli()
