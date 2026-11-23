# VoltWise — Project Specification

> **Version:** 1.1
> **Created:** 2026-11-23
> **Last Updated:** 2026-11-23
> **Status:** 🟡 In Planning
>
> Living document — the AI agent updates **Codebase Inventory**, **Decision Log**, and **Current Focus**
> at the end of every working session. Do not edit those sections manually.

---

## Current Focus

- Building the responsive VoltWise authentication experience in React.
- Use a premium light mint and ice-white theme with green and blue accents.
- Support Domestic, Enterprise, and System Administrator account types.

---

## ⚠️ Critical Pre-Work (Do Before Any Feature Work)

- [ ] Add secure authentication API integration.
- [ ] Store credentials and environment values outside source control.
- [ ] Add route protection for authenticated dashboard pages.

---

## Project Overview

VoltWise is a smart appliance and electricity monitoring application for domestic and business users. Its login experience should help users securely enter the correct account area while presenting a modern, premium energy-brand identity.

The target experience uses a soft mint and ice-white interface, emerald green and blue accents, a glass-like login card, clear account selection, and a compact mobile layout.

### Problem Statement

Users need a clear, trustworthy way to monitor home or commercial electricity consumption. VoltWise provides separate domestic and business account paths in a focused, responsive authentication interface.

### Target Users

- Homeowners monitoring household electricity usage.
- Small and medium business operators managing commercial consumption.

### Current Operational Reality (as of 2026-11-23)

- A static HTML/CSS prototype exists at the workspace root.
- A React JS application using Vite exists at `d:\appliancemonitering\voltwise-react`.
- The login design is implemented and the React production build succeeds.
- Authentication and dashboard APIs are not yet integrated.

---

## Success Criteria (v1.0)

- [ ] The React login page builds successfully with Vite.
- [ ] Domestic, Enterprise, and System Administrator selections update the active account state.
- [ ] Password visibility can be toggled.
- [ ] The interface remains usable at desktop and mobile widths.
- [ ] No horizontal overflow occurs on mobile devices.
- [ ] Authentication form fields use visible labels, accessible names, and keyboard-focus states.
- [ ] Credentials are not committed to source control.

---

## Constraints & Non-Negotiables

- **Team:** Single developer.
- **Timeline:** MVP implementation in progress.
- **Budget:** No infrastructure budget established.
- **Compliance:** Security and credential handling best practices.
- **Non-negotiables:** React JS frontend, responsive layout, premium light theme, accessible authentication controls, and no emoji-based interface icons.

---

## Tech Stack

### Current (what exists today)

| Layer | Technology | Notes |
|---|---|---|
| Language | JavaScript, HTML, CSS | React components use JSX |
| Framework | React 19, Vite | React project in `voltwise-react` |
| Database | Not implemented | Authentication and usage data backend pending |
| Cache | Not implemented | |
| Auth | UI prototype only | API integration pending |
| Frontend | React, CSS | SVG icons and responsive layout |
| Testing | Vite build | Automated interaction tests not yet added |
| Containerisation | Not implemented | |
| CI/CD | Not implemented | |

### Target (what we are building toward)

| Layer | Technology | Notes |
|---|---|---|
| Database | TBD | Choose based on usage and deployment requirements |
| Auth | Secure backend authentication | Session or token strategy to be selected |
| Testing | Vitest / React Testing Library | Add form and account-selection tests |
| CI/CD | GitHub Actions | Build and test login app |

---

## Architectural Principles

- **Component isolation**: Keep reusable UI elements and SVG icons in focused React components.
- **Accessible by default**: Use semantic form labels, tab roles, visible focus states, and 44px minimum interactive targets.
- **Responsive first**: Preserve usability across 375px, 768px, 1024px, and 1440px widths.
- **Security-first authentication**: Never store or log raw passwords; integration must use secure backend endpoints.
- **Theme consistency**: Reuse existing CSS custom properties for dark surfaces, text, borders, and accent colors.
- **TDD**: Add focused tests before new authentication behavior, aiming for at least 80% coverage on core login logic.

---

## Codebase Inventory

| File | Role | Status | Last Updated |
|---|---|---|---|
| `AGENT_MD_v1/spec.md` | Living project specification | ✅ Active | 2026-11-23 |
| `AGENT_MD_v1/spec_init.md` | Raw project initialization input | ✅ Active | 2026-11-23 |
| `index.html` | Static VoltWise login prototype | ✅ Active | 2026-11-23 |
| `styles.css` | Static login theme | ✅ Active | 2026-11-23 |
| `script.js` | Static prototype interactions | ✅ Active | 2026-11-23 |
| `voltwise-react/src/App.jsx` | React login component and account state | ✅ Active | 2026-11-23 |
| `voltwise-react/src/main.jsx` | React application entry point | ✅ Active | 2026-11-23 |
| `voltwise-react/src/styles.css` | React login visual styles | ✅ Active | 2026-11-23 |
| `voltwise-react/package.json` | Vite and React dependencies | ✅ Active | 2026-11-23 |

---

## Feature Index

| # | Feature | Status | Priority | Notes |
|---|---|---|---|---|
| 0 | Pre-Work: Security + Stability | [ ] | P0 | Authentication API, environment variables, route protection |
| 1 | Responsive premium light-theme login page | ✅ | P0 | Domestic, Enterprise, and Administrator account selection with React state |
| 2 | Password visibility control | ✅ | P0 | Toggle implemented in React |
| 3 | Authentication API integration | [ ] | P0 | Login submission and error handling |
| 4 | Forgot-password flow | [ ] | P1 | UI link currently placeholder |
| 5 | Account creation flow | [ ] | P1 | UI link currently placeholder |
| 6 | Domestic usage dashboard | [ ] | P1 | Requires authentication |
| 7 | Enterprise usage dashboard | [ ] | P1 | Requires authentication |
| 8 | System administration console | [ ] | P1 | Requires elevated authentication |

---

## Known Issues & Technical Debt

- Login submission is intentionally prevented; no authentication backend is connected.
- Forgot-password and account creation links are placeholders.
- Automated tests and linting are not configured.
- Authentication provider and session strategy are undecided.

---

## Known Unknowns

- Authentication provider or backend framework.
- Database technology.
- Dashboard API contracts and user/household data model.
- Production hosting and CI/CD platform.

---

## Decision Log

| Date | Decision | Rationale | Alternatives Considered |
|---|---|---|---|
| 2026-11-23 | Added React/Vite implementation | User requested the login page in React JS | Static HTML/CSS prototype |
| 2026-11-23 | Used domestic/business account tabs | Matches supplied reference and supports both target user types | A single account login |
| 2026-11-23 | Created the specification | Replaced the unused spec template with the real VoltWise context | Leaving the template as-is |

---

# FEATURE 0 — Pre-Work: Security / Stability / Setup

## Goal

Establish secure authentication, environment configuration, testing, and deployment foundations before connecting production features.

## Tasks

- [ ] Initialize git repository and add `.gitignore`.
- [ ] Add `.env` and `.env.example` with no committed secrets.
- [ ] Audit and pin dependencies.
- [ ] Define authentication API endpoints and error contracts.
- [ ] Configure route protection.
- [ ] Add linting and automated tests.

## Verification

- Production build passes.
- No credentials or tokens appear in source control or application logs.
- Authenticated routes cannot be accessed anonymously.
- Login tests pass for success and validation failures.

---

# FEATURE 1 — Responsive Black-Theme Login Page

## Goal

Provide a premium VoltWise authentication entry page matching the supplied visual reference.

## Existing Code to Reference

- `voltwise-react/src/App.jsx`
- `voltwise-react/src/styles.css`
- `index.html`
- `styles.css`

## Tasks

- [ ] Preserve the soft mint, ice-white, emerald green, and blue visual system.
- [ ] Use neon green and electric blue accents only where they communicate status or primary actions.
- [ ] Preserve the domestic/enterprise/administrator account selector.
- [ ] Support password visibility toggling.
- [ ] Prevent horizontal overflow at mobile widths.

## Acceptance Criteria

- [ ] React production build succeeds.
- [ ] Domestic, Enterprise, and Administrator selections update the selected account state.
- [ ] Password toggle changes the input type and accessible label.
- [ ] Layout reflows at desktop and mobile breakpoints.
- [ ] Keyboard focus remains visible.

---

# FEATURE 2 — Authentication API Integration

## Goal

Submit login credentials securely and direct authenticated users to the correct dashboard.

## Existing Code to Reference

- `voltwise-react/src/App.jsx`

## Tasks

- [ ] Define the authentication request contract.
- [ ] Send credentials through a secure backend endpoint.
- [ ] Display field and server errors near the relevant controls.
- [ ] Store only approved session information.
- [ ] Redirect domestic and business users to their respective dashboards.

## Acceptance Criteria

- [ ] Invalid credentials produce accessible inline feedback.
- [ ] No password appears in logs or browser URLs.
- [ ] Successful authentication creates an authorized session.
- [ ] Account type controls the correct post-login destination.
