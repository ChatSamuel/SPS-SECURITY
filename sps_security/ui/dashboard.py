"""
ui/dashboard.py
Interface simples no terminal.
"""

from rich.console import Console

console = Console()


def print_banner():
    console.print("\n[bold green]SPS-SECURITY[/bold green]\n")


def print_result(file, risk, score):
    if risk in ("HIGH", "CRITICAL"):
        console.print(f"[red][THREAT][/red] {file} -> {risk} (score={score})")
    elif risk in ("MEDIUM", "LOW"):
        console.print(f"[yellow][WARN][/yellow] {file} -> {risk}")
