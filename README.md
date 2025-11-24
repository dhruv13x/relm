# Repo Manager

A unified CLI tool to automate versioning, git operations, and PyPI releases for the dhruv13x tool suite.

## Features

- **Project Discovery**: Automatically detects Python projects with `pyproject.toml`.
- **Smart Versioning**: Bumps versions (major, minor, patch) in `pyproject.toml` and `__init__.py`.
- **Git Automation**: Stages, commits, and pushes release changes.
- **PyPI Release**: Builds and uploads packages to PyPI.

## Installation

```bash
pip install -e .
```

## Usage

```bash
relm --help
```
