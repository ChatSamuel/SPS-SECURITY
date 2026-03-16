from colorama import Fore

def signature_scan(file, signatures):

    try:

        with open(file, "r", errors="ignore") as f:

            content = f.read()

            for sig in signatures:

                if sig in content:

                    print(Fore.RED + f"[SIGNATURE ALERT] {sig} in {file}")
                    return True

    except:
        pass

    return False
