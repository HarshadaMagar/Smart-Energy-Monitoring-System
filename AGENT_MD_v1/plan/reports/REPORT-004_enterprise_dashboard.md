# REPORT-004: Enterprise Dashboard

**Plan:** PLAN-004
**Completed:** 2026-11-23
**Author:** Copilot SDK in VS Code

---

## 1. Summary

PLAN-004 implemented the enterprise dashboard and role-owned workflows for building, room, and appliance management; energy monitoring; room limits; alerts; and reports. All enterprise queries scope records to the authenticated enterprise account. The full test suite passes with 31 tests.

---

## 2. Goals vs. actuals

| Goal (from plan) | Outcome | Evidence |
|---|---|---|
| **G1:** Cyan enterprise dashboard and navigation | ✅ Met | `app/templates/enterprise/dashboard.html` provides responsive enterprise navigation and summary cards |
| **G2:** Building, floor, room, and appliance workflows | ✅ Met | Create, update, and dependency-safe delete routes for buildings, rooms, and appliances |
| **G3:** Database-backed summary totals | ✅ Met | Dashboard queries account-owned buildings, floors, rooms, appliances, readings, and alerts |
| **G4:** Monitoring measurements and source status | ✅ Met | Appliance history and monitoring table display voltage, current, power, energy, and reading source |
| **G5:** Daily/monthly room limits and comparisons | ✅ Met | Daily/monthly limit management and actual usage comparison |
| **G6:** High-consumption, limit, and appliance-status alerts | ✅ Met | Limit checks create de-duplicated high-consumption/limit alerts; offline alerts resolve when appliances return online |
| **G7:** Role-owned reports | ✅ Met | Daily, weekly, monthly, and asset-wise report summaries are generated and account-scoped |
| **G8:** Organization data isolation | ✅ Met | Cross-organization reads and mutations are denied; reports are filtered by owner |

---

## 3. Changes made

### 3.1 Enterprise application

- `app/enterprise.py` — added ownership-scoped dashboard, hierarchy CRUD, monitoring, status, limit, alert, and report routes.
- `app/main.py` — removed the generic enterprise dashboard route in favor of the enterprise blueprint.
- `app/__init__.py` — registered the enterprise blueprint and configured the electricity rate.
- `app/auth.py` — routes enterprise login to the enterprise dashboard.
- `app/models.py` — added model relationships and report summaries; added uniqueness for room energy limits.

### 3.2 Enterprise interface

- `app/templates/enterprise/dashboard.html` — cyan summary cards, building list, and compact responsive consumption charts.
- `app/templates/enterprise/buildings.html` — building creation and account-owned building list.
- `app/templates/enterprise/building_detail.html` — building, room, appliance, and limit workflows.
- `app/templates/enterprise/appliance_detail.html` — appliance details, status, and sensor reading history.
- `app/templates/enterprise/monitoring.html` — building/floor/room/appliance readings.
- `app/templates/enterprise/alerts.html` — active and resolved enterprise alerts.
- `app/templates/enterprise/reports.html` — report generation and owned report history.
- `app/static/css/app.css` — cyan enterprise styling, compact chart sizing, responsive forms, and scrollable tables.

### 3.3 Migration and setup

- `migrations/upgrade.py` — added an idempotent migration for the report summary field.
- `tests/test_migrations.py` — verifies the migration is safe to run repeatedly.
- `README_SETUP.md` — documented migration and electricity tariff configuration.
- `.env.example` — added `ELECTRICITY_RATE_PER_KWH`.

### 3.4 Tests

- `tests/test_enterprise.py` — covers enterprise access, ownership, hierarchy CRUD, monitoring, limits, alerts, and reports.

---

## 4. Testing & validation

```text
python -m compileall -q app tests
python -m pytest tests -q
31 passed, 0 failed
```

The existing local SQLite database was upgraded with:

```text
python -m migrations.upgrade
Database schema is up to date.
```

Live MySQL integration remains unverified because no MySQL server was available.

---

## 5. Known issues & follow-ups

- The electricity tariff is not specified; `ELECTRICITY_RATE_PER_KWH` defaults to `0` until configured.
- The physical PZEM-004T integration should confirm whether sensor energy values are interval or cumulative.
- Charts use compact CSS bar visuals rather than Chart.js datasets; wire Chart.js when analytics chart behavior is implemented.
- Real hardware transport and automatic reading ingestion remain part of Feature 5.
- The development server requires a secure secret key and production WSGI server before deployment.

---

## 6. Metrics

| Metric | Before PLAN-004 | After PLAN-004 |
|---|---:|---:|
| Enterprise-focused tests | 0 | 12 |
| Total passing tests | 18 | 31 |
| Enterprise route handlers | 0 | 18 |
| Enterprise templates | 0 | 7 |
| Cross-organization access tests | 0 | 2 |

---

## 7. Lessons learned

- Resolve every enterprise-owned resource through the authenticated account before reading or mutating it.
- Dependency-safe deletion protects historical readings and room assignments from accidental loss.
- Tariff and sensor reading semantics should remain explicit configuration/domain decisions rather than hidden assumptions.
