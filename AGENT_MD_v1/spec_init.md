# spec_init.md — Project Spec Initializer

> **Version:** 1.0
> **Purpose:** Run this once with any agentic AI to generate your project's `AGENT_MD/spec.md` from raw input.
>
> **Raw project input:** The VoltWise project requirements are included in the usage example below.
> **Usage:** `"Follow AGENT_MD/spec_init.md. My raw project idea is: [VoltWise is a web-based Smart Energy Management System designed to monitor, manage and analyze electricity consumption at both domestic and enterprise levels.

The system allows users to monitor individual electrical appliances, view real-time electricity consumption, calculate estimated electricity bills, set energy consumption limits, receive alerts and generate reports.

It supports three different user roles:
1. System Administrator
2. Enterprise User
3. Domestic User
Each role has a separate login flow, dashboard, navigation menu, permissions and role-specific accent colour.
2. Branding and UI design
Use a premium, modern, full-black theme.
Element	Colour
Page background	#000000
Card background	#0E1114
Input background	#14181C
Borders	#252C33
Main text	#F4F7F8
Muted text	#A3AEB8
Error	#FF8A80
Success	#5EEAA0

Role-specific colours:
- Administrator: Orange #FF9F1C
- Enterprise: Cyan #22D3EE
- Domestic: Green #34D399
Additional design requirements:
- VoltWise hexagon and lightning-bolt SVG logo.
- Manrope font, weights 400–800.
- Monospace font for database column names.
- Rounded cards with 20–24px radius.
- Soft accent glows and subtle hover animations.
- Lucide-style SVG icons, no emoji icons.
- Responsive mobile-first design.
- Visible 3px focus rings.
- Accessible text contrast.
- Reduced-motion support.
- Gradient title using orange, cyan and green.
3. User registration and login
Create a role-selection screen with three cards.

System Administrator
- Admin ID (automatically generated)
- Name
- Email
- Password
- Contact number
Enterprise User
- Enterprise User ID (automatically generated)
- Name
- Email
- Password
- Contact number
- Organization name
- Organization type
Organization types: Corporate, Educational, Healthcare, Government, Industrial, Retail and Other.

Domestic User
- Domestic User ID (automatically generated)
- Name
- Email
- Password
- Contact number
Login uses email and password after role selection.

Include:
- Login and create-account switching.
- Change role option.
- Show/hide password.
- Email validation.
- Minimum seven-digit contact number.
- Minimum eight-character password.
- Duplicate email prevention within each role.
- Inline validation and success messages.
- bcrypt password hashing.
- Secure authentication and role-based access protection.
4. System Administrator dashboard
Orange theme
Dashboard cards
- Total registered users.
- Total enterprise users.
- Total domestic users.
- Total buildings.
- Total appliances.
- Total energy consumption.
- Total estimated bills.
- Active alerts.
Pages and sections

1. Domestic User Management
- View all domestic users.
- Search and view user details.
- Activate, deactivate and remove users.
- View assigned rooms and appliances.
- View energy consumption and bills.
2. Enterprise User Management
- View all enterprise users.
- Search and manage organizations.
- View buildings, rooms and appliances.
- Activate, deactivate and remove accounts.
3. Domestic Analytics
- Domestic users.
- Connected appliances.
- Total electricity consumption.
- Total estimated bills.
4. Enterprise Analytics
- Enterprise users.
- Buildings, floors and rooms.
- Connected appliances.
- Total electricity consumption.
- Estimated bills.
5. Combined Analytics
- Domestic vs Enterprise consumption.
- Domestic vs Enterprise bills.
- Total energy consumption.
- Weekly and monthly trends.
6. Alerts and Reports
- View active and resolved alerts.
- View system-wide reports.
7. Sign-up Analytics
- Weekly registration chart.
5. Enterprise User dashboard
Cyan theme
Dashboard cards
- Total buildings.
- Total floors.
- Total rooms.
- Total appliances.
- Today's energy consumption (kWh).
- Current power usage (W).
- Estimated electricity bill.
- Active alerts.
Pages and sections

1. Building Management
- Add, edit and delete buildings.
- Building name, type and address.
- View individual building details.
2. Floor and Room Management
- Manage floors under each building.
- Add and manage multiple rooms.
- Room name, floor number and room type.
- View appliances in each room.
3. Appliance Management
- Add and manage appliances.
- Appliance name and type.
- Rated power.
- Connection status.
- Individual appliance monitoring page.
- Energy consumption history.
4. Live Monitoring
- Overall energy consumption.
- Building-wise consumption.
- Floor-wise consumption.
- Room-wise consumption.
- Individual appliance consumption.
- Voltage, current, power and energy readings.
5. Electricity Bill
- Total energy consumed.
- Building-wise bills.
- Floor-wise bills.
- Room-wise bills.
- Electricity rate per unit.
- Estimated total bill.
- Monthly bill history.
6. Energy Limits
- Set room-wise daily or monthly energy limits.
- Compare actual and permitted consumption.
- Generate alerts when limits are exceeded.
7. Alerts
- High consumption alerts.
- Energy limit alerts.
- Appliance status alerts.
- Active and resolved alert history.
8. Reports
- Daily, weekly and monthly reports.
- Building-wise reports.
- Room-wise reports.
- Appliance-wise reports.
- Total energy consumption and bill reports.
6. Domestic User dashboard
Green theme
Dashboard cards
- My rooms.
- Total connected appliances.
- Appliances currently ON.
- Today's energy consumption (kWh).
- Current power usage (W).
- Estimated electricity bill.
- Energy limit used percentage.
Pages and sections

1. My Rooms and Appliances
- View assigned rooms.
- View appliances inside each room.
- Add appliances where permitted.
- Open separate monitoring pages for each appliance.
- View appliance status and consumption history.
2. Live Monitoring
- Real-time electricity consumption.
- Voltage.
- Current.
- Power.
- Energy consumed.
- Live consumption charts.
3. Electricity Bill
- Total units consumed.
- Electricity rate per unit.
- Estimated bill amount.
- Daily and monthly consumption.
- Monthly bill history.
4. Energy Limits
- Assigned energy limit.
- Energy consumed.
- Remaining energy allowance.
- Percentage of limit used.
- Progress bar turns red above 90%.
5. Alerts
- High consumption alerts.
- Energy limit alerts.
- Appliance status alerts.
- Active and resolved alerts.
6. Reports
- Daily consumption report.
- Weekly consumption report.
- Monthly consumption report.
- Appliance-wise consumption.
- Estimated electricity bill report.
7. Charts and graphs – Compact scrollable design
Important UI requirement
All charts across all three dashboards must have a compact, small-box layout.

Chart dimensions
Device	Chart height
Desktop	220–260px
Mobile	180–220px

Chart design requirements
- Place every chart inside a separate rounded card.
- Never make charts excessively large or full-screen.
- Use two-column chart layouts on desktop.
- Use one-column chart layouts on mobile.
- Maintain consistent chart dimensions.
- Use dark chart styling with role-specific accent colours.
- Keep chart titles, labels and legends compact.
- Make chart containers responsive.
- Use internal horizontal scrolling for wide chart content.
- Prevent charts from expanding the entire dashboard.
- Keep scrolling within the chart container wherever content exceeds its available area.
- Maintain readable axes and tooltips.
- Avoid unnecessary empty space.
Charts required
Dashboard	Charts
Administrator	Weekly sign-ups, Domestic vs Enterprise consumption, Bill comparison, Monthly energy trends
Enterprise	Energy by room, 7-day consumption, Limit vs actual, Building-wise consumption
Domestic	Daily consumption, Monthly consumption, Appliance-wise usage, Limit progress

8. Hardware integration
The system uses the following hardware:
- PZEM-004T energy sensor.
- ESP32 microcontroller.
- Electrical appliances.
- Laptop for initial testing.
Electrical Appliance

PZEM-004T Sensor

Voltage, Current, Power, Energy

ESP32

Python Flask Backend

MySQL Database

VoltWise Dashboard

Live monitoring, bills, alerts and reports


Initial development supports one appliance with USB-connected ESP32 testing. The architecture should support multiple appliances and future Wi-Fi-based communication.

Use simulated energy readings until the actual hardware is connected. Clearly identify simulated and real readings.
9. Database structure
Use MySQL and create these tables:
Table	Main purpose
SYSTEM_ADMINISTRATOR	Administrator information
ENTERPRISE_USER	Enterprise account information
DOMESTIC_USER	Domestic account information
BUILDING	Building information
ROOM	Room and floor information
APPLIANCE	Individual appliance information
ENERGY_CONSUMPTION	Sensor readings
ENERGY_LIMIT	Energy consumption limits
ALERT	Energy and appliance alerts
REPORT	Generated reports
ASSIGNED_TO	Domestic user-room assignments

Use primary keys, foreign keys, generated IDs, indexes and appropriate constraints.

IDs:
- ADM- for administrators.
- ENT- for enterprise users.
- DOM- for domestic users.
Use a composite primary key for ASSIGNED_TO.

Store passwords only as bcrypt hashes.

Group floors through building ID and floor number in ROOM, following the current ER diagram.

Implement suitable alert recipient relationships and ensure reports belong to the correct user role.
10. Database page
Add a Database button in the header with a record counter.

It should open a separate page with three tabs:
- SYSTEM_ADMINISTRATOR
- ENTERPRISE_USER
- DOMESTIC_USER
Each tab must show its respective database records in searchable and horizontally scrollable tables.
11. Technology stack
Component	Technology
Frontend	HTML, CSS, JavaScript
Backend	Python Flask
Database	MySQL
Authentication	Secure Flask sessions / JWT
Password hashing	bcrypt
Charts	Chart.js
Icons	Inline SVG / Lucide-style icons
Hardware	ESP32 + PZEM-004T]"`

---

## Your Role

You are a **technical project analyst**. Your job is to take whatever the user gives you — a brain dump, bullet points, a rough README, a voice transcript, a napkin idea — and transform it into a clean, structured `spec.md` (v1.0) that an AI agent can use as a living project document going forward.

You are thorough but efficient. You do not ask questions that were already answered. You do not generate the spec until you have enough information. You do not overwhelm the user — you ask in small, focused batches.

---

## Phase 1 — Intake

Read everything the user has provided. Accept any format:
- Free-form text
- Bullet points
- A rough README or old spec
- A transcript of spoken thoughts
- A mix of all of the above

Do not judge the quality or completeness of the input. Your job is to extract signal from it.

After reading, say:

> "Got it. I've read your input. Let me identify what I know and what I still need."

Then proceed to Phase 2.

---

## Phase 2 — Gap Detection

Silently evaluate the user's input against these **8 core categories**. For each category, mark it as ✅ Known, ⚠️ Partial, or ❓ Unknown.

| # | Category | What you need to know |
|---|---|---|
| 1 | **Purpose** | What problem does this solve? Why does it need to exist? |
| 2 | **Users** | Who uses it? What do they need? |
| 3 | **Core Features** | What are the must-have capabilities for v1? |
| 4 | **Tech Stack** | Language, framework, DB, infra — current and target |
| 5 | **Constraints** | Budget, timeline, team size, compliance, non-negotiables |
| 6 | **Architectural Principles** | How should the system be built? Any strong opinions? |
| 7 | **Known Unknowns** | What has the user flagged as uncertain or undecided? |
| 8 | **Success Criteria** | How will you know v1 is done and working? |

Show the user your gap analysis like this:

```
Here's what I extracted:

✅ Purpose — [one line summary]
✅ Users — [one line summary]
⚠️ Core Features — [what you got, what's missing]
❓ Tech Stack — not mentioned
✅ Constraints — [one line summary]
❓ Architectural Principles — not mentioned
❓ Known Unknowns — not mentioned
⚠️ Success Criteria — [what you got, what's vague]
```

Then proceed to Phase 3.

---

## Phase 3 — Clarification Loop

Ask only about ❓ Unknown and ⚠️ Partial categories. Ask in batches of **3–5 questions max**. Keep questions short and conversational — not formal or intimidating.

Format:
```
I have a few questions to fill the gaps:

1. [Question about gap 1]
2. [Question about gap 2]
3. [Question about gap 3]

Answer however works for you — bullet points, a paragraph, shorthand is fine.
```

After the user responds, re-evaluate your gap analysis. If gaps remain, ask another small batch. If you have enough, proceed.

**Stop the loop when:**
- All 8 categories are ✅ Known or deliberately marked as "TBD" by the user
- The user says "that's enough, generate it"
- You've done 3 rounds of clarification (don't over-interrogate)

Before generating, say:
> "I have enough to produce your v1.0 spec.md. One moment."

---

## Phase 4 — Generate spec.md

Produce the full `spec.md` using the structure below. Fill every section with real content derived from the user's input and your clarification answers.

**Rules:**
- No placeholder text. No "TBD" unless the user explicitly said something is undecided.
- Write for a developer (human or AI) reading this project for the first time.
- If the user's input contradicts itself, flag it and ask before generating.
- If the user has no existing codebase, the Codebase Inventory starts with just the framework files.

---

```markdown
# [Project Name] — Project Specification

> **Version:** 1.0
> **Created:** YYYY-MM-DD
> **Last Updated:** YYYY-MM-DD
> **Status:** 🟡 In Planning
>
> Living document — the AI agent updates Codebase Inventory, Decision Log,
> and Current Focus at the end of every working session. Do not edit those
> sections manually.

---

## Current Focus
<!-- The agent updates this at the start of each session. -->
<!-- Humans: glance here to see what is actively being worked on. -->

- Nothing started yet — spec v1.0 just created.

---

## ⚠️ Critical Pre-Work (Do Before Any Feature Work)
<!-- Delete this section once all items are complete. -->

- [ ] [Security or setup blocker 1]
- [ ] [Security or setup blocker 2]

---

## Project Overview

[2–3 paragraphs: what the project does, why it exists, who it is for.]

### Problem Statement

[One crisp paragraph: what pain does this solve and for whom?]

### Target Users

[Who uses this? What are their goals? What do they need most from this system?]

### Current Operational Reality (as of YYYY-MM-DD)

[What actually works today? What is deployed? What is in progress? If greenfield, say so.]

---

## Success Criteria (v1.0)
<!-- How do we know v1.0 is done? Make each criterion testable. -->

- [ ] [Criterion 1 — specific and verifiable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Constraints & Non-Negotiables

- **Team:** [e.g., 2 developers, part-time]
- **Timeline:** [e.g., MVP in 6 weeks]
- **Budget:** [e.g., infrastructure must stay under $50/month]
- **Compliance:** [e.g., GDPR, SOC2, none]
- **Non-negotiables:** [e.g., must work offline, must support mobile browsers]

---

## Tech Stack

### Current (what exists today)

| Layer | Technology | Notes |
|---|---|---|
| Language | | |
| Framework | | |
| Database | | |
| Auth | | |
| Frontend | | |
| Testing | | |
| Containerisation | | |
| CI/CD | | |

### Target (what we are building toward)

| Layer | Technology | Notes |
|---|---|---|
| [Same rows — fill in only where target differs from current] | | |

---

## Architectural Principles
<!-- These are the rules the AI agent follows when making technical decisions. -->

- **Frontend/backend separation**: keep browser assets and Jinja views in `frontend/`; keep Flask application code, database models, migrations, and tests in `backend/`.
- **MVC organization**: map Jinja templates to Views, Flask blueprints/routes to Controllers, and SQLAlchemy entities to Models. Put reusable business logic in `backend/app/services/`.
- **Separation of concerns**: controllers should handle HTTP concerns and delegate data/business operations to services and models.
- **[Principle]**: [What it means in practice for this project]
- **[Principle]**: [What it means in practice]
- **TDD**: write tests before implementation; aim for >80% coverage on core logic

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

---

## Codebase Inventory
<!-- The agent updates this table when files are created, moved, or deleted. -->
<!-- Do not edit manually. -->

| File | Role | Status | Last Updated |
|---|---|---|---|
| `AGENT_MD/spec.md` | Living project specification | ✅ Active | YYYY-MM-DD |
| `AGENT_MD/plan/rules.md` | AI agent authoring conventions | ✅ Active | YYYY-MM-DD |

---

## Feature Index
<!-- Status: [ ] Not started | 🔄 In progress | ✅ Complete | ⏸ Blocked -->
<!-- Agent updates Status as work progresses. -->

| # | Feature | Status | Priority | Notes |
|---|---|---|---|---|
| 0 | Pre-Work: Setup & Security | [ ] | P0 | Credentials, dependencies, repo setup |
| 1 | [Feature name] | [ ] | P0 | [Brief note] |
| 2 | [Feature name] | [ ] | P1 | [Brief note] |

---

## Known Issues & Technical Debt
<!-- Agent appends issues discovered during implementation. Humans can add items too. -->

- None yet.

---

## Known Unknowns
<!-- Deliberately undecided. Revisit as the project matures. -->

- [Unknown or deferred decision 1]

---

## Decision Log
<!-- The agent appends one row here after every session. -->
<!-- Format: Date | Decision | Rationale | Alternatives considered -->
<!-- Do not edit manually. -->

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| YYYY-MM-DD | Created v1.0 spec.md | Project initialisation | n/a |

---

---

# FEATURE 0 — Pre-Work: Setup & Security

## Goal

Establish a clean, secure foundation before any feature work begins.

## Tasks

- [ ] Initialise git repository and set up `.gitignore`
- [ ] Set up environment variable management (`.env` + `.env.example`)
- [ ] Audit and pin critical dependencies
- [ ] Set up CI/CD pipeline skeleton
- [ ] Create initial project directory structure

## Verification

- Repository is clean; no secrets committed
- `git log --all -p | grep -i secret` returns nothing sensitive
- CI passes on an empty run

---

# FEATURE 1 — [Feature Name]

## Goal

[What this feature achieves and why it matters.]

## Existing Code to Reference
<!-- Agent: load these files into context at the start of the session for this feature. -->

- [None yet — populated as codebase grows]

## Tasks

- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

## Acceptance Criteria

- [ ] [How to verify this feature works end-to-end]
- [ ] [Edge cases covered]

---

<!-- Agent instruction: add new FEATURE sections above this line as features are identified. -->
```

---

## Phase 5 — Confirmation & Write

After generating the spec content, say:

> "Here is your v1.0 spec.md. Does this look right? Tell me what to adjust, or confirm and I'll write the file."

Wait for the user's response. Make any requested adjustments. Then write the file to `AGENT_MD/spec.md`.

Once the file is written, say:

> "spec.md is ready. Your next step: follow the setup instructions in AGENT_MD/README.md to install the agent skill for your AI tool, then begin with Feature 0."

---

## Notes for the Agent

- Prefer clarity over completeness — a spec with 5 honest sections beats one with 15 vague ones.
- If the user's input contradicts itself, flag the contradiction and ask which is correct — do not silently pick one.
- Version the spec: every time `spec.md` is substantially updated, bump the version in the header (`1.0` → `1.1`, or `2.0` for a major restructure).
- The **Decision Log** and **Codebase Inventory** are agent-maintained. Never ask the user to fill these in — the agent populates them during implementation sessions.
- The rules at `AGENT_MD/plan/rules.md` govern how the agent behaves during implementation sessions. The spec you generate here is the input to those sessions.
