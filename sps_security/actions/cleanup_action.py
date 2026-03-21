import os
from rich.console import Console
from sps_security.security.removal import secure_delete

console = Console()

QUARANTINE_DIR = "quarantine"


def cleanup_quarantine():
    if not os.path.exists(QUARANTINE_DIR):
        console.print("[yellow]No quarantine folder[/yellow]")
        return

    # pegar apenas arquivos válidos
    files = [
        f for f in os.listdir(QUARANTINE_DIR)
        if os.path.isfile(os.path.join(QUARANTINE_DIR, f))
    ]

    if not files:
        console.print("[green]Quarantine empty[/green]")
        return

    console.print("\n[bold]Files in quarantine:[/bold]\n")

    for i, f in enumerate(files):
        console.print(f"[cyan][{i}][/cyan] {f}")

    console.print()
    choice = input("Delete all? (y/n): ").strip().lower()

    if choice == "y":
        for f in files:
            path = os.path.join(QUARANTINE_DIR, f)
            secure_delete(path)

        console.print("\n[bold green]Quarantine cleaned[/bold green]")
    else:
        console.print("[yellow]Canceled[/yellow]")
