import typer
from rich.console import Console
from rich.table import Table

from datatrace.core import add_dataset, load_metadata
from datatrace.tracking import track_dataset
from datatrace.experiments import log_experiment

app = typer.Typer(help="Datatrace – Lightweight MLOps dataset & experiment tracker")
console = Console()


@app.command()
def add(path: str):
    """Add and version a dataset"""
    version = add_dataset(path)
    console.print(f"📦 Dataset added → version [green]{version}[/green]")


@app.command()
def list():
    """List all tracked datasets"""
    metadata = load_metadata()

    if not metadata:
        console.print("[yellow]No datasets found[/yellow]")
        return

    table = Table(title="📁 Versioned Datasets")
    table.add_column("Version", style="cyan")
    table.add_column("Original File")
    table.add_column("Stored Name")
    table.add_column("Timestamp", style="green")

    for v, info in metadata.items():
        table.add_row(
            v,
            info["file"],
            info["stored_as"],
            info["timestamp"]
        )

    console.print(table)


@app.command()
def track(path: str):
    """Track dataset usage"""
    track_dataset(path)
    console.print("📊 Dataset usage tracked", style="bold green")


@app.command()
def experiment(
    name: str,
    version: str,
    lr: float,
    accuracy: float
):
    """Log an ML experiment"""
    log_experiment(
        experiment_name=name,
        dataset_version=version,
        params={"lr": lr},
        metrics={"accuracy": accuracy}
    )
    console.print("🧪 Experiment logged", style="bold green")


if __name__ == "__main__":
    app()
