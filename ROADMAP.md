# SmartCare AI — Development Roadmap

Remaining work after the completed baseline. Each module is **independently buildable** with its own database migrations, API routes, UI pages, and tests. Dependencies are noted only where a module consumes another module’s APIs or data.

---

## Complexity Scale

| Level | Effort | Meaning |
|-------|--------|---------|
| **S** | 2–4 days | Few tables, ≤6 endpoints, 1–2 screens |
| **M** | 1–2 weeks | Full CRUD domain, RBAC, multiple pages |
| **L** | 2–4 weeks | Workflows, transactions, cross-entity rules |
| **XL** | 4+ weeks | AI integration, predictions, dashboards, or infra |

---

## Module Status

### Completed

| Module | Complexity | Delivered |
|--------|------------|-----------|
| **Authentication** ✅ | M | JWT login, RBAC (`Patient` / `Doctor` / `Admin`), demo users, `POST /auth/login`, `GET /auth/me` |
| **Patient Module** ✅ | M | Patient CRUD, search, medical history, admin registration, patient profile & history pages |

---

### Remaining — Core Hospital (MVP Phase 1)

| Module | Complexity | Build independently? | Depends on | Summary |
|--------|------------|------------------------|------------|---------|
| **Doctor Module** | M | Yes | Auth ✅ | Departments, doctor profiles, schedules, admin doctor UI, doctor linked to user account |
| **Appointment Module** | L | Yes* | Doctor Module | Book / reschedule / cancel, slot availability, status lifecycle, patient booking + staff list views |
| **Queue Management** | L | Yes* | Doctor Module; Appointment† | Tokens, priority queue, call-next, staff queue board, patient queue status |
| **Billing** | L | Yes | Auth ✅; Patient ✅ | Invoices, line items, payments, receipts; can bill by patient without appointments at first |
| **Medical Records (Full EHR)** | L | Yes* | Doctor Module | Structured visits, prescriptions, lab orders; extends existing medical history |

\* Appointment and Queue are independently testable with seeded doctors; full hospital flow needs both.  
† Queue can demo with walk-in tokens before appointments are live.

**Suggested order:** Doctor → Appointment → Queue → Billing → Medical Records (Full EHR)

---

### Remaining — Platform & Cross-Cutting

| Module | Complexity | Build independently? | Depends on | Summary |
|--------|------------|------------------------|------------|---------|
| **Users & Auth Hardening** | M | Yes | Auth ✅ | Move users to PostgreSQL, refresh token, logout, forgot-password; replaces in-memory demo users |
| **Shared UI & Route Protection** | M | Yes | Auth ✅ | Reusable components, layouts, Next.js middleware, role-based redirects |
| **Notifications** | M | Yes | — | Email/SMS abstraction, appointment reminders, queue alerts; hooks into other modules when ready |
| **Audit Logging** | M | Yes | — | `audit_logs` table, sensitive-action logging, admin read-only viewer |
| **Document Storage** | M | Yes | Patient ✅ | Upload/download medical files (PDF, images), metadata in DB, files in object storage |

These can ship in parallel with core hospital modules or immediately after Auth + Patient.

---

### Remaining — AI (Phase 2 & 3)

| Module | Complexity | Build independently? | Depends on | Summary |
|--------|------------|------------------------|------------|---------|
| **AI Chatbot** | XL | Yes | Auth ✅ | Gemini chat, session history, disclaimers, FAQ first then API tool calls |
| **Queue Prediction** | L | Yes* | Queue Management | Estimated wait time per token; heuristic MVP, improves with live queue data |
| **Medical Report Summarization** | L | Yes | Document Storage | AI summary of lab/radiology reports, doctor approve / edit / reject |
| **Symptom Analyzer** | M | Yes | Doctor Module | Symptom input → department + urgency; emergency flags, no diagnosis |
| **Doctor Workload Optimization** | L | Yes | Doctor, Appointment, Queue | Overload detection, redistribution recommendations, admin approval |
| **No-show Prediction** | L | Yes | Appointment Module | Risk score on appointments, staff flags; does not block booking |

**Suggested AI order:** Report Summarization or Chatbot first (establishes Gemini layer) → Queue Prediction → Symptom Analyzer → Workload → No-show

---

### Remaining — Analytics & Portals

| Module | Complexity | Build independently? | Depends on | Summary |
|--------|------------|------------------------|------------|---------|
| **Analytics** | XL | Yes* | Appointment, Queue, Billing† | Admin KPIs: appointments, wait times, revenue, no-show rates, AI usage dashboards |
| **Admin Portal** | L | Incremental | Core modules | Unified admin shell, dashboard, navigation (wireframes §3.x); page-by-page as modules land |
| **Doctor Portal** | L | Incremental | Doctor, Queue, EHR | Doctor dashboard, queue, consultation workspace (wireframes §2.x) |
| **Patient Portal (Extended)** | M | Incremental | Appointment, Queue, Billing | Booking, queue, bills, chat entry; extends existing dashboard / profile / history |

\* Analytics MVP can ship with mock or partial data; full value needs operational modules.  
† Revenue analytics needs Billing.

---

### Remaining — Deployment

| Module | Complexity | Build independently? | Depends on | Summary |
|--------|------------|------------------------|------------|---------|
| **Deployment** | M | Yes | — | Vercel (frontend), Railway (backend + Postgres), env config, health checks, migration on release, Docker compose for local dev |

Can start early (staging environment) and harden before production launch.

---

## Full Module List (Checklist)

```
Authentication                    ✅   M
Patient Module                    ✅   M

Doctor Module                          M
Appointment Module                     L
Queue Management                       L
Billing                                L
Medical Records (Full EHR)             L

Users & Auth Hardening                 M
Shared UI & Route Protection           M
Notifications                          M
Audit Logging                          M
Document Storage                       M

AI Chatbot                             XL
Queue Prediction                       L
Medical Report Summarization           L
Symptom Analyzer                       M
Doctor Workload Optimization           L
No-show Prediction                     L

Analytics                              XL
Admin Portal                           L
Doctor Portal                          L
Patient Portal (Extended)              M

Deployment                             M
```

---

## Recommended Milestones

### Milestone 1 — Next up (≈ 2–3 weeks)

| Module | Complexity |
|--------|------------|
| Doctor Module | M |
| Shared UI & Route Protection | M |
| Users & Auth Hardening | M |

**Goal:** Doctors manageable in admin UI; routes protected by role; users in database.

---

### Milestone 2 — MVP hospital flow (≈ 8–12 weeks total)

| Module | Complexity |
|--------|------------|
| Appointment Module | L |
| Queue Management | L |
| Billing | L |
| Medical Records (Full EHR) | L |
| Document Storage | M |
| Audit Logging | M |

**Goal:** Patient journey from booking → queue → consult → bill → records.

---

### Milestone 3 — AI & insights (≈ 6–10 weeks)

| Module | Complexity |
|--------|------------|
| Medical Report Summarization | L |
| Queue Prediction | L |
| AI Chatbot | XL |
| Symptom Analyzer | M |
| Notifications | M |

---

### Milestone 4 — Optimization & launch (≈ 6–8 weeks)

| Module | Complexity |
|--------|------------|
| Doctor Workload Optimization | L |
| No-show Prediction | L |
| Analytics | XL |
| Admin / Doctor / Patient portals (polish) | L + M |
| Deployment | M |

---

## Effort Summary

| Scope | Modules | Approx. effort |
|-------|---------|----------------|
| **Done** | Authentication, Patient | ~3–4 weeks (complete) |
| **MVP Phase 1 remaining** | Doctor through Medical Records + platform helpers | ~10–16 developer-weeks |
| **AI + Analytics + Deployment** | All AI modules, Analytics, Portals, Deployment | ~18–28 developer-weeks |
| **Full product (PRD)** | All modules above | ~30–45 developer-weeks total remaining |

---

## Definition of Done (Every Module)

- Alembic migration(s) where schema changes apply  
- FastAPI routes with Pydantic validation and RBAC  
- Frontend pages: responsive, loading / empty / error states  
- Tests for critical paths  
- Environment variables documented in `.env.example`  
- Module demoable on its own without broken stubs in the happy path  

Standards: `skills.md` · Requirements: `prd.md` · Architecture: `docs/architecture.md`
