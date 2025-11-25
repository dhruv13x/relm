<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/relm/main/relm_logo.png" alt="relm logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/relm.svg)](https://pypi.org/project/relm/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/relm.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/relm/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/relm/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/relm/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/relm/graph/badge.svg)](https://codecov.io/gh/dhruv13x/relm)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/relm/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/relm.svg)
[![PyPI Downloads](https://img.shields.io/pypi/dm/relm.svg)](https://pypistats.org/packages/relm)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/relm.svg)](https://pypi.org/project/relm/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Docs -->
[![Docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://your-docs-link)

</div>


# relm

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
