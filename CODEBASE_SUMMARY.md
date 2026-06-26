# SmartCare AI — Codebase Summary

> Generated from repository analysis on 2026-06-26. This document reflects **what exists in code today**, cross-referenced with project documentation (`skills.md`, `prd.md`, `docs/architecture.md`, `docs/ui_wireframes.md`, `project_context.md`, `ai_memory.md`).

---

## 1. Project Architecture

### 1.1 High-Level Design

SmartCare AI is a **modular monolith** hospital management platform targeting deployment on **Vercel (frontend)** and **Railway (backend + PostgreSQL)**. The intended architecture follows clean layering:

```
Browser (Web / Mobile)
        │
        ▼
Next.js 15 Frontend (Presentation)
        │  HTTPS REST / JSON
        ▼
FastAPI Backend (API + Application + Domain + Infrastructure)
        │
        ├── PostgreSQL (transactional data)
        ├── Object Storage (planned — medical documents)
        ├── Gemini API (planned — AI features)
        └── Notification providers (planned)
```

### 1.2 Request Flow (Implemented)

```
Next.js page / service
  → fetch() to /api/v1/*
    → FastAPI router (auth.py | patients.py)
      → require_roles() JWT middleware
        → Service (AuthService | PatientService)
          → Repository (UserRepository | PatientRepository)
            → In-memory users OR PostgreSQL (patients)
```

### 1.3 Current Implementation Status

| Layer | Status |
|-------|--------|
| Frontend (Next.js 15, TypeScript, Tailwind) | Partial — auth + patient flows only |
| Backend (FastAPI, SQLAlchemy) | Partial — auth + patient APIs |
| Database (PostgreSQL) | Partial — `patients` and `patient_medical_history` tables |
| JWT + RBAC | Implemented (3 roles: Patient, Doctor, Admin) |
| AI (Gemini) | Not implemented |
| Docker | PostgreSQL service only via `docker/docker-compose.yml` |
| CI/CD | Not present in repo |

### 1.4 Authentication Model

- **JWT bearer tokens** (HS256) issued on login; 30-minute expiry (configurable via `ACCESS_TOKEN_EXPI_MINUTES`).
- **Role-based access control** enforced via FastAPI dependency `require_roles()`.
- Frontend stores token and user in `localStorage` (`smartcare_token`, `smartcare_user`).
- Users are currently **hardcoded in memory** in `UserRepository` (not persisted to PostgreSQL).

---

## 2. Folder Structure

### 2.1 Actual Repository Layout

```
smartcare-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # auth.py, patients.py
│   │   ├── core/             # config.py, security.py
│   │   ├── database/         # base.py, session.py, migrations/
│   │   ├── models/           # patient.py
│   │   ├── repositories/     # user_repository.py, patient_repository.py
│   │   ├── schemas/          # auth.py, patient.py
│   │   ├── services/         # auth_service.py, patient_service.py
│   │   └── main.py
│   ├── tests/                # test_auth.py, test_patients.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── docker/
│   ├── docker-compose.yml    # PostgreSQL 16 only
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── structure.md          # Target/planned structure (not fully built)
│   └── ui_wireframes.md
├── frontend/
│   ├── app/
│   │   ├── (auth)/login/
│   │   ├── (patient)/dashboard/, profile/, medical-records/
│   │   ├── (admin)/patients/, patients/register/
│   │   ├── globals.css, layout.tsx, page.tsx
│   ├── lib/                  # auth.ts, config.ts, patient.ts
│   ├── services/             # auth.service.ts, patient.service.ts
│   ├── types/                # auth.ts, patient.ts, api.ts
│   ├── tests/unit/           # auth.test.mjs, patient.test.mjs
│   ├── middleware.ts         # Empty matcher (no route protection)
│   ├── Dockerfile
│   └── package.json
├── ai_memory.md
├── project_context.md
├── prd.md
├── skills.md
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

### 2.2 Documented but Not Present

The following are described in `docs/structure.md`, `prd.md`, or `project_context.md` but **do not exist in the repo yet**:

| Path | Purpose |
|------|---------|
| `docs/database.md` | Referenced in `project_context.md` — **file missing** |
| `docs/ui-wireframes.md` | Requested name; actual file is `docs/ui_wireframes.md` |
| `database/` | Standalone migrations, seeds, schema |
| `prompts/` | AI prompt templates |
| `scripts/` | Dev setup, migrate, seed scripts |
| `.github/workflows/` | CI/CD pipelines |
| `frontend/components/` | Shared UI components |
| `frontend/features/` | Feature modules |
| `frontend/hooks/` | React hooks |
| `backend/app/integrations/` | Gemini, email, SMS, storage |
| `backend/app/workers/` | Background jobs |
| Most backend API modules | doctors, appointments, queues, billing, ai, admin |
| Doctor and admin route groups (most pages) | See Frontend Pages section |

---

## 3. Implemented Modules

### 3.1 Authentication

**Backend**

| Component | File | Notes |
|-----------|------|-------|
| Login endpoint | `backend/app/api/v1/auth.py` | `POST /api/v1/auth/login` |
| Current user | `backend/app/api/v1/auth.py` | `GET /api/v1/auth/me` |
| RBAC demo route | `backend/app/api/v1/auth.py` | `GET /api/v1/auth/admin-only` |
| Auth service | `backend/app/services/auth_service.py` | Credential validation, token issuance |
| Security | `backend/app/core/security.py` | PBKDF2-SHA256 hashing, JWT create/decode, `require_roles()` |
| User repository | `backend/app/repositories/user_repository.py` | In-memory demo users |
| Schemas | `backend/app/schemas/auth.py` | LoginRequest, TokenResponse, AuthenticatedUser |
| Tests | `backend/tests/test_auth.py` | Login, RBAC allow/deny |

**Frontend**

| Component | File | Notes |
|-----------|------|-------|
| Login page | `frontend/app/(auth)/login/page.tsx` | Client form, demo accounts, localStorage auth |
| Auth service | `frontend/services/auth.service.ts` | `login()` fetch wrapper |
| Auth helpers | `frontend/lib/auth.ts` | Role home paths, `canAccessRole()` |
| Types | `frontend/types/auth.ts` | UserRole, LoginRequest, LoginResponse |

**Demo accounts** (password: `Password123`):

| Role | Email |
|------|-------|
| Patient | patient@smartcare.ai |
| Doctor | doctor@smartcare.ai |
| Admin | admin@smartcare.ai |

### 3.2 Patient Management

**Backend**

| Component | File | Notes |
|-----------|------|-------|
| Patient routes | `backend/app/api/v1/patients.py` | Full CRUD + medical history |
| Patient service | `backend/app/services/patient_service.py` | Business rules, duplicate detection, code generation |
| Patient repository | `backend/app/repositories/patient_repository.py` | SQLAlchemy persistence |
| Models | `backend/app/models/patient.py` | `Patient`, `PatientMedicalHistory` |
| Schemas | `backend/app/schemas/patient.py` | Create, Update, Response, MedicalHistory |
| Migration | `backend/app/database/migrations/20260617_0001_create_patients.py` | Alembic revision |
| Tests | `backend/tests/test_patients.py` | Registration, search, profile, history, RBAC |

**Frontend**

| Component | File | Notes |
|-----------|------|-------|
| Patient dashboard | `frontend/app/(patient)/dashboard/page.tsx` | Profile summary cards |
| Patient profile | `frontend/app/(patient)/profile/page.tsx` | Full profile display |
| Medical records | `frontend/app/(patient)/medical-records/page.tsx` | Timeline of history |
| Admin patient list | `frontend/app/(admin)/patients/page.tsx` | Search with pagination |
| Register patient | `frontend/app/(admin)/patients/register/page.tsx` | Admin registration form |
| Patient service | `frontend/services/patient.service.ts` | API client functions |
| Utilities | `frontend/lib/patient.ts` | Name formatting, search matching |
| Types | `frontend/types/patient.ts` | Patient, MedicalHistoryItem |
| Tests | `frontend/tests/unit/patient.test.mjs` | Utility unit tests |

### 3.3 Infrastructure (Partial)

| Component | File | Notes |
|-----------|------|-------|
| App entry | `backend/app/main.py` | Registers auth + patient routers |
| Config | `backend/app/core/config.py` | Pydantic settings from `.env` |
| DB session | `backend/app/database/session.py` | SQLAlchemy engine + `get_db()` |
| Docker Postgres | `docker/docker-compose.yml` | PostgreSQL 16 on port 5432 |
| Env template | `.env.example` | API URL, DB, JWT, Gemini key placeholders |

---

## 4. Pending Modules

Based on `prd.md`, `project_context.md`, `ai_memory.md`, and gaps vs. `docs/structure.md`:

### 4.1 Phase 1 MVP (Core Hospital Operations)

| Module | Backend | Frontend | Database |
|--------|---------|----------|----------|
| Doctor Management | Not started | Not started | Not started |
| Appointment Booking | Not started | Not started | Not started |
| Queue Management | Not started | Not started | Not started |
| Billing | Not started | Not started | Not started |
| Medical Records (full EHR) | Partial (history only) | Partial (read-only timeline) | Partial |

### 4.2 Phase 2 — AI (Gemini)

| Feature | Status |
|---------|--------|
| Smart Chatbot | Not started |
| Medical Report Summarization | Not started |
| Queue Waiting Time Prediction | Not started |

### 4.3 Phase 3 — Advanced AI & Analytics

| Feature | Status |
|---------|--------|
| Symptom Analyzer | Not started |
| Doctor Workload Optimization | Not started |
| No-show Prediction | Not started |
| Analytics dashboards | Not started |

### 4.4 Cross-Cutting (Planned, Not Built)

- Refresh token / logout / forgot-password auth flows
- Persistent `users` and `roles` tables in PostgreSQL
- Next.js middleware route protection (matcher is empty)
- Shared UI component library (`components/ui`, forms, tables, modals)
- Notification service (SMS, email, WhatsApp)
- Audit logging
- Object storage for medical documents
- Background workers (reminders, AI summaries, queue predictions)
- CI/CD (GitHub Actions)
- Full admin/doctor dashboards per wireframes

**Next module** (per `ai_memory.md`): **Doctor Management**

---

## 5. API Routes

### 5.1 Implemented Routes

All routes are prefixed with `/api/v1`.

#### Authentication (`/auth`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/login` | Public | Login; returns JWT + user |
| GET | `/auth/me` | Patient, Doctor, Admin | Current authenticated user |
| GET | `/auth/admin-only` | Admin only | RBAC verification endpoint |

#### Patients (`/patients`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/patients` | Admin | Register new patient |
| GET | `/patients` | Admin, Doctor | Search/list patients (`q`, `limit`, `offset`) |
| GET | `/patients/me` | Patient | Get linked patient profile |
| GET | `/patients/me/medical-history` | Patient | Own medical history |
| GET | `/patients/{patient_id}` | Admin, Doctor | Get patient by ID |
| PATCH | `/patients/{patient_id}` | Admin | Update patient |
| POST | `/patients/{patient_id}/medical-history` | Admin, Doctor | Add history entry |
| GET | `/patients/{patient_id}/medical-history` | Admin, Doctor | List history for patient |

### 5.2 Planned Routes (from PRD / Architecture — Not Implemented)

#### Auth (planned)

- `POST /auth/logout`
- `POST /auth/refresh-token`
- `POST /auth/forgot-password`

#### Doctors

- `POST /doctors`, `GET /doctors`, `GET /doctors/{id}`, `PATCH /doctors/{id}`
- `GET /doctors/{id}/schedule`, `POST /doctors/{id}/schedule`

#### Appointments

- `POST /appointments`, `GET /appointments`, `GET /appointments/{id}`, `PATCH /appointments/{id}`
- `POST /appointments/{id}/cancel`, `POST /appointments/{id}/check-in`

#### Queues

- `GET /queues`, `GET /queues/{id}`, `POST /queues/tokens`
- `PATCH /queues/tokens/{id}`, `POST /queues/{id}/call-next`
- `GET /patients/{id}/queue-status`

#### Billing

- `POST /invoices`, `GET /invoices`, `GET /invoices/{id}`
- `POST /invoices/{id}/payments`, `POST /invoices/{id}/refund`

#### Medical Records (extended)

- `POST /medical-records`, `GET /patients/{id}/medical-records`
- `GET /medical-records/{id}`, `PATCH /medical-records/{id}`
- `POST /medical-documents`

#### AI

- `POST /ai/symptom-analyzer`, `POST /ai/queue-wait-prediction`
- `POST /ai/report-summary`, `POST /ai/chat`
- `GET /ai/workload-recommendations`, `POST /ai/no-show-prediction`

### 5.3 API Conventions

**Implemented today**

- Version prefix: `/api/v1`
- Bearer JWT in `Authorization` header
- Pydantic request/response validation
- Role checks via `require_roles()`
- Pagination on patient search (`limit` 1–100, `offset`)

**Planned (documented, not enforced in code)**

- Standard envelope: `{ success, data, message }` / `{ success: false, error: { code, message, details } }`
- OpenAPI documentation (FastAPI auto-docs available at `/docs` when running)
- Rate limiting on auth and AI endpoints

---

## 6. Database Schema

### 6.1 Implemented Tables (PostgreSQL)

#### `patients`

| Column | Type | Constraints |
|--------|------|-------------|
| id | VARCHAR(36) | PK, UUID default |
| patient_code | VARCHAR(32) | UNIQUE, indexed |
| user_id | VARCHAR(64) | UNIQUE, nullable, indexed — links to auth user |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| date_of_birth | DATE | NOT NULL |
| gender | VARCHAR(32) | NOT NULL |
| phone | VARCHAR(32) | UNIQUE, indexed |
| email | VARCHAR(255) | UNIQUE, nullable, indexed |
| address | TEXT | nullable |
| emergency_contact | VARCHAR(255) | nullable |
| blood_group | VARCHAR(8) | nullable |
| insurance_provider | VARCHAR(120) | nullable |
| insurance_number | VARCHAR(120) | nullable |
| status | VARCHAR(32) | default `Active` |
| created_at | TIMESTAMPTZ | server default |
| updated_at | TIMESTAMPTZ | server default, on update |

#### `patient_medical_history`

| Column | Type | Constraints |
|--------|------|-------------|
| id | VARCHAR(36) | PK |
| patient_id | VARCHAR(36) | FK → patients.id ON DELETE CASCADE, indexed |
| visit_date | DATE | NOT NULL |
| doctor_name | VARCHAR(160) | NOT NULL |
| department | VARCHAR(120) | NOT NULL |
| diagnosis | VARCHAR(255) | NOT NULL |
| notes | TEXT | nullable |
| created_at | TIMESTAMPTZ | server default |

**Migration:** `20260617_0001` (Alembic revision in `backend/app/database/migrations/`)

### 6.2 Not Yet Migrated (Planned per PRD / Architecture)

| Group | Tables |
|-------|--------|
| Identity & Access | users, roles, permissions, role_permissions, user_sessions, password_reset_tokens |
| Hospital Organization | branches, departments, rooms, services |
| Patients (extended) | patient_contacts, patient_insurance, patient_allergies, patient_conditions |
| Doctors | doctors, doctor_specialties, doctor_schedules, doctor_leaves |
| Appointments | appointments, appointment_status_history, appointment_reminders |
| Queues | queues, queue_tokens, queue_status_history |
| Medical Records (full) | visits, medical_records, prescriptions, lab_orders, medical_documents, document_summaries |
| Billing | invoices, invoice_items, payments, refunds, billing_adjustments |
| AI | ai_interactions, ai_prompt_versions, ai_predictions, chatbot_sessions, chatbot_messages |
| Audit | audit_logs, security_events, system_events |

### 6.3 Database Tooling

- **ORM:** SQLAlchemy 2.x with declarative models
- **Migrations:** Alembic (`alembic.ini` present; one revision committed)
- **Connection:** `DATABASE_URL` env var (default `postgresql+psycopg://postgres:postgres@localhost:5432/smartcare_ai`)
- **Tests:** In-memory SQLite override in `test_patients.py`

---

## 7. Frontend Pages

### 7.1 Implemented Pages

| Route | File | Role | Description |
|-------|------|------|-------------|
| `/` | `app/page.tsx` | Public | Placeholder home ("SmartCare AI") |
| `/login` | `app/(auth)/login/page.tsx` | Public | Sign-in form with demo accounts |
| `/dashboard` | `app/(patient)/dashboard/page.tsx` | Patient* | Profile summary (ID, phone, blood group, insurance) |
| `/profile` | `app/(patient)/profile/page.tsx` | Patient* | Detailed profile view |
| `/medical-records` | `app/(patient)/medical-records/page.tsx` | Patient* | Medical history timeline |
| `/patients` | `app/(admin)/patients/page.tsx` | Admin/Doctor* | Patient search list |
| `/patients/register` | `app/(admin)/patients/register/page.tsx` | Admin* | Patient registration form |

\*Route groups `(patient)` and `(admin)` do not add URL segments; **middleware does not enforce role-based routing** — protection is client-side via token presence and API RBAC.

### 7.2 Planned Pages (from Wireframes / Structure — Not Built)

#### Patient Portal

| Route | Wireframe Section |
|-------|-------------------|
| `/appointments` | Appointment booking |
| `/queue` | Queue status |
| `/billing` | Bills & payments |
| `/chatbot` | Smart assistant |

#### Doctor Portal

| Route | Wireframe Section |
|-------|-------------------|
| `/dashboard` (doctor) | Daily summary, queue, appointments |
| `/queue` | Queue management |
| `/appointments` | Today's schedule |
| `/patients` | Patient lookup |
| `/consultations` | Clinical notes workspace |
| `/medical-records` | Report review |
| `/workload` | Workload insights |

#### Admin Portal

| Route | Wireframe Section |
|-------|-------------------|
| `/dashboard` | KPI cards, operations overview |
| `/doctors` | Doctor management |
| `/appointments` | Appointment management |
| `/queues` | Queue operations |
| `/billing` | Billing management |
| `/medical-records` | Records oversight |
| `/ai-insights` | AI metrics |
| `/settings` | Users, roles, departments |

#### Auth (planned)

- `/register`, `/forgot-password`

### 7.3 UI Patterns in Use

- **Mobile-first** Tailwind layouts (`max-w-*`, responsive grids)
- **Client components** (`"use client"`) for all interactive pages
- **Semantic HTML** with labels, `role="alert"`, `aria-live`
- **Slate color palette** — no shared component library yet; inline Tailwind classes
- **Auth state:** `localStorage` (not httpOnly cookies)

---

## 8. Coding Conventions

### 8.1 Backend (Python / FastAPI)

| Convention | Practice in Repo |
|------------|------------------|
| Layering | Router → Service → Repository → Model |
| Validation | Pydantic v2 schemas in `schemas/` |
| DI | FastAPI `Depends()` for DB session and services |
| Auth | `require_roles(UserRole.*)` dependency injection |
| Errors | `HTTPException` with appropriate status codes (401, 403, 404, 409) |
| IDs | UUID strings (36 chars) |
| Password hashing | Custom PBKDF2-SHA256 (120k iterations in security module; demo users use 60k) |
| JWT | python-jose, HS256 |
| Config | pydantic-settings, `.env` file |
| Tests | pytest + FastAPI TestClient; SQLite in-memory for patient tests |
| Docstrings | Module-level docstrings on Python files |

**Naming**

- Files: `snake_case.py`
- Classes: `PascalCase` (e.g., `PatientService`, `PatientRepository`)
- Routes: RESTful, plural nouns (`/patients`, `/auth/login`)

### 8.2 Frontend (TypeScript / Next.js)

| Convention | Practice in Repo |
|------------|------------------|
| Framework | Next.js 15 App Router |
| Components | Default server components; `"use client"` when state/effects needed |
| Route groups | `(auth)`, `(patient)`, `(admin)` for organization |
| API calls | `services/*.service.ts` with `fetch()` |
| Config | `lib/config.ts` — `NEXT_PUBLIC_API_URL` |
| Types | Dedicated `types/` directory, exported types (not interfaces in services) |
| Styling | Tailwind CSS utility classes |
| Path alias | `@/` → project root (tsconfig paths) |
| Tests | Node `assert` in `.mjs` files (mirrors lib logic, not full component tests) |
| Auth storage | `localStorage` keys: `smartcare_token`, `smartcare_user` |

**Naming**

- Files: `kebab-case` for routes, `camelCase.ts` for utilities, `*.service.ts` for API layer
- Functions: `camelCase` (e.g., `getMyPatientProfile`, `formatPatientName`)
- Types: `PascalCase` (e.g., `Patient`, `UserRole`)

### 8.3 Cross-Cutting Standards (from `skills.md` — Target)

These are **documented expectations**; adoption varies in current code:

- Clean architecture with domain boundaries
- No secrets in code — use environment variables
- WCAG 2.1 AA accessibility
- Consistent loading, empty, and error states (partially implemented)
- Unit tests for critical business logic (backend: yes; frontend: utility-only)
- API versioning under `/api/v1`
- AI calls isolated behind backend integration layer (not yet applicable)

### 8.4 Git & Project Docs

| File | Purpose |
|------|---------|
| `skills.md` | Engineering standards, tech stack, definition of done |
| `prd.md` | Full product requirements, roles, APIs, MVP phases |
| `docs/architecture.md` | System design, service map, planned folder layout |
| `docs/ui_wireframes.md` | UI wireframes for patient, doctor, admin dashboards |
| `docs/structure.md` | Target repository tree (aspirational) |
| `project_context.md` | Quick status: completed vs pending |
| `ai_memory.md` | Session progress notes for AI agents |

---

## 9. Environment & Local Development

### 9.1 Required Environment Variables

From `.env.example`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
APP_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/smartcare_ai
JWT_SECRET=change-me
GEMINI_API_KEY=change-me
```

### 9.2 Running Locally (Typical)

1. Start PostgreSQL: `docker compose -f docker/docker-compose.yml up -d`
2. Run Alembic migration: apply `20260617_0001`
3. Backend: `uvicorn app.main:app --reload` from `backend/`
4. Frontend: `npm run dev` from `frontend/`

### 9.3 Test Commands

| Scope | Command |
|-------|---------|
| Backend | `pytest` from `backend/` |
| Frontend | `npm test` (runs unit tests in `tests/unit/`) |

---

## 10. Summary

SmartCare AI is an early-stage hospital management platform with a **clear architectural vision** (modular monolith, clean layers, JWT + RBAC, PostgreSQL) and **two working domains**: **Authentication** and **Patient Management**. The backend exposes 11 patient-related endpoints plus 3 auth endpoints; the frontend provides login, patient self-service pages, and admin patient registration/search. Everything else in the PRD — doctors, appointments, queues, billing, full EHR, AI features, analytics, and shared UI infrastructure — remains **planned and documented but not implemented**. The next development priority is **Doctor Management** per project memory files.
