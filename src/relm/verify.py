import json
import urllib.request
import urllib.error
from typing import Tuple
from rich.console import Console
from .core import Project
from .git_ops import git_tag_exists

console = Console()

def verify_project_release(project: Project) -> Tuple[bool, str]:
    """
    Verifies if the locally defined version of the project is available on PyPI.
    Returns (success: bool, message: str).
    """
    local_version = project.version
    tag_name = f"v{local_version}"
    
    # 1. Check if local tag exists (Strict check as requested)
    if not git_tag_exists(project.path, tag_name):
        return False, f"Local git tag '{tag_name}' does not exist. Was the release command run?"

    # 2. Query PyPI using its JSON API
    url = f"https://pypi.org/pypi/{project.name}/json"
    try:
        # We use urllib to avoid extra dependencies like requests
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            available_versions = list(data.get("releases", {}).keys())
            
            if local_version in available_versions:
                return True, f"Version {local_version} is verified on PyPI."
            else:
                latest = data.get("info", {}).get("version", "unknown")
                return False, f"Version {local_version} not found on PyPI. Latest is {latest}."

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, f"Failed to query PyPI for '{project.name}'. Package might not be published yet."
        return False, f"PyPI API returned error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"Failed to connect to PyPI: {e.reason}"
    except json.JSONDecodeError:
        return False, "Failed to parse PyPI response."
    except Exception as e:
        return False, f"Unexpected error: {e}"
