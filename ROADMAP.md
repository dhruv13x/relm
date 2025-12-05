# 🗺️ relm Smart Roadmap

This document outlines the strategic vision for `relm`, categorized from foundational essentials to "God Level" ambitions. It serves as a living guide for development, prioritizing stability, ecosystem integration, and future-forward capabilities.

---

## Phase 1: Foundation (CRITICALLY MUST HAVE)
**Focus**: Core functionality, stability, security, and basic usage.
**Timeline**: Q1

- [x] **Project Discovery & Listing** (`relm list`) - *Automatically find projects with `pyproject.toml`.*
- [x] **Basic Release Flow** (`relm release`) - *Version bumping, tagging, and committing.*
- [x] **Bulk Operations** - *Release, install, or run commands across all projects at once.*
- [x] **Git Integration** - *Automated staging, committing, tagging, and pushing.*
- [x] **Status Reporting** (`relm status`) - *View git status and versions for all projects.*
- [x] **Comprehensive Unit Tests** - *Existing `tests/` directory and test runners.*
- [x] **Custom Commit Messages** - *Allow users to customize the release commit message template.*
- [x] **Pre-release Version Support** - *Support for `alpha`, `beta`, and `rc` suffixes.*
- [ ] **Workspace Cleaning** (`relm clean`) - *Recursively remove build artifacts (`dist/`, `build/`, `__pycache__`).*

---

## Phase 2: The Standard (MUST HAVE)
**Focus**: Feature parity with top competitors, user experience improvements, and robust error handling.
**Timeline**: Q2

- [ ] **Automated Changelog Generation** - *Parse Conventional Commits to generate/update `CHANGELOG.md`.*
- [ ] **Configuration File Support** (`.relm.toml`) - *Global configuration to reduce CLI argument repetition.*
- [ ] **Dependency Awareness** - *Topological sort for execution (build `lib-a` before `app-b`).*
- [ ] **"Changed Since" Detection** - *Only run commands on projects modified since the last release (CI optimization).*
- [ ] **Project Scaffolding** (`relm create`) - *Generate new standard Python projects from templates.*
- [ ] **Advanced Interactive Mode** - *Guided wizard for releases (selecting version bump, editing notes).*
- [ ] **Pre-flight Checks** - *Validate credentials, registry access, and environment health before starting.*

---

## Phase 3: The Ecosystem (INTEGRATION & SHOULD HAVE)
**Focus**: Webhooks, API exposure, 3rd party plugins, SDK generation, and extensibility.
**Timeline**: Q3

- [ ] **CI/CD Platform Integration** - *Native support for generating GitHub Actions/GitLab CI workflows.*
- [ ] **Webhook Notifications** - *Post to Slack/Discord/Teams upon successful or failed releases.*
- [ ] **Plugin Architecture** - *Hooks for custom build steps (e.g., "run this script before tagging").*
- [ ] **Non-PyPI Index Support** - *First-class support for private registries (Artifactory, Nexus) configuration.*
- [ ] **Public SDK** - *Stabilize internal APIs (`relm.core`, `relm.git_ops`) for external tool usage.*
- [ ] **Mixed-Language Monorepo Support** - *Extend discovery to `package.json` (Node) or `go.mod` (Go).*

---

## Phase 4: The Vision (GOD LEVEL)
**Focus**: "Futuristic" features, AI integration, advanced automation, and industry-disrupting capabilities.
**Timeline**: Q4

- [ ] **AI-Powered Release Notes** - *Use LLMs to summarize code diffs into human-readable release notes.*
- [ ] **Predictive Release Scheduling** - *Analyze commit velocity to suggest optimal release windows.*
- [ ] **Cross-Repository Dependency Graph** - *Link and manage dependencies across multiple git repositories.*
- [ ] **"Shadow Release" Mode** - *Simulate a full release (build, publish to local mock registry, install, test) without side effects.*
- [ ] **Automated Dependency Upgrades** - *Local "Dependabot" that bumps dependencies and runs tests automatically.*

---

## The Sandbox (OUT OF THE BOX / OPTIONAL)
**Focus**: Wild, creative, experimental ideas that set the project apart.

- [ ] **Voice Control** - *"Hey relm, ship it to production."*
- [ ] **IoT Integration** - *Flash smart lights red on build failure, green on release success.*
- [ ] **Gamification** - *Leaderboards and achievements for release frequency and quality.*
