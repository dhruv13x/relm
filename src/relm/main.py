# src/relm/main.py

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from .core import find_projects
from .release import perform_release
from .install import install_project
from .git_ops import is_git_clean, get_current_branch
from .banner import print_logo

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
    print_logo()
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

    # Install command
    install_parser = subparsers.add_parser("install", help="Install projects into the current environment")
    install_parser.add_argument("project_name", help="Name of the project to install or 'all'")
    install_parser.add_argument("--no-editable", action="store_true", help="Install in standard mode instead of editable")

    # Status command
    status_parser = subparsers.add_parser("status", help="Check git status of projects")
    status_parser.add_argument("project_name", help="Name of the project to check or 'all'", nargs="?", default="all")

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

    elif args.command == "install":
        all_projects = find_projects(root_path)
        target_projects = []

        if args.project_name == "all":
            target_projects = all_projects
            console.print(f"[bold]Bulk Installing {len(target_projects)} projects...[/bold]")
        else:
            target = next((p for p in all_projects if p.name == args.project_name), None)
            if not target:
                console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
                sys.exit(1)
            target_projects = [target]

        results = {"installed": [], "failed": []}
        editable_mode = not args.no_editable

        for project in target_projects:
            success = install_project(project, editable=editable_mode)
            if success:
                results["installed"].append(project.name)
            else:
                results["failed"].append(project.name)
        
        if args.project_name == "all":
            console.rule("Bulk Install Summary")
            console.print(f"[green]Installed: {len(results['installed'])}[/green] {results['installed']}")
            if results["failed"]:
                console.print(f"[red]Failed:    {len(results['failed'])}[/red] {results['failed']}")

    elif args.command == "status":
        all_projects = find_projects(root_path)
        target_projects = []

        if args.project_name == "all":
            target_projects = all_projects
        else:
            target = next((p for p in all_projects if p.name == args.project_name), None)
            if not target:
                console.print(f"[red]Project '{args.project_name}' not found in {root_path}[/red]")
                sys.exit(1)
            target_projects = [target]

        table = Table(title=f"Git Status for {len(target_projects)} Projects")
        table.add_column("Project", style="cyan", no_wrap=True)
        table.add_column("Version", style="magenta")
        table.add_column("Branch", style="blue")
        table.add_column("Status", style="bold")

        for project in target_projects:
            branch = get_current_branch(project.path)
            is_clean = is_git_clean(project.path)
            
            status_str = "[green]Clean[/green]" if is_clean else "[red]Dirty[/red]"
            # Check for potential conflict markers if dirty (simple heuristic) or just leave as Dirty
            
            table.add_row(
                project.name,
                project.version,
                branch,
                status_str
            )

        console.print(table)

if __name__ == "__main__":
    main()