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
