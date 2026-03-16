from colorama import Fore

def binary_scan(file, patterns):

    try:

        with open(file, "rb") as f:

            data = f.read()

        text = data.decode("latin-1", errors="ignore")

        for p in patterns:

            if p in text:

                print(Fore.YELLOW + f"[BINARY ALERT] {p} in {file}")
                return True

    except:
        pass

    return False
