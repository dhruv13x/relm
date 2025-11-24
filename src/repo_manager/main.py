import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .core import find_projects
from .release import perform_release

console = Console()

def list_projects(path: Path):
    projects = find_projects(path)
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

def main():
    parser = argparse.ArgumentParser(
        description="Manage releases and versioning for local Python projects."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to the root directory containing projects (default: current dir)."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all discovered projects")
    
    # Release command
    release_parser = subparsers.add_parser("release", help="Release a new version of a project")
    release_parser.add_argument("project_name", help="Name of the project to release (must match pyproject.toml name)")
    release_parser.add_argument("type", choices=["major", "minor", "patch"], default="patch", nargs="?", help="Type of version bump")
    release_parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompts (assume yes)")

    args = parser.parse_args()
    root_path = Path(args.path).resolve()

    if args.command == "list":
        list_projects(root_path)
    
    elif args.command == "release":
        all_projects = find_projects(root_path)
        
        target_projects = []
        check_changes_flag = False

        if args.project_name == "all":
            target_projects = all_projects
            check_changes_flag = True
            console.print(f"[bold]Running Bulk Release on {len(target_projects)} projects...[/bold]")
        else:
            # Find single project
            target = next((p for p in all_projects if p.name == args.project_name), None)
            if not target:
                console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
                sys.exit(1)
            target_projects = [target]

        # Execute releases
        results = {"released": [], "skipped": [], "failed": []}

        for project in target_projects:
            # Skip template/meta repos if needed, but git_has_changes handles most logic
            try:
                success = perform_release(
                    project, 
                    args.type, 
                    yes_mode=args.yes, 
                    check_changes=check_changes_flag
                )
                if success:
                    results["released"].append(project.name)
                else:
                    results["skipped"].append(project.name)
            except Exception as e:
                console.print(f"[red]Critical error releasing {project.name}: {e}[/red]")
                results["failed"].append(project.name)

        # Summary
        if args.project_name == "all":
            console.rule("Bulk Release Summary")
            console.print(f"[green]Released: {len(results['released'])}[/green] {results['released']}")
            console.print(f"[yellow]Skipped:  {len(results['skipped'])}[/yellow]")
            if results["failed"]:
                console.print(f"[red]Failed:   {len(results['failed'])}[/red] {results['failed']}")

if __name__ == "__main__":
    main()
