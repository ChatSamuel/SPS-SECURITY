import os
import shutil
from datetime import datetime
from rich.console import Console

console = Console()

QUARANTINE_DIR = "quarantine"


def ensure_quarantine():
    if not os.path.exists(QUARANTINE_DIR):
        os.makedirs(QUARANTINE_DIR)


def quarantine_file(file_path):
    try:
        ensure_quarantine()

        filename = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        new_name = f"{timestamp}_{filename}"
        dest = os.path.join(QUARANTINE_DIR, new_name)

        shutil.move(file_path, dest)

        console.print(
            f"[bold red]⚠ File moved to quarantine:[/bold red] {dest}"
        )

        return True

    except Exception as e:
        console.print(f"[red]Quarantine error:[/red] {e}")
        return False
