# VoltWise — Project Specification

> **Version:** 1.0
> **Created:** 2026-11-23
> **Last Updated:** 2026-11-23
> **Status:** In Planning
>
> Living document — the AI agent updates **Codebase Inventory**, **Decision Log**, and **Current Focus**
> at the end of every working session. Do not edit those sections manually.

---

## Current Focus

- Spec v1.0 created from the VoltWise project requirements. Implementation has not started.

---

## Critical Pre-Work

- [ ] Establish the Python/Flask and MySQL development environment.
- [x] Configure environment variables and remove all secrets from source control.
- [x] Define and pin dependency versions for Flask, MySQL support, authentication, chart delivery, and testing.
- [x] Create the initial source, test, static asset, template, migration, and configuration structure.
- [ ] Confirm which MySQL instance and credentials are available for local and test environments.

---

## Project Overview

VoltWise is a web-based Smart Energy Management System for monitoring, managing, and analysing electricity consumption at domestic and enterprise levels. It gives users visibility of appliance-level readings, estimated electricity bills, energy limits, alerts, reports, and role-specific usage analytics.

The initial implementation is a greenfield Python Flask application using MySQL, HTML, CSS, JavaScript, Chart.js, and ESP32/PZEM-004T hardware integration. It supports simulated readings until connected hardware is available and must explicitly distinguish simulated data from real sensor readings.

### Problem Statement

Consumers and organisations lack a single accessible system that combines real-time appliance monitoring, cost estimation, consumption limits, alerts, and role-specific reporting. VoltWise provides those capabilities through three distinct role-based experiences.

### Target Users

- **System Administrators** monitor the whole system, manage domestic and enterprise accounts, view cross-user analytics, and review system-wide alerts and reports.
- **Enterprise Users** manage buildings, floors, rooms, appliances, limits, bills, alerts, and reports across an organisation.
- **Domestic Users** monitor assigned rooms and appliances, consumption, estimated bills, allowances, alerts, and personal reports.

### Current Operational Reality

The project is in planning. No application source code or deployed system is present; this specification and the supporting AGENT_MD framework are the current artifacts.

---

## Success Criteria

- [ ] All three roles can register, log in, switch roles, and access only their authorised pages.
- [ ] The system creates, queries, updates, and deletes the required MySQL entities with enforced relationships and constraints.
- [ ] Administrators, enterprise users, and domestic users can complete their role-specific dashboard workflows end to end.
- [ ] Live views display voltage, current, power, and energy readings with a clear simulated or real source indicator.
- [ ] Bill estimates, limits, alerts, charts, and reports use consistent stored data and role-specific permissions.
- [ ] The responsive interface follows the black visual theme, role accent, compact chart, focus, and reduced-motion requirements.
- [ ] Automated tests cover authentication, authorization, database relationships, limits, bill calculations, and core dashboards.

---

## Constraints and Non-Negotiables

- **Team:** Small project team; no team-size limit is specified.
- **Timeline:** No fixed delivery date is specified.
- **Budget:** No budget limit is specified.
- **Compliance:** No specific compliance framework is specified.
- **Non-negotiables:**
  - Full-black premium UI with the required role-specific accents.
  - Responsive mobile-first design.
  - Flask backend, MySQL database, Chart.js charts, and bcrypt password hashing.
  - Readable, accessible text and visible 3px focus rings.
  - Simulated readings until real hardware is connected.
  - Architecture must support multiple appliances and future Wi-Fi communication.

---

## Tech Stack

### Current

| Layer | Technology | Notes |
|---|---|---|
| Language | — | Greenfield; Python target |
| Framework | — | Greenfield; Python Flask target |
| Database | — | Greenfield; MySQL target |
| Frontend | — | Greenfield; HTML, CSS, and JavaScript target |
| Authentication | — | Greenfield; secure Flask sessions or JWT |
| Password hashing | — | bcrypt |
| Charts | — | Chart.js |
| Hardware | — | ESP32 and PZEM-004T |
| Testing | — | To be selected as part of setup |
| Containerisation | — | Not specified |
| CI/CD | — | To be configured |

### Target

| Layer | Technology | Notes |
|---|---|---|
| Language | Python | Flask application and hardware bridge |
| Framework | Flask | Server-rendered or API-backed web application |
| Database | MySQL | Relational data store |
| Frontend | HTML, CSS, JavaScript | Responsive role dashboards |
| Authentication | Secure Flask sessions / JWT | Choose one consistently for the implementation |
| Password hashing | bcrypt | Store hashes only |
| Charts | Chart.js | Compact dark-theme chart cards |
| Hardware | ESP32 + PZEM-004T | USB testing initially; Wi-Fi expansion later |

---

## Architectural Principles

- **Frontend/backend separation:** Keep browser assets and Jinja views in `frontend/`; keep Flask application code, database models, migrations, configuration, and tests in `backend/`.
- **MVC organization:** Use Jinja templates as Views, Flask blueprints and routes as Controllers, and SQLAlchemy entities as Models.
- **Separation of concerns:** Controllers handle HTTP concerns and delegate reusable business logic to `backend/app/services/`.
- **Organized modules:** Models belong in `backend/app/models/`, controllers in `backend/app/controllers/`, and services in `backend/app/services/`.
- **Role isolation:** Every protected route and data query must enforce administrator, enterprise, or domestic access.
- **Database-primary:** MySQL is authoritative for accounts, buildings, rooms, appliances, readings, limits, alerts, and reports.
- **Password safety:** Never store or log plaintext passwords; use bcrypt hashes exclusively.
- **Secure configuration:** Store credentials and environment-specific settings outside source control.
- **Sensor abstraction:** Separate simulated and real sensor providers behind a common reading interface.
- **API and server boundaries:** Keep authorization and validation server-side; frontend code must not be trusted as a security boundary.
- **Responsive UI:** Implement mobile-first layouts that remain compact and usable on small screens.
- **TDD:** Write focused tests before implementation and cover authentication, authorization, calculations, and data relationships.
- **Traceability:** Use plans and reports with matching serial numbers for implementation work.

```text
Smart Energy project/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── utils/
│   │   └── extensions.py
│   ├── migrations/
│   ├── tests/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── run.py
│   └── .env.example
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth.html
│   │   ├── administrator/
│   │   ├── enterprise/
│   │   └── domestic/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── .github/
├── run.py
├── README_SETUP.md
└── .gitignore
```

### MVC Mapping

| MVC component | Location | Responsibility |
|---|---|---|
| Model | `backend/app/models/` | SQLAlchemy entities, relationships, constraints, and data behavior |
| View | `frontend/templates/` and `frontend/static/` | Jinja output plus HTML, CSS, and JavaScript presentation |
| Controller | `backend/app/controllers/` | Flask blueprints, routes, request validation, authorization, and responses |
| Service | `backend/app/services/` | Reusable authentication, reporting, energy, alert, and billing business logic |

---

## Data Model

The MySQL database must include:

| Table | Purpose |
|---|---|
| SYSTEM_ADMINISTRATOR | Administrator account information |
| ENTERPRISE_USER | Enterprise account information |
| DOMESTIC_USER | Domestic account information |
| BUILDING | Enterprise building information |
| ROOM | Room and floor information |
| APPLIANCE | Individual appliance information |
| ENERGY_CONSUMPTION | Voltage, current, power, energy, timestamp, and reading source |
| ENERGY_LIMIT | Daily or monthly consumption limits |
| ALERT | Energy and appliance alerts |
| REPORT | Role-owned generated reports |
| ASSIGNED_TO | Composite-key assignment of domestic users to rooms |

Use primary keys, foreign keys, generated IDs, indexes, nullability rules, and appropriate constraints.

- Administrator IDs use `ADM-`.
- Enterprise user IDs use `ENT-`.
- Domestic user IDs use `DOM-`.
- Passwords are stored only as bcrypt hashes.
- Floors are grouped through building ID and floor number in `ROOM`.
- Alert recipients must reflect the correct account role.
- Reports must belong to the correct enterprise or domestic user, or to system-wide administrator scope.

---

## UI and Branding

The application uses a premium, modern, full-black theme.

| Element | Colour |
|---|---|
| Page background | `#000000` |
| Card background | `#0E1114` |
| Input background | `#14181C` |
| Borders | `#252C33` |
| Main text | `#F4F7F8` |
| Muted text | `#A3AEB8` |
| Error | `#FF8A80` |
| Success | `#5EEAA0` |

| Role | Accent |
|---|---|
| Administrator | Orange `#FF9F1C` |
| Enterprise | Cyan `#22D3EE` |
| Domestic | Green `#34D399` |

Required design elements:

- VoltWise hexagon and lightning-bolt SVG logo.
- Manrope font with weights 400–800.
- Monospace styling for database column names.
- 20–24px rounded cards.
- Soft role accent glows and subtle hover animations.
- Inline SVG or Lucide-style icons; no emoji icons.
- Responsive mobile-first layout.
- Visible 3px keyboard focus rings.
- Accessible text contrast.
- Reduced-motion support.
- Gradient page titles using orange, cyan, and green.

### Compact Chart Requirements

All charts must be in separate, rounded cards:

| Device | Chart height |
|---|---|
| Desktop | 220–260px |
| Mobile | 180–220px |

- Use two-column chart layouts on desktop and one-column layouts on mobile.
- Use dark chart styling and role-specific accent colours.
- Keep titles, labels, legends, tooltips, and axes compact and readable.
- Use internal horizontal scrolling for wide content instead of expanding the dashboard.
- Prevent chart containers from expanding to full-screen or excessive height.

Required charts:

| Dashboard | Charts |
|---|---|
| Administrator | Weekly sign-ups, domestic vs enterprise consumption, bill comparison, monthly energy trends |
| Enterprise | Energy by room, 7-day consumption, limit vs actual, building-wise consumption |
| Domestic | Daily consumption, monthly consumption, appliance-wise usage, limit progress |

---

## Codebase Inventory

| File | Role | Status | Last Updated |
|---|---|---|---|
| `AGENT_MD/spec.md` | Living project specification | Active | 2026-11-23 |
| `AGENT_MD/spec_init.md` | Project spec initializer | Active | 2026-11-23 |
| `AGENT_MD/plan/rules.md` | AI agent authoring conventions | Active | 2026-11-23 |
| `backend/app/` | Flask MVC application source, database models, and extensions | In progress | 2026-11-23 |
| `backend/app/controllers/` | Flask route and controller modules | Planned | 2026-11-23 |
| `backend/app/models/` | SQLAlchemy model modules | Planned | 2026-11-23 |
| `backend/app/services/` | Reusable business logic | Planned | 2026-11-23 |
| `backend/migrations/` | Database schema migrations | In progress | 2026-11-23 |
| `backend/tests/` | Authentication, authorization, integration, and migration tests | In progress | 2026-11-23 |
| `frontend/templates/` | Jinja HTML Views | In progress | 2026-11-23 |
| `frontend/static/` | Browser CSS and JavaScript assets | In progress | 2026-11-23 |

---

## Feature Index

| # | Feature | Status | Priority | Notes |
|---|---|---|---|---|
| 0 | Pre-Work: Setup and Security | ✅ | P0 | Environment, secrets, dependencies, repository structure; live MySQL verification pending |
| 1 | Role Registration and Authentication | ✅ | P0 | Role selection, validation, bcrypt, secure session authorization |
| 2 | System Administrator Dashboard | ✅ | P0 | System cards, account management, analytics, alerts, and reports |
| 3 | Enterprise Dashboard | ✅ | P0 | Buildings, rooms, appliances, monitoring, bills, limits |
| 4 | Domestic Dashboard | [ ] | P0 | Assigned rooms, appliances, monitoring, bills, limits |
| 5 | Energy and Hardware Integration | [ ] | P0 | Simulated and real PZEM-004T/ESP32 readings |
| 6 | MySQL Data and Relationships | [ ] | P0 | Required tables, constraints, IDs, indexes |
| 7 | Alerts and Reports | [ ] | P1 | Active/resolved alerts and role-owned reports |
| 8 | Charts and Analytics | [ ] | P1 | Compact Chart.js dashboards for all roles |
| 9 | Database Records Page | [ ] | P1 | Header counter and searchable account tabs |
| 10 | Responsive UI and Accessibility | [ ] | P1 | Branding, keyboard focus, contrast, reduced motion |

---

## Known Issues and Technical Debt

- Authentication mechanism is not yet finalized between secure Flask sessions and JWT.
- MySQL connection details and deployment environment are not known.
- Hardware communication protocol and ESP32 data format are not specified beyond USB-connected PZEM-004T testing.
- Electricity tariff/rate sources and bill formulas are not specified.
- Existing source code and database schema do not yet exist.

---

## Known Unknowns

- The preferred local and production MySQL setup.
- The exact implementation date range for enterprise and domestic bill history.
- Whether administrators can create administrator accounts through the UI or only manage existing accounts.
- Whether enterprise or domestic accounts are reviewed or approved before activation.
- The final ESP32 serial/USB and future Wi-Fi message format.

---

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| 2026-11-23 | Created v1.0 VoltWise specification | Greenfield project requirements are sufficient for implementation planning | Continue as placeholders; rejected because the source requirements are complete |

---

# FEATURE 0 — Pre-Work: Setup and Security

## Goal

Establish a clean, secure Flask/MySQL foundation before feature implementation.

## Tasks

- [ ] Initialise source control and a project-specific `.gitignore`.
- [ ] Add `.env` and `.env.example` for database, secret, and hardware configuration.
- [ ] Audit, pin, and document critical dependencies.
- [ ] Create application, test, template, static asset, migration, and configuration directories.
- [ ] Configure a CI or test command that runs the automated suite.

## Verification

- No credential or environment secret exists in tracked files or git history.
- The application can start against a configured test database.
- Dependency installation from the documented setup instructions is reproducible.
- CI or the project test command passes on a clean checkout.

---

# FEATURE 1 — Role Registration and Authentication

## Goal

Provide secure role selection, account creation, login, and role-based access protection for administrators, enterprise users, and domestic users.

## Existing Code to Reference

- None yet; this is the initial implementation feature.

## Tasks

- [ ] Create a three-card role-selection screen for administrator, enterprise, and domestic roles.
- [ ] Implement administrator fields: admin ID, name, email, password, and contact number.
- [ ] Implement enterprise fields: enterprise ID, name, email, password, contact number, organization name, and organization type.
- [ ] Implement domestic fields: domestic ID, name, email, password, and contact number.
- [ ] Generate role-prefixed IDs and prevent duplicate email addresses within each role.
- [ ] Add login/create-account switching, role change, and show/hide password controls.
- [ ] Validate email format, at least seven digits in contact numbers, and at least eight password characters.
- [ ] Hash passwords with bcrypt and display inline validation or success messages.
- [ ] Implement secure sessions or JWT and reject access to unauthorized role dashboards.

## Acceptance Criteria

- [ ] A new account of each role can be created and cannot reuse an email already stored for that role.
- [ ] Invalid email, contact number, and password values remain blocked with inline errors.
- [ ] Passwords are never stored or exposed in plaintext.
- [ ] Login requires valid credentials and the selected role.
- [ ] A logged-in user receives 403 or redirect behavior when attempting another role's protected routes.
- [ ] Show/hide password and role-change controls work without losing required form state unexpectedly.

---

# FEATURE 2 — System Administrator Dashboard

## Goal

Give administrators system-wide account, asset, consumption, bill, alert, and reporting visibility.

## Existing Code to Reference

- None yet; implement only after authentication and the MySQL schema exist.

## Tasks

- [ ] Create an orange-themed administrator dashboard and navigation.
- [ ] Display totals for registered users, enterprise users, domestic users, buildings, appliances, energy consumption, estimated bills, and active alerts.
- [ ] Implement domestic account search, details, activation, deactivation, removal, rooms, appliances, consumption, and bills.
- [ ] Implement enterprise account search and organization management, buildings, rooms, appliances, activation, deactivation, and removal.
- [ ] Add domestic, enterprise, and combined analytics.
- [ ] Display active/resolved alerts and system-wide reports.
- [ ] Add weekly sign-up analytics.

## Acceptance Criteria

- [ ] Every dashboard card reflects the current database state.
- [ ] Account activation, deactivation, removal, and search actions work with clear success or failure feedback.
- [ ] Administrator views cannot expose credentials or inactive account data unexpectedly.
- [ ] Domestic-vs-enterprise consumption and bill comparisons use the same calculation rules.

---

# FEATURE 3 — Enterprise Dashboard

## Goal

Enable enterprise users to manage buildings and rooms, monitor appliances, estimate bills, set limits, receive alerts, and generate reports.

## Existing Code to Reference

- None yet; implement after authentication and data ownership authorization exist.

## Tasks

- [ ] Create a cyan-themed enterprise dashboard and navigation.
- [ ] Display building, floor, room, appliance, daily consumption, current power, bill, and active-alert totals.
- [ ] Implement building, floor, room, and appliance CRUD workflows.
- [ ] Display appliance status, rated power, connection status, monitoring history, and individual appliance readings.
- [ ] Implement overall and building/floor/room/appliance live monitoring views.
- [ ] Show unit consumption and estimated bills with building, floor, room, and monthly history views.
- [ ] Add room-wise daily or monthly limits and limit-vs-actual comparisons.
- [ ] Implement high-consumption, limit, and appliance-status alerts.
- [ ] Implement daily, weekly, monthly, and asset-wise reports.

## Acceptance Criteria

- [ ] An enterprise user can create a building hierarchy and manage its rooms and appliances.
- [ ] Monitoring views show voltage, current, power, energy, and source status.
- [ ] Bill totals and room/building/appliance totals reconcile with underlying consumption records.
- [ ] Exceeding a configured limit creates an alert and updates the limit comparison.
- [ ] Enterprise users cannot view or modify another organization's data.

---

# FEATURE 4 — Domestic Dashboard

## Goal

Give domestic users assigned-room monitoring, limit tracking, bills, alerts, and personal reports.

## Existing Code to Reference

- None yet; implement after authentication and assigned-room authorization exist.

## Tasks

- [ ] Create a green-themed domestic dashboard and navigation.
- [ ] Display room, appliance, appliance-on, daily consumption, current power, bill, and limit-usage totals.
- [ ] Show assigned rooms and appliances and allow appliance creation where permitted.
- [ ] Implement individual appliance monitoring and consumption history.
- [ ] Display live voltage, current, power, energy, and chart values.
- [ ] Show units consumed, unit rate, estimated bill, daily/monthly consumption, and monthly history.
- [ ] Track assigned limits, consumed energy, remaining allowance, and percentage used.
- [ ] Turn the limit progress indicator red above 90% usage.
- [ ] Implement domestic high-consumption, limit, and appliance-status alerts and reports.

## Acceptance Criteria

- [ ] A domestic user sees only assigned rooms and permitted appliances.
- [ ] Appliance status and current readings update in real time or by the same refresh mechanism used across dashboards.
- [ ] Bill and unit totals reconcile with stored readings.
- [ ] Limit progress reaches and reflects 90% as an error state.
- [ ] Domestic reports cover daily, weekly, monthly, appliance-wise, and bill data.

---

# FEATURE 5 — Energy and Hardware Integration

## Goal

Support reliable sensor readings and preserve a clear distinction between simulated and real PZEM-004T/ESP32 data.

## Existing Code to Reference

- None yet; sensor integration can follow a provider abstraction.

## Tasks

- [ ] Support one appliance using a USB-connected ESP32 for initial testing.
- [ ] Implement a PZEM-004T reading provider for voltage, current, power, and energy.
- [ ] Implement a simulated-reading provider until real hardware is connected.
- [ ] Store a source indicator and timestamp for every reading.
- [ ] Surface simulated/real status in monitoring and history views.
- [ ] Design the provider interface for multiple appliances and future Wi-Fi communication.

## Acceptance Criteria

- [ ] Simulated readings work without hardware and are labelled as simulated.
- [ ] Real readings are parsed, timestamped, stored, and labelled as real.
- [ ] Invalid, disconnected, or out-of-range sensor values are handled without corrupting totals.
- [ ] One USB appliance can be monitored end to end and the architecture can represent additional devices.

---

# FEATURE 6 — MySQL Data and Relationships

## Goal

Provide a normalized, constrained MySQL schema that supports every role and feature.

## Existing Code to Reference

- None yet; define migrations or schema setup before feature implementation.

## Tasks

- [ ] Create all required tables and role-specific foreign keys.
- [ ] Add generated IDs, indexes, composite assignment keys, and uniqueness constraints.
- [ ] Add reading source, timestamp, and measurement fields.
- [ ] Add role ownership relationships for alerts and reports.
- [ ] Implement activation/deactivation and account removal behavior safely.
- [ ] Create test fixtures and reset helpers for isolated database tests.

## Acceptance Criteria

- [ ] The schema satisfies the required entity and relationship list.
- [ ] Invalid foreign keys and duplicate role-prefixed IDs or emails are rejected.
- [ ] `ASSIGNED_TO` uses an appropriate composite primary key.
- [ ] Removing a parent account or asset does not create silent orphan records.
- [ ] Database tests pass for constraints and role ownership.

---

# FEATURE 7 — Alerts and Reports

## Goal

Generate actionable role-specific alerts and reports from stored readings and configuration.

## Existing Code to Reference

- None yet.

## Tasks

- [ ] Implement high-consumption alerts.
- [ ] Implement energy-limit alerts for enterprise rooms and domestic allowances.
- [ ] Implement appliance status alerts.
- [ ] Separate active and resolved alert history.
- [ ] Implement role-owned daily, weekly, monthly, asset-wise, and system-wide reports.
- [ ] Preserve report ownership and generation timestamps.

## Acceptance Criteria

- [ ] Alerts are generated only once according to an agreed threshold and resolution rule.
- [ ] Active and resolved alerts can be reviewed by the authorized role.
- [ ] Reports reconcile totals with underlying readings.
- [ ] Cross-role report access is denied.

---

# FEATURE 8 — Charts and Analytics

## Goal

Provide compact, responsive Chart.js visualizations for all role dashboards.

## Existing Code to Reference

- None yet.

## Tasks

- [ ] Add administrator sign-up, consumption, bill, and monthly trend charts.
- [ ] Add enterprise room, 7-day, limit-vs-actual, and building consumption charts.
- [ ] Add domestic daily, monthly, appliance usage, and limit progress charts.
- [ ] Apply dark chart styling and role accent colours.
- [ ] Implement desktop and mobile chart dimensions and layouts.
- [ ] Contain overflow and avoid dashboard page expansion.

## Acceptance Criteria

- [ ] Every required chart renders from database-backed data.
- [ ] Desktop charts use the specified 220–260px range and mobile charts use 180–220px.
- [ ] Charts fit two columns on desktop and one column on mobile.
- [ ] Wide chart content scrolls within its card.
- [ ] Labels and tooltips remain readable at supported viewport sizes.

---

# FEATURE 9 — Database Records Page

## Goal

Give authorized users a searchable view of role account records directly from the header.

## Existing Code to Reference

- None yet.

## Tasks

- [ ] Add a header Database button with a live account-record counter.
- [ ] Create a separate database page.
- [ ] Add SYSTEM_ADMINISTRATOR, ENTERPRISE_USER, and DOMESTIC_USER tabs.
- [ ] Render searchable, horizontally scrollable record tables.
- [ ] Hide password values and sensitive credentials.
- [ ] Restrict the database page to administrator authorization.

## Acceptance Criteria

- [ ] The record counter matches the combined or individually tabbed database counts.
- [ ] Tabs switch correctly and filter through search.
- [ ] Tables remain horizontally scrollable on small screens.
- [ ] Password hashes and unrelated sensitive credentials are not rendered.
- [ ] Non-administrators cannot access the page or its data endpoints.

---

# FEATURE 10 — Responsive UI and Accessibility

## Goal

Deliver the premium VoltWise interface consistently across roles and viewport sizes.

## Existing Code to Reference

- None yet.

## Tasks

- [ ] Implement the full-black background, card, input, border, text, success, and error palette.
- [ ] Implement administrator orange, enterprise cyan, and domestic green themes.
- [ ] Add the VoltWise SVG logo and inline SVG/Lucide-style icons.
- [ ] Load Manrope weights 400–800 and use monospace styling for database fields.
- [ ] Add 20–24px cards, soft glows, hover transitions, and gradient titles.
- [ ] Add 3px focus rings and accessible contrast.
- [ ] Implement reduced-motion behavior.
- [ ] Verify mobile navigation, tables, charts, forms, and dialogs.

## Acceptance Criteria

- [ ] Core workflows remain usable from mobile through desktop widths.
- [ ] Role themes and contrast meet the specified palettes.
- [ ] Keyboard focus is always visible on interactive elements.
- [ ] Reduced-motion preference disables or minimizes non-essential animation.
- [ ] No emoji icon is used in the interface.

---
