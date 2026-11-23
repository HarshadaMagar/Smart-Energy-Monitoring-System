# PLAN-004: Enterprise Dashboard

**Created:** 2026-11-23
**Status:** Completed
**Addresses:** Implement enterprise building, room, appliance, monitoring, billing, limit, alert, and report workflows.

---

## 1. Context & motivation

Feature 3 requires Enterprise Users to manage a building hierarchy and monitor its electrical assets. It depends on secure role authentication from PLAN-002, the MySQL data model, and a common consumption-reading and bill-calculation approach.

Every enterprise query must be restricted to the authenticated enterprise user's owned buildings. Cross-organization access is prohibited even if IDs are known.

---

## 2. Goals

- **G1:** Authenticated enterprise users have a cyan-themed dashboard and navigation.
- **G2:** Enterprise users can create and manage buildings, floors, rooms, and appliances.
- **G3:** Enterprise dashboards show building, floor, room, appliance, consumption, power, bill, and alert totals.
- **G4:** Live monitoring exposes voltage, current, power, energy, and simulated/real source status.
- **G5:** Daily/monthly limits and limit-vs-actual values are recalculated from stored readings.
- **G6:** Enterprise users receive high-consumption, limit, and appliance-status alerts.
- **G7:** Enterprise users can view role-owned daily, weekly, monthly, and asset-wise reports.
- **G8:** Enterprise users cannot view or mutate another organization's data.

---

## 3. Non-goals

- Administrator and domestic dashboard implementations.
- Real ESP32/PZEM-004T hardware communication in this plan.
- Future Wi-Fi protocol implementation.
- Bill tariff discovery or final tariff-source selection.
- Cross-enterprise analytics.
- External report exports unless the specification later requires them.

---

## 4. Approach

Implement an enterprise blueprint behind the `enterprise` role guard. Use server-owned enterprise-user IDs for every building query and transaction. Separate hierarchy CRUD, reading aggregation, billing, limits, alerts, and reports into bounded service modules only if multiple routes need the same logic.

For initial implementation, use simulated readings unless Feature 5 is explicitly added. Monitoring must still model a source field so real readings can replace simulated readings later without changing the UI contract.

Alternatives considered:

- **Using user-provided organization IDs in every query:** Rejected because it allows ID tampering and cross-organization access.
- **Calculating totals only in JavaScript:** Rejected because browser totals cannot be authoritative and may be inconsistent.
- **Building one generic asset CRUD:** Rejected because buildings, rooms, and appliances have different required fields and relationship rules.

### 4.1 Ownership and hierarchy

1. Write enterprise ownership and unauthorized-access tests.
2. Implement building CRUD for the authenticated enterprise account.
3. Implement floor and room management under a building.
4. Implement appliance CRUD and status/rated-power fields.

### 4.2 Monitoring and readings

1. Write aggregate tests for overall and building/floor/room/appliance scopes.
2. Implement read and source indicators for voltage, current, power, and energy.
3. Add building-, floor-, room-, and appliance-level monitoring views.
4. Reconcile aggregate totals with underlying reading records.

### 4.3 Bills and limits

1. Write bill and unit-consumption tests using fixture readings and a temporary documented tariff input.
2. Implement daily and monthly room limit storage and comparisons.
3. Generate limit-exceeded records using deterministic threshold rules.
4. Implement bill-history views once stored consumption and tariff inputs are consistent.

### 4.4 Alerts and reports

1. Write tests for high consumption, limit exceeded, and appliance status alerts.
2. Implement active/resolved alert history.
3. Write report aggregation tests for daily, weekly, monthly, and asset scopes.
4. Implement role-owned report views.

### 4.5 UI and chart layout

1. Apply the cyan enterprise theme to the existing full-black card system.
2. Add compact chart cards for room energy, seven-day consumption, limit-vs-actual, and building consumption.
3. Use 220–260px desktop and 180–220px mobile chart areas.
4. Add internal overflow scrolling and accessible axes/tooltips.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Write enterprise ownership and cross-organization access tests | 1 hr | PLAN-002 |
| 2 | Implement enterprise-owned building CRUD | 2 hr | 1 |
| 3 | Implement floor and room management | 2 hr | 2 |
| 4 | Implement appliance CRUD and status fields | 2 hr | 3 |
| 5 | Write reading and hierarchy aggregate tests | 1 hr | 3, 4 |
| 6 | Implement overall and asset-level monitoring views | 3 hr | 5 |
| 7 | Implement source-labelled reading display and history | 2 hr | 6 |
| 8 | Write consumption and bill calculation tests | 1 hr | 5 |
| 9 | Implement bill units, totals, and monthly history | 3 hr | 8 |
| 10 | Write room limit and threshold tests | 1 hr | 5 |
| 11 | Implement daily/monthly room limits and comparisons | 2 hr | 10 |
| 12 | Implement high-consumption, limit, and appliance alerts | 2 hr | 11 |
| 13 | Write and implement enterprise report aggregations | 2 hr | 8, 12 |
| 14 | Add enterprise charts and compact responsive layouts | 3 hr | 6, 9, 11 |
| 15 | Run integration tests and update the current state report | 1 hr | 12, 13, 14 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Cross-enterprise data access | Medium | Critical | Derive ownership from the session account and test direct object-ID access |
| Inconsistent consumption or bill aggregates | Medium | High | Centralize reading aggregation and fixture-based reconciliation tests |
| Bill formula is unspecified | Medium | High | Keep tariff input configurable only in data/configuration, and defer final tariff rules as a stated unknown |
| Simulated readings cannot be distinguished from real readings | Low | High | Add and test an explicit source field before monitoring UI |
| Limit alerts recur repeatedly | Medium | Medium | Store alert state and resolution conditions; test repeated readings |
| Hierarchy operations leave orphaned assets | Medium | High | Use transactions and foreign-key-safe delete behavior |

---

## 7. Success criteria

- [ ] G1 is verified by enterprise role authorization and cyan dashboard tests.
- [ ] G2 is verified by building, floor, room, and appliance CRUD tests.
- [ ] G3 is verified by seeded summary-card reconciliation.
- [ ] G4 is verified by voltage, current, power, energy, and source display tests.
- [ ] G5 is verified by limit-vs-actual and room-limit tests.
- [ ] G6 is verified by alert generation and active/resolved history tests.
- [ ] G7 is verified by daily, weekly, monthly, and asset report fixture tests.
- [ ] G8 is verified by cross-organization access tests returning redirect or HTTP 403.
- [ ] The complete enterprise test suite passes.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 3, chart requirements, UI palette, and data model
- `AGENT_MD/plan/plans/PLAN-002_role_authentication.md` — Enterprise authorization dependency
- `AGENT_MD/plan/rules.md` — Plan structure and test-first rules
- `AGENT_MD/plan/current_state_report.md` — Current implementation baseline
