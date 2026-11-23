# VoltWise — Current State Report

**Date:** 2026-11-23
**Prepared for:** Project implementation, review, and re-onboarding
**Scope:** Greenfield setup, authentication, administrator dashboard, and enterprise dashboard

**Project layout:** Backend Flask code and tests are in `backend/`; Jinja templates and browser assets are in `frontend/`.

## Update — 2026-11-23 PLAN-004 completed
- Added enterprise-owned building, room, and appliance management, including guarded update/delete operations.
- Added enterprise summary cards, room/building consumption charts, seven-day trends, limit comparisons, and monitoring history.
- Added room energy limits, threshold alerts, appliance status alerts, and enterprise-owned daily/weekly/monthly/asset report summaries.
- All enterprise data routes derive ownership from the authenticated account session.
- Added an idempotent database migration for existing report tables.
- Test result: `31 passed, 0 failed` across the full suite.
- Key files: `app/enterprise.py`, `app/templates/enterprise/`, `tests/test_enterprise.py`.

---

## Update — 2026-11-23 PLAN-001 / PLAN-002
- Added the Flask application factory, environment template, pinned dependencies, setup guide, test suite, and CI skeleton.
- Added secure Flask-session registration and login for administrator, enterprise, and domestic roles.
- Added role-prefixed IDs, bcrypt password hashes, inline validation, role guards, and logout.
- Test result: `12 passed, 0 failed` using isolated SQLite test configuration.
- Live MySQL verification remains pending because no MySQL client or server was available in the environment.
- Key files: `app/`, `tests/test_auth.py`, `requirements.txt`, `.env.example`, `.github/workflows/tests.yml`.

## Update — 2026-11-23 PLAN-003
- Added the administrator dashboard, account search, activation/deactivation, and removal routes.
- Added administrator analytics, active/resolved alert, and system report views.
- Added Building, Room, Appliance, EnergyConsumption, EnergyLimit, Alert, Report, and AssignedTo models.
- Corrected login redirect routing to the administrator blueprint.
- Test result: `18 passed, 0 failed` across authentication and administrator suites.
- Key files: `app/admin.py`, `app/templates/administrator/`, `tests/test_administrator.py`.

---

## 1. Executive summary

<!-- One paragraph: overall health of the codebase. Is it deployable? What's the biggest risk? -->

VoltWise is a greenfield Flask application with a working setup skeleton, role authentication, administrator dashboard, and enterprise dashboard. Domestic dashboard and physical hardware integration remain for later feature plans.

The largest remaining setup risk is live MySQL validation. Authentication behavior is verified in an isolated SQLite test database, while production models use PyMySQL and are prepared for MySQL.

---

## 2. Source code inventory

<!-- List all significant files/modules with LOC and role. -->
<!-- Tip: run `find src/ -name '*.py' | xargs wc -l | sort -rn` to get LOC counts. -->

### Core files by size

| File | LOC | Role |
|---|---:|---|
| `app/__init__.py` | ~36 | Flask application factory and extension setup |
| `app/auth.py` | ~160 | Registration, login, logout, validation, and role guards |
| `app/models.py` | ~140 | Account and VoltWise data models |
| `app/admin.py` | ~100 | Administrator dashboard and account management |
| `app/main.py` | ~20 | Health route and role dashboard placeholders |

### Web / API layer

| Component | Count | Key files |
|---|---:|---|
| Services | 1 | Shared authentication and validation functions |
| Routes | 10+ | Authentication, administrator management, and role placeholders |
| Tests | 31 | Authentication, administrator, enterprise ownership/workflow, and migration cases |

---

## 3. Configuration audit

<!-- List actual config values, defaults, and any dangerous settings. -->

| Setting | Default | Source | Notes |
|---|---|---|---|
| `DATABASE_URL` | MySQL placeholder URL | Environment variable | Uses PyMySQL; no real credentials in source |
| `SECRET_KEY` | Development-only change value | Environment variable | Must be replaced for deployment |
| `TEST_DATABASE_URL` | In-memory SQLite | `.env.example` | Test override only; not the production target |
| `ESP32_PORT` | Empty | `.env.example` | Reserved for future hardware integration |

---

## 4. Test suite status

<!-- Run tests and record results. -->

| Suite | Passed | Failed | Skipped | Notes |
|---|---:|---:|---:|---|
| Authentication unit/integration | 12 | 0 | 0 | SQLite test database |
| Administrator unit/integration | 6 | 0 | 0 | SQLite test database |
| Enterprise unit/integration | 12 | 0 | 0 | SQLite test database |
| Migration unit | 1 | 0 | 0 | In-memory SQLite test |
| Live MySQL integration | — | — | 1 | MySQL server/client unavailable |

---

## 5. Infrastructure & deployment

<!-- Docker images, CI pipelines, deployment targets. -->

| Component | Status | Notes |
|---|---|---|
| Local Flask runtime | Available | Application factory and health route |
| MySQL | Pending | User must configure `DATABASE_URL` and create a database |
| CI pipeline | Skeleton | GitHub Actions runs pytest on Python 3.12 |
| Docker Compose | Not created | Deferred |
| Production deploy | Not created | Deferred |

---

## 6. Known issues & technical debt

<!-- Bullet list of known problems. Reference plan numbers if fixes are planned. -->

- Live MySQL startup and migration behavior has not been verified.
- Email uniqueness is enforced per role in both ORM and a unique database constraint.
- Domestic dashboard implementation remains pending.
- Hardware integration and database records page remain pending.
- Electricity bill estimates use the configured `ELECTRICITY_RATE_PER_KWH`; default is zero until a tariff is configured.
