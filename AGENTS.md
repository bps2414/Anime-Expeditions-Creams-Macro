# AGENTS.md - Repository Guidelines for Anime Expeditions Macro

## Project & Workflow Overview
- **Upstream Repository (`origin`):** `Cweamy/Anime-Expeditions-Creams-Macro`
- **Fork Repository (`fork`):** `bps2414/Anime-Expeditions-Creams-Macro`
- **Primary Goal:** Maintain a clean personal fork while contributing high-quality, atomic Pull Requests back to the upstream repository (`Cweamy/main`).

---

## 1. Code & Language Standards
- **Code Language:** All Python code, function names, variable names, and data structures must be in **English**.
- **Comments & Documentation:** All inline comments, docstrings, and module documentation **MUST be written in English** so that PRs are instantly readable and ready for upstream merge by the main maintainer.
- **Code Quality:** Keep code simple, modular, and functional (KISS principle). Avoid bloated abstractions or single-use helper classes.

---

## 2. Commit & Git Rules
- **Commit Style:** Use [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat(scope): ...` for new features
  - `fix(scope): ...` for bug fixes
  - `test(scope): ...` for adding or updating unit tests
  - `style(scope): ...` for formatting or translation of comments
  - `docs(scope): ...` for documentation updates
- **Atomic Commits:** Make small, focused commits that do one thing well. This makes code reviews on GitHub fast and easy for the upstream maintainer.
- **Branching Strategy:**
  - Create feature/fix branches for new work (`feat/my-feature` or `fix/my-bugfix`).
  - Never commit directly to `main` when developing new features intended for PRs.

---

## 3. Validation & Testing Mandatory Rules
Before making any commit or claiming completion:
1. **Run Unit Tests:** Execute `python -m pytest tests/ -v` to ensure all tests pass.
2. **Compile Check:** Ensure there are no Python syntax errors or broken imports.
3. **Verify Functionality:** Confirm that existing functionality has not regressed.

---

## 4. AI Agent Guidelines
- **Response Language:** Explain concepts in clear, easy-to-understand **Brazilian Portuguese**.
- **Code Generation:** Write code and comments strictly in **English**.
- **Verification First:** Never declare a task complete without running tests and checking git status.
