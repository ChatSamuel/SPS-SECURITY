import os
import shutil
from colorama import Fore

QUARANTINE_FOLDER = "quarantine"

def quarantine(file):

    if not os.path.exists(QUARANTINE_FOLDER):
        os.mkdir(QUARANTINE_FOLDER)

    try:

        shutil.move(file, QUARANTINE_FOLDER)

        print(Fore.MAGENTA + f"[QUARANTINE] {file}")

    except:
        pass
