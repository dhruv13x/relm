# src/relm/core.py

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

@dataclass
class Project:
    name: str
    version: str
    path: Path
    description: Optional[str] = None

    @property
    def pyproject_path(self) -> Path:
        return self.path / "pyproject.toml"

    def __str__(self) -> str:
        return f"{self.name} (v{self.version}) - {self.path}"

def load_project(path: Path) -> Optional[Project]:
    """
    Loads a project from a directory if it contains a valid pyproject.toml.
    """
    pyproject_file = path / "pyproject.toml"
    if not pyproject_file.exists():
        return None

    try:
        with open(pyproject_file, "rb") as f:
            data = tomllib.load(f)
        
        project_data = data.get("project", {})
        name = project_data.get("name")
        version = project_data.get("version")
        description = project_data.get("description")

        if name and version:
            return Project(
                name=name,
                version=version,
                path=path,
                description=description
            )
    except Exception as e:
        # We might want to log this error in a real app
        pass
    
    return None

def find_projects(root_path: Path) -> List[Project]:
    """
    Scans the immediate subdirectories of root_path for valid projects.
    """
    projects = []
    if not root_path.exists() or not root_path.is_dir():
        return projects

    # Check if the root itself is a project
    root_project = load_project(root_path)
    if root_project:
        projects.append(root_project)

    # Check subdirectories
    for item in root_path.iterdir():
        if item.is_dir() and item != root_path:
            # Avoid recursing too deep or checking hidden dirs for now
            if item.name.startswith("."):
                continue
            
            project = load_project(item)
            if project:
                projects.append(project)
    
    return sorted(projects, key=lambda p: p.name)
