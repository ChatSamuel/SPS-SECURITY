import os
from rich.console import Console
from sps_security.security.logger import log_detection

console = Console()


def secure_delete(file_path):
    try:
        if not os.path.exists(file_path):
            console.print(f"[yellow]File not found:[/yellow] {file_path}")
            return False

        # overwrite before delete
        with open(file_path, "ba+", buffering=0) as f:
            length = f.tell()
            f.seek(0)
            f.write(os.urandom(length))

        os.remove(file_path)

        console.print(f"[bold red]File securely deleted:[/bold red] {file_path}")
        log_detection(file_path, "DELETED", "QUARANTINE")

        return True

    except Exception as e:
        console.print(f"[red]Delete error:[/red] {e}")
        return False
