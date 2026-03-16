from colorama import Fore

HEURISTIC_PATTERNS = [
    "powershell -enc",
    "cmd.exe /c",
    "nc -e",
    "wget http",
    "curl http",
    "base64 -d"
]

def heuristic_scan(file):

    try:

        with open(file, "r", errors="ignore") as f:

            content = f.read()

            for pattern in HEURISTIC_PATTERNS:

                if pattern in content:

                    print(Fore.YELLOW + f"[HEURISTIC ALERT] {pattern} in {file}")
                    return True

    except:
        pass

    return False
