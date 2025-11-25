#  relm

A unified CLI tool to manage versioning, git, and PyPI releases for multiple projects.

[![PyPI Version](https://img.shields.io/pypi/v/relm)](https://pypi.org/project/relm/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/dhruv13x/relm/ci.yml)](https://github.com/dhruv13x/relm/actions)
[![License](https://img.shields.io/pypi/l/relm)](https://github.com/dhruv13x/relm/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/relm)](https://pypi.org/project/relm/)

## About

`relm` is a command-line tool designed to streamline the release process for Python projects. It automates version bumping, git tagging, and uploading to PyPI, making it ideal for managing multiple libraries or microservices from a single repository.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+

### Installation
For a clean, isolated installation, use `pipx`:
```bash
pipx install relm
```
Alternatively, you can use `pip`:
```bash
pip install relm
```

### Usage Example
1. **Navigate to your repository** containing one or more Python projects.
2. **List all discoverable projects**:
   ```bash
   relm list
   ```
3. **Release a new version of a specific project**:
   ```bash
   # Bump the patch version (e.g., 0.1.0 -> 0.1.1)
   relm release my-project-name patch

   # Bump the minor version (e.g., 0.1.1 -> 0.2.0)
   relm release my-project-name minor
   ```
> **Note**: The `project_name` must match the `name` field in the project's `pyproject.toml`.

## ✨ Key Features

- **Automated Project Discovery**: Scans directories to find all valid Python projects with a `pyproject.toml`.
- **Smart Version Bumping**: Increments semantic versions (`major`, `minor`, `patch`) in your project files.
- **Git Integration**: Automatically stages, commits, and pushes release changes to your remote repository.
- **PyPI Publishing**: Builds your project and uploads the distributable to PyPI.
- **Bulk Release Mode**: **Release all discovered projects at once with a single command.**

## ⚙️ Configuration & Advanced Usage

### CLI Arguments

The `relm` CLI is organized into subcommands.

#### Global Arguments

| Argument | Default | Description |
|---|---|---|
| `--path` | `.` | The root directory to scan for projects. |

#### `list` Command

Lists all projects found in the specified path.

```bash
relm list --path /path/to/your/projects
```

#### `release` Command

Handles the versioning and release process.

| Argument | Default | Description |
|---|---|---|
| `project_name` | (required) | The name of the project to release. Use `all` to release all projects with detected changes. |
| `type` | `patch` | The type of version bump (`major`, `minor`, `patch`). |
| `-y`, `--yes` | `False` | Skips all confirmation prompts, assuming an answer of "yes." |

## 🏗️ Architecture

### Directory Structure
```
src/relm/
├── __init__.py     # Package initializer
├── banner.py       # ASCII art for the CLI
├── core.py         # Core logic for project discovery
├── git_ops.py      # Git-related operations
├── main.py         # CLI entry point (argparse)
├── release.py      # Release orchestration logic
└── versioning.py   # Version bumping utilities
```

### Core Logic Flow
1. **`main.py`**: Parses CLI arguments and orchestrates the requested command (`list` or `release`).
2. **`core.py`**: The `find_projects` function recursively scans the specified directory for `pyproject.toml` files and parses them to identify valid projects.
3. **`release.py`**: The `perform_release` function coordinates the release process, calling other modules for specific tasks.
4. **`versioning.py`**: Bumps the version number in `pyproject.toml` and `__init__.py`.
5. **`git_ops.py`**: Handles staging, committing, and pushing changes to the remote Git repository.

## 🗺️ Roadmap

- [x] Initial release
- [ ] Add support for custom commit messages
- [ ] Add support for pre-release versions (e.g., `alpha`, `beta`, `rc`)
- [ ] Add a `changelog` command to generate a changelog from commit history

## 🤝 Contributing & License

Contributions are welcome! Please feel free to submit a pull request or open an issue.

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
