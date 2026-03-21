from rich.console import Console
from rich.panel import Panel

console = Console()

def show_result(result: dict):
    risk = result.get("risk")
    detections = result.get("detections")
    confidence = result.get("confidence")

    if risk == "SAFE":
        color = "green"
        label = "🟢 SAFE"
    elif risk == "LOW":
        color = "yellow"
        label = "🟡 LOW RISK"
    elif risk == "MEDIUM":
        color = "orange1"
        label = "🟠 SUSPICIOUS"
    elif risk == "HIGH":
        color = "red"
        label = "🔴 DANGEROUS"
    else:
        color = "bold red"
        label = "💀 CRITICAL"

    console.print(
        Panel(
            f"""
[bold]{label}[/bold]

📊 Detections: {detections}
📈 Confidence: {round(confidence * 100, 1)}%
""",
            title="[bold]SCAN RESULT[/bold]",
            border_style=color
        )
    )
