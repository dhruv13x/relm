# 🗺️ relm Roadmap

This document outlines the strategic vision for `relm`, categorized into phases from foundational requirements to ambitious, long-term goals.

---

## Phase 1: Foundation (Q1)
**Focus**: Core functionality, stability, security, and basic usage.

- [x] Initial CLI release (`list`, `release`)
- [ ] Add support for custom commit messages during release
- [ ] Add support for pre-release versions (e.g., `alpha`, `beta`, `rc`)
- [ ] Enhanced error handling and user feedback
- [ ] Comprehensive unit and integration test suite

---

## Phase 2: The Standard (Q2)
**Focus**: Feature parity with top competitors, user experience improvements, and robust error handling.

- [ ] Add a `changelog` command to generate a changelog from commit history
- [ ] Interactive mode for guided releases
- [ ] Configuration file support (`.relm.toml`) to reduce CLI arguments
- [ ] Pre-flight checks (e.g., check for clean git status, valid credentials)
- [ ] Support for non-PyPI package indexes

---

## Phase 3: The Ecosystem (Q3)
**Focus**: Webhooks, API exposure, 3rd party plugins, and extensibility.

- [ ] Plugin architecture for custom release steps (e.g., run tests, build docs)
- [ ] Webhook notifications (Slack, Discord, etc.) on successful or failed releases
- [ ] Integration with CI/CD platforms (GitHub Actions, GitLab CI)
- [ ] SDK for programmatic releases from other Python tools
- [ ] Support for monorepos with mixed languages (e.g., Node.js, Go)

---

## Phase 4: The Vision (GOD LEVEL) (Q4)
**Focus**: "Futuristic" features, AI integration, advanced automation, and industry-disrupting capabilities.

- [ ] AI-powered release notes generation based on commit analysis
- [ ] Automated dependency analysis and upgrade recommendations
- [ ] Predictive release scheduling based on commit velocity and project milestones
- [ ] Cross-repository release orchestration and dependency management
- [ ] "Shadow release" mode to simulate a release without publishing

---

## The Sandbox (OUT OF THE BOX / OPTIONAL)
**Focus**: Wild, creative, experimental ideas that set the project apart.

- [ ] Gamification of the release process (e.g., achievements for frequent releases)
- [ ] Voice-activated releases ("Hey relm, release a new version")
- [ ] Integration with IoT devices to signal release status (e.g., a light turns green on success)

---

## Proposed Features (Detailed Analysis)

1. **Dependency Awareness & Graph Resolution (Critical)**
   Currently, relm treats every project as an isolated island. It lists them and releases them, but it doesn't understand how they relate to one another.
   * *The Need*: In a tool suite, project-a often depends on project-b.
   * *Missing Feature*:
       * **Topological Sort**: Operations (install/release) should run in dependency order (e.g., build project-b before project-a).
       * **Cascading Releases**: If project-b releases a breaking change, the tool should detect that project-a needs its dependency requirement updated and potentially a version bump as well.
       * **Workspace Linking**: Ability to toggle dependencies between "local path" (for dev) and "pypi version" (for release).

2. **Bulk Command Execution (Task Runner)**
   You can install and release, but you cannot currently run arbitrary commands across the suite.
   * *The Need*: A developer wants to run tests or linters for all projects with one command.
   * *Missing Feature*: A `relm run <command>` or `relm exec` command.
       * Example: `relm run test` (triggers pytest in every project).
       * Example: `relm run lint` (triggers ruff in every project).

3. **Automated Changelog Generation**
   The current release process bumps the version and tags git, but it doesn't appear to generate release notes.
   * *The Need*: Consumers need to know what changed between v0.1.1 and v0.1.2.
   * *Missing Feature*: Integration with "Conventional Commits" to parse git history since the last tag and automatically append to a `CHANGELOG.md` file before committing the release.

4. **Project Scaffolding (init / create)**
   The tool can manage existing projects, but it cannot create new ones.
   * *The Need*: Adding a new tool to the suite requires manually creating folders and copying pyproject.toml boilerplate.
   * *Missing Feature*: A `relm create <project_name>` command that generates a standardized folder structure, a configured pyproject.toml, and basic source files based on a built-in template.

5. **Clean / Prune Functionality**
   Building distributions creates build/, dist/, and .egg-info/ directories scattered throughout the workspace.
   * *The Need*: Quickly resetting the workspace to a pristine state.
   * *Missing Feature*: A `relm clean` command to recursively remove build artifacts and `__pycache__` from all projects.

6. **"Changed Since" Detection (CI Optimization)**
   While `relm release` has a check for git changes, generic task running usually lacks this.
   * *The Need*: In a CI environment, I only want to run tests for projects that have actually changed (or whose dependencies have changed) since the last commit/branch point.
   * *Missing Feature*: A flag like `relm run test --affected` which calculates the diff graph and only targets modified projects.
