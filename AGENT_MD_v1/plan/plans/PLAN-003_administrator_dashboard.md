# PLAN-003: System Administrator Dashboard

**Created:** 2026-11-23
**Status:** Completed
**Addresses:** Implement the system-wide administrator dashboard, account management, analytics, alerts, and reporting views for VoltWise.

---

## 1. Context & motivation

Feature 2 requires a System Administrator to manage domestic and enterprise accounts and review system-wide operational data. The implementation depends on completed role authentication from PLAN-002 and the MySQL account and asset relationships defined in `AGENT_MD/spec.md`.

The administrator experience must remain server-authorized: account totals and all management actions must come from database-backed views, not client-side aggregates or role-state values.

---

## 2. Goals

- **G1:** Authenticated administrators have an orange-themed dashboard and navigation.
- **G2:** Every administrator dashboard card reports current database totals.
- **G3:** Administrators can search and manage domestic and enterprise account status.
- **G4:** Administrators can inspect domestic and enterprise rooms, appliances, consumption, and bills.
- **G5:** Domestic, enterprise, combined, and sign-up analytics display database-backed results.
- **G6:** Active and resolved system alerts and system reports are available to administrators only.
- **G7:** Administrator routes and mutations enforce authorization and never expose password hashes or unrelated secrets.

---

## 3. Non-goals

- Building, room, and appliance CRUD implementation for enterprise users.
- Domestic-user dashboard implementation.
- ESP32/PZEM-004T hardware communication.
- Report file generation or export formats not required by the specification.
- Public APIs or account self-service outside the administrator workflow.
- Changing electricity tariffs or bill formulas before they are specified.

---

## 4. Approach

Implement one server-side administrator blueprint and reusable database query functions. Complete feature tests before each production surface; use MySQL for integration data and isolated test data for route and authorization tests.

Dashboard cards use server queries or one bounded summary query, depending on data volume. Account management uses atomic transactions for activation, deactivation, and removal. Removal must use the relationship behavior defined by the schema rather than silently orphaning rooms or readings.

Alternatives considered:

- **Client-side-only account filtering:** Rejected because browser code cannot enforce authorization or provide an authoritative system record count.
- **A generic role dashboard:** Rejected because administrator, enterprise, and domestic workflows have different permissions and visual accents.
- **Deleting account records immediately:** Deferred to schema policy; account removal must account for protected relationships and avoid unintended reading deletion.

### 4.1 Dashboard shell and totals

1. Write route and authorization tests for the administrator page.
2. Create the orange navigation and dashboard card layout.
3. Query registered users, role totals, buildings, appliances, consumption, bills, and active alerts.
4. Add loading-safe empty states and accessible card labels.

### 4.2 Account management

1. Write tests for domestic and enterprise search and status mutations.
2. Implement paginated/searchable account lists.
3. Implement detail views for rooms, appliances, consumption, and bills.
4. Implement activation, deactivation, and removal with confirmation and success/error feedback.

### 4.3 Analytics, alerts, and reports

1. Write tests for domestic, enterprise, combined, and weekly sign-up datasets.
2. Define chart payload serializers server-side.
3. Implement active/resolved alert views.
4. Implement system-wide report queries and role-safe report pages.

### 4.4 UI and accessibility

1. Apply the orange role theme and VoltWise full-black card palette.
2. Keep required charts compact and responsive.
3. Provide visible focus rings, accessible table labels, and mobile table overflow.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Write administrator route and unauthorized-access tests | 1 hr | PLAN-002 |
| 2 | Add required MySQL/ORM account summary queries | 2 hr | 1 |
| 3 | Implement administrator dashboard shell and orange navigation | 2 hr | 2 |
| 4 | Write and implement dashboard card and empty-state tests | 1 hr | 2 |
| 5 | Write domestic and enterprise account search tests | 1 hr | 2 |
| 6 | Implement searchable account lists and detail views | 3 hr | 5 |
| 7 | Write account activation/deactivation/removal tests | 1 hr | 6 |
| 8 | Implement account status mutations and removal confirmation | 2 hr | 7 |
| 9 | Write analytics and chart-data tests | 1 hr | 2 |
| 10 | Implement domestic, enterprise, combined, and sign-up analytics | 3 hr | 9 |
| 11 | Write and implement system alert/report tests | 1 hr | 2 |
| 12 | Implement active/resolved alerts and system-wide reports | 2 hr | 11 |
| 13 | Add compact responsive charts and accessible tables | 3 hr | 3, 10 |
| 14 | Run integration tests and update the current state report | 1 hr | 8, 12, 13 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Account removal creates orphaned assets or readings | Medium | High | Confirm relationship policy; enforce transactions and foreign-key behavior before removal UI |
| Dashboard totals use inconsistent calculation rules | Medium | High | Centralize consumption and bill summary queries and test them against fixtures |
| Administrator routes leak password or inactive-account details | Low | High | Use explicit response models and test serialized fields |
| Large account lists degrade usability | Medium | Medium | Add search and pagination server-side |
| Chart values differ between cards and detail pages | Medium | Medium | Reuse summary serializers and reconciling fixtures |
| Analytics scope is ambiguous | Medium | Medium | Mark tariff-dependent totals as blocked until the bill formula is approved |

---

## 7. Success criteria

- [ ] G1 is verified by role authorization and orange dashboard tests.
- [ ] G2 is verified by dashboard totals that reconcile with seeded database fixtures.
- [ ] G3 is verified by domestic and enterprise account search/status tests.
- [ ] G4 is verified by account detail tests covering rooms, appliances, consumption, and bills.
- [ ] G5 is verified by domestic, enterprise, combined, and sign-up chart payload tests.
- [ ] G6 is verified by administrator-only alert/report route tests.
- [ ] G7 is verified by password-field exclusion and unauthorized-route checks.
- [ ] The complete administrator test suite passes.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 2, UI palette, chart requirements, and data model
- `AGENT_MD/plan/plans/PLAN-002_role_authentication.md` — Authentication dependency
- `AGENT_MD/plan/rules.md` — Plan structure and test-first rules
- `AGENT_MD/plan/current_state_report.md` — Current implementation baseline

