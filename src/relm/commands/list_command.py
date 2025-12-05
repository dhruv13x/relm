from argparse import Namespace, _SubParsersAction
from pathlib import Path
from rich.console import Console
from rich.table import Table
from ..core import find_projects

def register(subparsers: _SubParsersAction):
    """Register the list command."""
    list_parser = subparsers.add_parser("list", help="List all discovered projects")
    list_parser.set_defaults(func=execute)

def execute(args: Namespace, console: Console):
    """Execute the list command."""
    root_path = Path(args.path).resolve()
    projects = find_projects(root_path)
    if not projects:
        console.print("[yellow]No projects found in this directory.[/yellow]")
        return

    table = Table(title=f"Found {len(projects)} Projects")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Path", style="green")
    table.add_column("Description")

    for project in projects:
        table.add_row(
            project.name,
            project.version,
            str(project.path),
            project.description or ""
        )

    console.print(table)
