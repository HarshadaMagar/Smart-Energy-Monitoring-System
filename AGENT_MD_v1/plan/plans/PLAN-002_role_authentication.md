# PLAN-002: Role Registration and Authentication

**Created:** 2026-11-23
**Status:** Completed
**Addresses:** Implement secure role selection, account creation, login, bcrypt password storage, and role-based authorization for VoltWise.

---

## 1. Context & motivation

VoltWise Feature 1 requires three account types with distinct fields and dashboards. After PLAN-001 establishes the application and test baseline, authentication must protect subsequent building, appliance, reporting, and analytics features.

The greenfield baseline means account storage and authorization decisions must be made before other role-specific features reference users or ownership. This plan uses the feature specification in `AGENT_MD/spec.md` and applies test-first implementation.

---

## 2. Goals

- **G1:** A role-selection screen offers System Administrator, Enterprise User, and Domestic User registration flows.
- **G2:** Account creation collects every role-specific field in `spec.md`, including enterprise organization type.
- **G3:** Generated IDs use `ADM-`, `ENT-`, and `DOM-` prefixes.
- **G4:** Duplicate emails are blocked independently within each role.
- **G5:** Email, contact, password, required-field, and organization validations produce inline feedback.
- **G6:** Passwords are stored only as bcrypt hashes and are never serialized or logged.
- **G7:** Login, logout, role change, show/hide password, and protected-route behavior work securely.
- **G8:** Authentication, validation, and authorization tests pass before dashboard implementation begins.

---

## 3. Non-goals

- Administrator, enterprise, or domestic dashboard feature implementation.
- Building, room, appliance, reading, limit, alert, report, or chart implementation.
- Password recovery or email-verification workflows.
- Social login or external identity providers.
- Production secrets, deployment, or hardware integration.
- Any Feature 2–10 dashboard content beyond authorization boundaries.

---

## 4. Approach

Use a test-first MySQL-backed implementation with separate account tables and a shared server-side authentication service. Secure Flask sessions are the preferred mechanism because `spec.md` allows sessions or JWT but no requirement favors JWT. The implementation should document the selected mechanism and use it consistently.

Define the role explicitly on login and registration so access checks cannot rely on a user-controlled generic role. Store password hashes with bcrypt and remove password values from response payloads and database-record views.

### 4.1 Schema and account models

1. Define and test three role tables and role-prefixed ID rules.
2. Enforce duplicate-email prevention independently within each role.
3. Add administrator, enterprise, and domestic fields exactly as defined by the specification.
4. Include enterprise organization types: Corporate, Educational, Healthcare, Government, Industrial, Retail, and Other.
5. Add activation/deactivation fields because administrator management features depend on account status.

### 4.2 Registration and validation

1. Write registration tests for every role and invalid field combination.
2. Implement a three-card role-selection screen and role-specific registration forms.
3. Validate email format, at least seven digits in contact numbers, at least eight password characters, and required fields.
4. Hash passwords with bcrypt before persistence and prevent plaintext password output.
5. Add success and error feedback that can use the VoltWise success/error palette.

### 4.3 Login and authorization

1. Write tests for valid credentials, invalid credentials, inactive users, and wrong-role access.
2. Implement login and session or JWT issuance after the mechanism decision.
3. Add role-based route guards for administrator, enterprise, and domestic areas.
4. Implement logout and role-change navigation behavior.
5. Return redirect or HTTP 403 behavior consistently for unauthorized role routes.

### 4.4 UI behavior

1. Add login/create-account switching, change-role, and show/hide-password controls.
2. Apply the role accent themes and full-black UI only where this authentication feature requires it.
3. Add visible keyboard focus and accessible inline feedback.
4. Derive authorization server-side; never trust a form-submitted role as an authorization grant.

---

## 5. Task breakdown

| # | Task | Est. | Depends on |
|---|------|------|------------|
| 1 | Complete PLAN-001 setup and document the authentication mechanism choice | 30 min | PLAN-001 |
| 2 | Write account schema, ID, and per-role uniqueness tests | 1 hr | 1 |
| 3 | Implement role account migrations/models | 2 hr | 2 |
| 4 | Write role registration validation tests | 1 hr | 3 |
| 5 | Implement role registration and bcrypt hashing | 2 hr | 4 |
| 6 | Write login, inactive-account, logout, and wrong-role tests | 1 hr | 3 |
| 7 | Implement login and the selected authentication mechanism | 2 hr | 6 |
| 8 | Implement role guards and denied-route behavior | 1 hr | 7 |
| 9 | Write authentication-page and UI behavior tests | 1 hr | 5, 8 |
| 10 | Implement role selection, registration, and login UI | 2 hr | 9 |
| 11 | Run authentication integration tests and secret/logging checks | 1 hr | 10 |
| 12 | Update the current state report and Feature 1 status | 20 min | 11 |

---

## 6. Risks & mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Session/JWT choice creates inconsistent authorization | Medium | High | Make one mechanism explicit before route implementation and test it at each role boundary |
| Duplicate email checks differ across roles | Medium | Medium | Add per-role database constraints and explicit service-level validation |
| Password hashes appear in logs or responses | Low | High | Exclude password fields from serialization and test response bodies |
| Role supplied by a form bypasses server authorization | Medium | High | Derive authorization from the authenticated account and fixed role guards |
| Contact number validation rejects valid international formatting | Medium | Medium | Define the minimum seven-digit rule explicitly and strip only non-digit display formatting for validation |
| User activation state is omitted | Medium | Medium | Include tested active/deactivated fields from the initial schema |

---

## 7. Success criteria

- [ ] G1 is demonstrated by successful registration tests for all three roles.
- [ ] G2 is demonstrated by generated-ID tests.
- [ ] G3 is demonstrated by duplicate-email tests and database constraints.
- [ ] G4 is demonstrated by stored bcrypt hashes and plaintext-exclusion tests.
- [ ] G5 is demonstrated by role-specific validation tests.
- [ ] G6 is demonstrated by bcrypt hash storage and no plaintext-password output.
- [ ] G7 is demonstrated by login/logout, role-change, show/hide-password, and protected-route tests.
- [ ] G8 is demonstrated by a passing role-authentication test suite.

---

## 8. References

- `AGENT_MD/spec.md` — Feature 1 and Constraints
- `AGENT_MD/plan/plans/PLAN-001_pre_work_security.md` — Setup dependency
- `AGENT_MD/plan/rules.md` — Test-first and plan/report conventions
- `AGENT_MD/plan/current_state_report.md` — Baseline project state

