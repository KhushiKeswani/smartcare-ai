# SmartCare AI — Codebase Summary

> Generated from repository analysis on 2026-06-27. This document reflects **what exists in code today** and highlights gaps against product documentation (`prd.md`, `skills.md`, `ROADMAP.md`, `docs/*`, `project_context.md`, `ai_memory.md`).

---

## 1. Project Overview

**SmartCare AI** is a **Smart Hospital Management System** intended to digitize core hospital workflows and extend them with AI-assisted features. The product targets multiple staff roles and patient self-service, including:

- Patient registration + profile + medical history
- Doctor profiles + scheduling (planned/partial)
- Appointment booking (planned/partial)
- Queue management (planned)
- Billing and receipts (planned)
- Full EHR expansion (planned)
- AI features (planned): symptom analysis, report summarization, queue prediction, chatbot, workload optimization, no-show prediction

Current repository state is an early MVP foundation with **Authentication** and **Patient Management** implemented end-to-end (backend + some frontend), plus **Doctor + Appointment** backend foundations that exist as code but are not reflected in the frontend routes as complete module UX.

---

## 2. Technology Stack

### Frontend
- **Next.js 15 (App Router)**
- **React**
- **TypeScript**
- **TailwindCSS**

### Backend
- **FastAPI**
- **Python**
- **Pydantic v2** (request/response schemas)
- **JWT auth + RBAC** via FastAPI dependencies

### Database
- **SQLAlchemy ORM**
- **Alembic** migrations configured (one migration present)
- **PostgreSQL (target)**
- **SQLite in-memory** used for backend tests

### Authentication
- **JWT bearer tokens**
- **Roles**: `Patient`, `Doctor`, `Admin`
- RBAC enforced with `require_roles()` dependency
- Frontend stores token in `localStorage` (`smartcare_token`) and user in `localStorage` (`smartcare_user`)

### Testing
- Backend: **pytest** + **FastAPI TestClient** + SQLite override
- Frontend: utility-level tests (Node `.mjs` unit tests) under `frontend/tests/*`

### Deployment
- Target: **Vercel** for frontend
- Target: **Railway** for backend + database
- Docker Compose present for local PostgreSQL

---

## 3. Folder Structure

### Top-level
- `README.md`: general overview (and roadmap excerpts)
- `prd.md`: functional requirements and full module checklist
- `skills.md`: engineering standards and target architecture practices
- `ROADMAP.md`: module status and recommended implementation order
- `project_context.md`, `ai_memory.md`: project progress notes

### Backend (`backend/`)
- `app/main.py`: FastAPI app entry point; includes routers under `/api/v1`
- `app/api/v1/`: **versioned route modules**
  - `auth.py`, `patients.py`, `doctors.py`, `appointments.py`
- `app/core/`: security + config
  - `security.py`: JWT + password hashing + RBAC dependency
  - `config.py`: settings via environment variables
- `app/database/`:
  - `base.py`: SQLAlchemy declarative base
  - `session.py`: DB session / `get_db()` dependency
  - `migrations/`: Alembic revisions
- `app/models/`: SQLAlchemy models
  - `patient.py`, `doctor.py`, `appointment.py`
- `app/schemas/`: Pydantic request/response models
- `app/repositories/`: persistence layer (SQLAlchemy operations)
- `app/services/`: business logic layer
- `tests/`: backend tests (unit/integration style)

### Frontend (`frontend/`)
- `app/`: Next.js App Router routes
  - Route groups: `(auth)`, (patient), (doctor), (admin)
  - Implemented pages exist for: login + patient dashboard/profile/records + admin patient management
- `components/`: UI component folders (currently mostly placeholders)
- `features/`: feature folders (currently mostly placeholders)
- `services/`: frontend API clients (`*.service.ts`)
- `lib/`: shared helpers (auth + formatting + small utilities)
- `types/`: shared TypeScript types
- `middleware.ts`: present but matcher is empty (no route protection)

---

## 4. Database Models (SQLAlchemy)

> Notes: The repository currently models only a subset of the PRD database. Only `Patient`, `PatientMedicalHistory`, `Doctor`, `DoctorSchedule`, and `Appointment` tables are implemented.

### `Patient` (`backend/app/models/patient.py`)
- **Purpose**: Stores patient profile data and links to an auth user (optional `user_id`).
- **Relationships**:
  - `medical_history: relationship(PatientMedicalHistory)` via `patient_medical_history.patient_id` FK
- **Important fields**:
  - `id` (UUID string primary key)
  - `patient_code` (unique, indexed)
  - `user_id` (unique, nullable; links to auth identity)
  - `phone` (unique, indexed)
  - `email` (unique, nullable; indexed)
  - `status` (default `Active`)
  - `created_at`, `updated_at`
- **Missing fields vs PRD (full EHR scope)**:
  - No separate tables for allergies/conditions/contacts/insurance beyond basic fields
  - No `patient type` (outpatient/inpatient) field
  - No consent flags or document storage metadata

### `PatientMedicalHistory` (`backend/app/models/patient.py`)
- **Purpose**: Stores consultation-style history records (a lightweight medical history timeline).
- **Relationships**:
  - Belongs to `Patient` (`patient_id` FK)
- **Important fields**:
  - `id` (UUID string primary key)
  - `patient_id` (FK to `patients.id`, cascade delete)
  - `visit_date`
  - `doctor_name`, `department`
  - `diagnosis`, optional `notes`
  - `created_at`
- **Missing fields vs PRD EHR**:
  - No structured prescriptions
  - No visit/entity separation (`visit_id`, `follow_up_date`, etc.)
  - No attachment/document metadata

### `Doctor` (`backend/app/models/doctor.py`)
- **Purpose**: Stores doctor profile details and links to auth user (optional).
- **Relationships**:
  - `schedules: relationship(DoctorSchedule)`
- **Important fields**:
  - `id` (UUID string primary key)
  - `user_id` (unique, nullable; links to auth identity)
  - `doctor_code` (unique, indexed)
  - `email` / `phone` (unique, indexed)
  - `specialization`, `department`
  - `license_number` (unique, indexed)
  - `consultation_fee` (Numeric)
  - `is_available`, `status`
  - `created_at`, `updated_at`
- **Missing fields vs PRD**:
  - No explicit `specialties` many-to-many, only one `specialization`
  - No leave table (`doctor_leaves` planned)
  - No workload/performance fields

### `DoctorSchedule` (`backend/app/models/doctor.py`)
- **Purpose**: Stores weekly availability windows and slot parameters.
- **Relationships**:
  - Belongs to `Doctor` (`doctor_id` FK)
- **Important fields**:
  - `day_of_week` (int)
  - `start_time`, `end_time`
  - `slot_duration_minutes` (default 30)
  - `max_patients` (default 16)
  - `is_active`
  - `created_at`, `updated_at`
- **Missing fields vs PRD**:
  - No overrides/room assignment
  - No appointment status history

### `Appointment` (`backend/app/models/appointment.py`)
- **Purpose**: Stores appointment bookings between patient and doctor.
- **Relationships**:
  - FK-only fields exist (`patient_id`, `doctor_id`); there is no SQLAlchemy relationship currently defined to other appointment-related models.
- **Important fields**:
  - `id` (UUID string primary key)
  - `appointment_code` (unique, indexed)
  - `patient_id` (FK)
  - `doctor_id` (FK)
  - `appointment_datetime`
  - `appointment_type` (default `In-person`)
  - `status` (default `Scheduled`)
  - `reason`, `cancellation_reason`
  - `created_by`
  - `created_at`, `updated_at`
- **Important constraints**:
  - Unique constraint `uq_active_doctor_appointment_slot` on `(doctor_id, appointment_datetime, status)`.
- **Missing fields vs PRD**:
  - No queue linkage/token table
  - No full status lifecycle (only statuses used in code: Scheduled/Confirmed/Checked in/Rescheduled/Cancelled)
  - No `no_show_risk_score`

---

## 5. Backend Architecture

### Routers
Implemented under `backend/app/api/v1/`:
- `auth.py` (auth + RBAC demo route)
- `patients.py` (patient CRUD + patient medical history endpoints)
- `doctors.py` (doctor CRUD + schedules)
- `appointments.py` (book, list, list slots, cancel, reschedule)

### Services
Implemented under `backend/app/services/`:
- `auth_service.py`: validates credentials and issues JWT
- `patient_service.py`: duplicate detection + patient code generation + history operations
- `doctor_service.py`: CRUD and schedule handling (implied by repository usage; model exists)
- `appointment_service.py`: slot listing from schedules + booking conflict checks + cancellation/reschedule

### Repositories
Implemented under `backend/app/repositories/`:
- `user_repository.py`: in-memory user store for demo accounts
- `patient_repository.py`: SQLAlchemy persistence and search
- `doctor_repository.py`: SQLAlchemy persistence and schedule CRUD
- `appointment_repository.py`: SQLAlchemy persistence, conflict detection, schedule lookup, and slot availability derivation

### Authentication & RBAC
- `backend/app/core/security.py`
  - Password hashing: PBKDF2-SHA256 (custom helper)
  - JWT creation/decoding using `python-jose`
  - RBAC via `require_roles(*allowed_roles)` dependency

### Database
- `backend/app/database/session.py` provides `get_db()` dependency
- Alembic present; migrations live under `backend/app/database/migrations/`

### Migrations
- One primary migration exists for patient tables and history (`20260617_0001*` pattern).
- Doctor and appointment migrations may exist depending on repository state (not fully enumerated here; see `backend/app/database/migrations/`).

---

## 6. Frontend Architecture

### Pages (Next.js App Router)
Implemented routes present in repo:
- Auth
  - `/login` (`frontend/app/(auth)/login/page.tsx`)
- Patient portal
  - `/dashboard` (`frontend/app/(patient)/dashboard/page.tsx`)
  - `/profile` (`frontend/app/(patient)/profile/page.tsx`)
  - `/medical-records` (`frontend/app/(patient)/medical-records/page.tsx`)
- Admin patient management
  - `/patients` (`frontend/app/(admin)/patients/page.tsx`)
  - `/patients/register` (`frontend/app/(admin)/patients/register/page.tsx`)

### Components / Layouts
- `frontend/app/layout.tsx`, `globals.css` exist.
- `frontend/components/` and `frontend/features/` folders exist but are largely placeholders in current tree.

### Hooks
- `frontend/hooks/` exists but no concrete hook files were enumerated in this run.

### API services
- `frontend/services/auth.service.ts`, `patient.service.ts`, `doctor.service.ts`, `appointment.service.ts` exist (tree present; only auth/patient are confirmed by page usage).

### Routing
- No Next.js server-side route protection is enforced; `middleware.ts` exists but route matcher is empty.
- Authorization is effectively “best effort” and relies on backend RBAC for correctness.

### State management
- Pages use local React `useState/useEffect` and browser `localStorage`.

---

## 7. Existing Features (Implemented vs Missing)

> Determined strictly from what exists in backend routes + frontend pages/components.

### Authentication
- ✅ Complete (backend JWT + RBAC + frontend login)

### Patient Module
- ✅ Complete (backend patient CRUD + medical history endpoints + frontend patient dashboard/profile/medical-records)

### Doctor Module
- 🟡 Partially Implemented (backend doctor + schedule endpoints exist; frontend doctor UX not verified)

### Appointment Module
- 🟡 Partially Implemented (backend appointment + slots + cancel/reschedule exist; frontend booking UI not verified)

### Queue Management
- ❌ Missing (no queue APIs/models/frontend)

### Billing
- ❌ Missing (no billing APIs/models/frontend)

### Dashboard (basic)
- 🟡 Partially Implemented (patient dashboard exists; admin/doctor dashboards not present as pages)

### AI Features
- ❌ Missing (no Gemini integration in codebase yet)

### Inventory / Laboratory
- ❌ Missing

### Notifications
- ❌ Missing

---

## 8. Current APIs (Backend)

> Grouped by module. Prefix is `/api/v1`.

### Authentication (`backend/app/api/v1/auth.py`)
- `POST /auth/login`
- `GET /auth/me`
- `GET /auth/admin-only` (RBAC demo route)

### Patients (`backend/app/api/v1/patients.py`)
- `POST /patients` (admin)
- `GET /patients` (admin/doctor search)
- `GET /patients/me` (patient)
- `GET /patients/me/medical-history` (patient)
- `GET /patients/{patient_id}` (admin/doctor)
- `PATCH /patients/{patient_id}` (admin)
- `POST /patients/{patient_id}/medical-history` (admin/doctor)
- `GET /patients/{patient_id}/medical-history` (admin/doctor)

### Doctors (`backend/app/api/v1/doctors.py`)
- `POST /doctors` (admin)
- `GET /doctors` (admin/doctor/patient)
- `GET /doctors/me` (doctor)
- `GET /doctors/me/schedule` (doctor)
- `GET /doctors/{doctor_id}` (admin/doctor/patient)
- `PATCH /doctors/{doctor_id}` (admin)
- `POST /doctors/{doctor_id}/schedule` (admin)
- `GET /doctors/{doctor_id}/schedule` (admin/doctor/patient)

### Appointments (`backend/app/api/v1/appointments.py`)
- `POST /appointments` (admin/doctor/patient)
- `GET /appointments` (admin/doctor/patient)
- `GET /appointments/slots?doctor_id=&slot_date=` (admin/doctor/patient)
- `GET /appointments/{appointment_id}` (admin/doctor/patient)
- `POST /appointments/{appointment_id}/cancel` (admin/doctor/patient)
- `POST /appointments/{appointment_id}/reschedule` (admin/doctor/patient)

---

## 9. Current Frontend Pages

### Auth
- `/login`

### Patient
- `/dashboard`
- `/profile`
- `/medical-records`

### Admin
- `/patients`
- `/patients/register`

### Doctor
- No doctor portal pages verified in current tree during this analysis run.

---

## 10. Current Database Tables

Implemented SQLAlchemy tables correspond to these current models:
- `patients`
- `patient_medical_history`
- `doctors`
- `doctor_schedules`
- `appointments`

---

## 11. Existing Tests

### Backend tests
- `backend/tests/test_auth.py`
  - login success + invalid credentials
  - RBAC allow/deny checks
- `backend/tests/test_patients.py`
  - admin patient registration
  - RBAC patient/doctor/admin behavior
  - medical history create/read flows
- `backend/tests/test_doctors.py`
  - admin doctor creation
  - schedule creation and reading
  - RBAC checks and doctor schedule access
- `backend/tests/test_appointments.py`
  - list available slots from schedules
  - patient booking and calendar listing
  - double-booking conflict detection
  - cancel/reschedule behavior
  - booking outside schedule rejection

### Frontend tests
- Present as unit tests folder; specific coverage beyond helper tests not verified in this run.

---

## 12. Technical Debt & Gaps

### Duplicate / missing modules
- PRD and `docs/architecture.md` describe many modules (queue, billing, AI, audit logs), but the codebase only implements auth/patients and partial doctor/appointments.

### Dead/placeholder code
- `frontend/components/*` and `frontend/features/*` exist mostly as empty `.gitkeep` directories.

### Missing validation / feature parity
- Queue, billing, AI, and full EHR are missing entirely.
- `frontend/middleware.ts` exists but does not enforce route protection.

### Security issues (current)
- Auth token stored in `localStorage` (higher XSS risk than httpOnly cookies).
- Demo users in-memory (`UserRepository`) instead of persistent identity in PostgreSQL.

### Performance issues
- Current backend uses synchronous SQLAlchemy calls with simple search; acceptable for MVP.
- Slot availability generation derives slots dynamically per request; ok for MVP but may require indexing/optimization later.

### Architecture issues
- Frontend uses client-side checks and relies on backend RBAC; lack of server route protection can degrade UX.
- Backend uses “name strings” in medical history (`doctor_name`, `department`) rather than foreign keys to doctor/department entities (breaks normalization vs PRD).

---

## 13. Roadmap Progress (vs `ROADMAP.md`)

> This table maps documented roadmap modules to current code reality.

| Module | Progress |
|---|---|
| Authentication | ✅ 100% |
| Patient Module | ✅ 100% |
| Doctor Module | 🟡 Backend exists; full frontend/module UX incomplete |
| Appointment Module | 🟡 Backend exists; full frontend integration incomplete |
| Queue Management | ❌ Missing |
| Billing | ❌ Missing |
| Medical Records (Full EHR) | ❌ Missing (only medical history timeline implemented) |
| Deployment | 🟡 Docker exists for backend DB; full release pipeline not present |
| Testing | 🟡 Backend tests exist; frontend coverage not verified beyond helpers |
| AI Features | ❌ Missing |

---

## 14. NEXT_STEPS.md (Milestones)

### Milestone 1 — Doctor Management UX + Data Integrity
- **Estimated difficulty**: M
- **Dependencies**: Auth + Patient done; Doctor backend exists
- **Files likely to change**:
  - `frontend/app/(doctor)/*` (add pages)
  - `frontend/components/*` (UI for doctor screens)
  - `frontend/services/doctor.service.ts` (API integration)
  - `backend/app/models/*`, `backend/app/api/v1/doctors.py` (if normalization is required)
- **Acceptance criteria**:
  - Doctor role can access doctor portal pages
  - Doctor can view/edit profile + manage schedules
  - RBAC-protected flows validated end-to-end

### Milestone 2 — Appointment Booking + Patient Scheduling UX
- **Estimated difficulty**: L
- **Dependencies**: Doctor + Appointment backend exists
- **Files likely to change**:
  - `frontend/app/(patient)/appointments/*` (new pages)
  - `frontend/services/appointment.service.ts`
  - Tailwind UI components for slot selection
- **Acceptance criteria**:
  - Patient can list available slots for a doctor
  - Patient can book/cancel/reschedule appointments
  - Calendar/list pages reflect backend state

### Milestone 3 — Queue Management (MVP demo)
- **Estimated difficulty**: L
- **Dependencies**: Appointment lifecycle
- **Files likely to change**:
  - Backend: new models + endpoints under `/api/v1/queues*` and `/patients/*/queue-status`
  - Frontend: `/queue` pages for patient and doctor
- **Acceptance criteria**:
  - Walk-in tokens or token creation after appointment check-in
  - Call-next workflow and patient queue position updates

### Milestone 4 — Billing (Invoices + payments)
- **Estimated difficulty**: L
- **Dependencies**: Patient (and optionally appointment)
- **Files likely to change**:
  - Backend: billing models + `/api/v1/invoices*`
  - Frontend: patient billing pages + invoice views
- **Acceptance criteria**:
  - Invoice creation and list
  - Payment recording and status updates

### Milestone 5 — Full Medical Records / EHR Expansion
- **Estimated difficulty**: L
- **Dependencies**: Appointments/Visits
- **Files likely to change**:
  - Backend: visits/records/prescriptions/lab order/document tables + endpoints
  - Frontend: EHR timeline + record viewer
- **Acceptance criteria**:
  - Patient timeline includes structured visits and documents
  - Doctor can create/update clinical notes linked to entities

### Milestone 6 — AI Layer (Phase 2)
- **Estimated difficulty**: XL
- **Dependencies**: Gemini integration layer + storage
- **Files likely to change**:
  - Backend: `/api/v1/ai/*` endpoints + Gemini adapter
  - Frontend: chatbot and report summary UI
- **Acceptance criteria**:
  - AI endpoints exist behind backend (not direct from UI)
  - Safety/disclaimer present
  - AI outputs are auditable

### Milestone 7 — Analytics + Portals + Deployment hardening
- **Estimated difficulty**: L+M
- **Dependencies**: operational modules (appointments/queue/billing)
- **Files likely to change**:
  - Frontend: admin dashboards
  - Backend: analytics endpoints (optional MVP with mocks)
  - Deployment: migration-on-release + env docs
- **Acceptance criteria**:
  - Admin KPIs visible
  - Dashboard data matches operational flows

---

*End of document.*

