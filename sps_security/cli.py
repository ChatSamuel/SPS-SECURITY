import argparse
from sps_security.core.scanner import scan_folder

def load_file(path):

    try:
        with open(path) as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

def run():

    parser = argparse.ArgumentParser(description="SPS Security Scanner")

    parser.add_argument("command", help="scan")
    parser.add_argument("target", help="folder or file")

    args = parser.parse_args()

    signatures = load_file("sps_security/database/signatures.txt")
    hashes = load_file("sps_security/database/malware_hash_db.txt")

    patterns = signatures

    if args.command == "scan":
        scan_folder(args.target, signatures, hashes, patterns)
