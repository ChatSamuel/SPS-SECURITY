from sps_security.utils.hashing import get_hash
from colorama import Fore

def hash_scan(file, malware_hashes):

    file_hash = get_hash(file)

    if file_hash in malware_hashes:

        print(Fore.RED + f"[HASH ALERT] {file}")
        print(Fore.YELLOW + f"SHA256: {file_hash}")

        return True

    return False
