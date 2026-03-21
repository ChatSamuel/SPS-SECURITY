from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_banner():
    banner = Text("""
 ███████╗██████╗ ███████╗      ███████╗███████╗ ██████╗
 ██╔════╝██╔══██╗██╔════╝      ██╔════╝██╔════╝██╔════╝
 ███████╗██████╔╝███████╗█████╗███████╗█████╗  ██║
 ╚════██║██╔═══╝ ╚════██║╚════╝╚════██║██╔══╝  ██║
 ███████║██║     ███████║      ███████║███████╗╚██████╗
 ╚══════╝╚═╝     ╚══════╝      ╚══════╝╚══════╝ ╚═════╝
""", style="bold green")

    console.print(
        Panel(
            banner,
            title="[bold green]SPS SECURITY v2.0[/bold green]",
            subtitle="[dim]Multi-Engine Antivirus System by Samuel Pontes[/dim]",
            border_style="green"
        )
    )
