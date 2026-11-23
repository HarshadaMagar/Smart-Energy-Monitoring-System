# PLAN-001: Pre-Work, Setup, and Security

**Created:** 2026-11-23
**Status:** Completed
**Addresses:** Establish a reproducible, secure Python/Flask and MySQL development foundation for VoltWise before feature implementation.

---

## 1. Context & motivation

The project specification identifies Feature 0 as the setup and security prerequisite. The baseline [current state report](../current_state_report.md) shows a greenfield workspace containing the AGENT_MD framework but no application source, test suite, pinned dependencies, MySQL environment, or CI configuration.

This plan creates only the foundation needed for test-first feature work. It does not implement the role dashboards, account workflows, sensor integration, charts, or reports described in later features.

---

## 2. Goals

- **G1:** The repository has a project-specific ignore policy and contains no tracked secrets or environment files.
- **G2:** A documented environment starts the Flask application against a configured local MySQL test database.
- **G3:** Runtime and test dependencies are pinned and install reproducibly.
- **G4:** The application, test, template, static asset, migration, and configuration directories exist with conventional Flask structure.
- **G5:** One repeatable test command and a CI skeleton pass from a clean checkout.
- **G6:** `plan/current_state_report.md` records the greenfield baseline, setup files, and validation results.

---

## 3. Non-goals

- Implement authentication, role dashboards, database entities, charts, alerts, reports, or hardware communication.
- Choose or provision a production MySQL or hosting environment.
- Choose secure Flask sessions or JWT as the authentication mechanism.
- Add feature-specific UI or business logic beyond the setup skeleton.
- Implement a production deployment pipeline or sensor communication provider.

---

## 4. Approach

Create only the project foundation needed for later test-first feature work. Keep environment-specific values in environment variables and provide `.env.example` containing names and safe placeholders only.

The application uses an application factory and centralized configuration. Test configuration targets an isolated MySQL test database and fails clearly when required database or secret configuration is missing rather than silently using unsafe defaults.

Alternatives considered:

- **SQLite fallback:** Rejected because VoltWise targets MySQL and setup should verify MySQL-capable configuration and constraints.
- **A monolithic setup script:** Rejected in favor of documented dependency installation and small configuration/test entry points.
- **Automatic production defaults:** Rejected because credentials and deployment targets are not known and unsafe defaults could reach source control.

### 4.1 Repository and environment setup

1. Add or verify `.gitignore` entries for `.env`, virtual environments, caches, database files, coverage output, and local secrets.
2. Add `.env.example` with Flask, MySQL, secret-key, and future hardware placeholders.
3. Add a configuration module that validates required environment variables and never commits real values.

### 4.2 Application and test foundation

1. Create `app/`, `tests/`, `templates/`, `static/`, `migrations/`, and configuration structure as appropriate to the selected Flask layout.
2. Add pinned runtime and test dependencies plus setup instructions.
3. Write a startup/test-configuration test before creating the application factory.
4. Implement a minimal application factory and health route, without feature routes or business entities.
5. Add database startup or migration placeholders without production schema logic.

### 4.3 Verification and CI

1. Install dependencies in a clean environment.
2. Run the minimal test suite and dependency check.
3. Add a CI skeleton or documented command for repeatable test execution.
4. Scan tracked files and available git history for secrets.
5. Update the current state report with exact commands and observed results.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Audit the repository and add project-specific `.gitignore` rules | 20 min | — |
| 2 | Create `.env.example` and environment validation/configuration | 45 min | 1 |
| 3 | Create pinned runtime/test dependency manifests and setup instructions | 45 min | 1 |
| 4 | Create Flask, test, template, static, migration, and configuration directories | 45 min | 3 |
| 5 | Write Flask startup and test-configuration tests | 30 min | 4 |
| 6 | Implement the application factory and minimal health route | 45 min | 5 |
| 7 | Add the repeatable test command and CI skeleton | 45 min | 6 |
| 8 | Run clean-environment install, tests, and secret scanning | 30 min | 2, 7 |
| 9 | Update `plan/current_state_report.md` | 20 min | 8 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| MySQL credentials or test instance are unavailable | Medium | High | Start with explicit configuration errors and document a local/test setup that can be completed when MySQL is available |
| Dependency versions have environment incompatibilities | Medium | Medium | Pin tested versions and verify installation from a clean environment |
| Secret data is introduced by `.env` or logs | Medium | High | Ignore environment files, use placeholders, validate configuration, and scan git history |
| Setup work grows into feature implementation | Medium | Medium | Keep only one minimal health/startup path and defer feature code to PLAN-002 |
| Flask structure conflicts with later authentication design | Low | Medium | Use an application factory and centralized configuration so sessions/JWT can be integrated later |

---

## 7. Success criteria

- [ ] G1 is verified by an ignore-policy review and secret scan.
- [ ] G2 is verified by starting the Flask app with a valid test configuration.
- [ ] G3 is verified by clean dependency installation and pinned manifest review.
- [ ] G4 is verified by the initial directory structure and documented setup.
- [ ] G5 is verified with a passing test command or CI run.
- [ ] G6 is verified by a dated current-state update.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 0 and Critical Pre-Work
- `AGENT_MD/plan/rules.md` — Plan, report, and test-first conventions
- `AGENT_MD/plan/current_state_report.md` — Greenfield baseline
- `AGENT_MD/plan/plans/PLAN-000_template.md` — Reserved template reference

