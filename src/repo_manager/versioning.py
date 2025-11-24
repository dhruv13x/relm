import re
from pathlib import Path
from typing import Tuple, List

def parse_version(version: str) -> Tuple[int, int, int]:
    """
    Parses a version string 'x.y.z' into a tuple of integers.
    """
    try:
        parts = version.split('.')
        if len(parts) < 3:
            # Handle cases like '0.1' -> '0.1.0'
            parts.extend(['0'] * (3 - len(parts)))
        return int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        raise ValueError(f"Invalid version format: {version}")

def bump_version_string(version: str, part: str) -> str:
    """
    Bumps the version string based on the part ('major', 'minor', 'patch').
    """
    major, minor, patch = parse_version(version)
    
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump part: {part}")
        
    return f"{major}.{minor}.{patch}"

def update_file_content(path: Path, old_version: str, new_version: str) -> bool:
    """
    Replaces occurrences of old_version with new_version in the file at path.
    Returns True if changes were made.
    """
    if not path.exists():
        return False
        
    try:
        content = path.read_text(encoding="utf-8")
        
        new_content = content
        
        # Pattern for pyproject.toml: version = "1.0.0"
        toml_pattern = re.compile(rf'version\s*=\s*"{re.escape(old_version)}"')
        if toml_pattern.search(content):
            new_content = toml_pattern.sub(f'version = "{new_version}"', new_content)
            
        # Pattern for __init__.py: __version__ = "1.0.0"
        init_pattern = re.compile(rf'__version__\s*=\s*"{re.escape(old_version)}"')
        if init_pattern.search(content):
            new_content = init_pattern.sub(f'__version__ = "{new_version}"', new_content)
            
        if new_content != content:
            path.write_text(new_content, encoding="utf-8")
            return True
            
    except Exception as e:
        print(f"Error updating {path}: {e}")
        return False
        
    return False

def update_version_tests(project_path: Path, old_version: str, new_version: str) -> List[str]:
    """
    Scans the 'tests' directory for files containing the old version string
    in an assertion context and updates them. returns list of updated files.
    """
    updated_files = []
    tests_dir = project_path / "tests"
    if not tests_dir.exists():
        return updated_files

    # Regex to match: assert ... == "1.2.3" or assert "1.2.3" == ...
    # We are generous with whitespace
    # This might need refinement but covers standard cases.
    # We actually just look for the literal string "1.2.3" inside test files
    # because replacing it strictly in context is safer than broad replace, 
    # but parsing python AST is too heavy. 
    # Let's look for the exact string "old_version" to be safe, 
    # but only if it looks like a version check? 
    # actually, if a test file has the version string "1.0.0", it is 99% likely the version check.
    
    for test_file in tests_dir.rglob("*.py"):
        try:
            content = test_file.read_text(encoding="utf-8")
            if old_version in content:
                # Check if it's surrounded by quotes to avoid partial matches
                # e.g. matching "1.0" in "1.0.0" (though old_version is usually full)
                
                # Simple string replace for "old_version" -> "new_version"
                # We use quotes to ensure we match string literals
                if f'"{old_version}"' in content:
                    new_content = content.replace(f'"{old_version}"', f'"{new_version}"')
                    test_file.write_text(new_content, encoding="utf-8")
                    updated_files.append(str(test_file.relative_to(project_path)))
                elif f"'{old_version}'" in content:
                    new_content = content.replace(f"'{old_version}'", f"'{new_version}'")
                    test_file.write_text(new_content, encoding="utf-8")
                    updated_files.append(str(test_file.relative_to(project_path)))
        except Exception:
            pass
            
    return updated_files
