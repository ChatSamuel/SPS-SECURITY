import zipfile
from rich.console import Console
from rich.panel import Panel

console = Console()


def run_apk(file):
    console.print("\n[bold cyan]APK Analysis Started...[/bold cyan]\n")

    try:
        with zipfile.ZipFile(file, 'r') as apk:
            files = apk.namelist()

            dex_files = [f for f in files if f.endswith(".dex")]
            manifest = [f for f in files if "manifest" in f.lower()]

            console.print(
                Panel(
                    f"""
📦 Total Files: {len(files)}
⚙️ DEX Files: {len(dex_files)}
📜 Manifest Found: {"YES" if manifest else "NO"}
""",
                    title="[bold]APK SCAN RESULT[/bold]",
                    border_style="cyan"
                )
            )

    except Exception as e:
        console.print(f"[red]Error analyzing APK:[/red] {e}")
