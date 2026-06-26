1. System Architecture
SmartCare AI should use a modular monolith architecture for the MVP, with clean domain boundaries. This is simpler to deploy on Vercel + Railway while still allowing future extraction into microservices.
Users
  |
  | Web / Mobile Browser
  v
Next.js 15 Frontend on Vercel
  |
  | HTTPS REST API
  v
FastAPI Backend on Railway
  |
  |---------------- PostgreSQL
  |---------------- Object Storage
  |---------------- Gemini API
  |---------------- Notification Providers
  |---------------- Background Jobs
Main layers:
Presentation Layer
- Next.js pages
- Staff dashboard
- Doctor dashboard
- Patient portal
- Admin portal

API Layer
- FastAPI routers
- Request validation
- Response formatting
- Auth middleware

Application Layer
- Use cases
- Workflow orchestration
- Business validations

Domain Layer
- Entities
- Policies
- Status transitions
- Business rules

Infrastructure Layer
- PostgreSQL repositories
- Gemini API integration
- File storage
- Email/SMS/WhatsApp providers
- Logging and audit systems
Recommended deployment:
Vercel
- Next.js frontend
- Static assets
- Server components
- Route protection

Railway
- FastAPI backend
- PostgreSQL database
- Background worker
- Scheduled jobs
- Environment secrets
2. Folder Structure
Recommended repository structure:
smartcare-ai/
  README.md
  prd.md
  skills.md

  frontend/
    app/
      layout.tsx
      page.tsx
      login/
      dashboard/
      patients/
      doctors/
      appointments/
      queue/
      billing/
      medical-records/
      ai/
      admin/

    components/
      ui/
      forms/
      tables/
      layout/
      feedback/
      medical/
      billing/
      queue/

    features/
      auth/
      patients/
      doctors/
      appointments/
      queue/
      billing/
      medical-records/
      ai-chatbot/
      reports/
      admin/

    lib/
      api/
      auth/
      config/
      validation/
      utils/

    hooks/
    types/
    styles/
    tests/

  backend/
    app/
      main.py

      api/
        v1/
          auth.py
          patients.py
          doctors.py
          appointments.py
          queues.py
          billing.py
          medical_records.py
          documents.py
          ai.py
          admin.py

      core/
        config.py
        security.py
        permissions.py
        logging.py
        errors.py

      domain/
        users/
        patients/
        doctors/
        appointments/
        queues/
        billing/
        medical_records/
        ai/
        audit/

      schemas/
        auth.py
        patients.py
        doctors.py
        appointments.py
        queues.py
        billing.py
        medical_records.py
        ai.py

      services/
        auth_service.py
        patient_service.py
        doctor_service.py
        appointment_service.py
        queue_service.py
        billing_service.py
        medical_record_service.py
        ai_service.py
        notification_service.py
        audit_service.py

      repositories/
        user_repository.py
        patient_repository.py
        doctor_repository.py
        appointment_repository.py
        queue_repository.py
        billing_repository.py
        medical_record_repository.py
        audit_repository.py

      integrations/
        gemini/
        email/
        sms/
        whatsapp/
        storage/

      db/
        session.py
        base.py
        migrations/

      workers/
        reminder_worker.py
        ai_summary_worker.py
        queue_prediction_worker.py

      tests/
        unit/
        integration/

  docs/
    architecture.md
    api.md
    database.md
    security.md
3. Service Architecture
Core backend services:
Auth Service
- Login
- Refresh token
- Password reset
- Role-based access control
- Permission checks

Patient Service
- Patient registration
- Duplicate detection
- Patient profile updates
- Patient timeline
- Insurance and emergency contacts

Doctor Service
- Doctor profile management
- Department assignment
- Schedule management
- Leave handling
- Workload metrics

Appointment Service
- Slot availability
- Appointment booking
- Rescheduling
- Cancellation
- Check-in
- No-show marking

Queue Service
- Token generation
- Queue ordering
- Priority handling
- Call-next workflow
- Real-time queue status
- Waiting time updates

Billing Service
- Invoice generation
- Invoice line items
- Taxes and discounts
- Payments
- Refunds
- Outstanding balances

Medical Record Service
- Consultation notes
- Diagnosis
- Prescriptions
- Lab orders
- Medical documents
- Patient medical history

AI Service
- Gemini API orchestration
- Symptom analyzer
- Report summarization
- Chatbot
- Queue wait prediction
- No-show prediction
- Doctor workload recommendations

Notification Service
- Appointment reminders
- Queue updates
- Payment notifications
- Report availability alerts

Audit Service
- Medical record access logs
- Billing change logs
- Auth logs
- Permission changes
- AI interaction logs
Service dependency flow:
API Router
  -> Service
    -> Repository
      -> PostgreSQL

AI Service
  -> Gemini Integration
  -> AI Interaction Repository
  -> Audit Service

Appointment Service
  -> Doctor Service
  -> Patient Service
  -> Queue Service
  -> Notification Service

Billing Service
  -> Patient Repository
  -> Appointment Repository
  -> Audit Service
4. Database Architecture
Use PostgreSQL as the transactional source of truth.
Core schema groups:
Identity and Access
- users
- roles
- permissions
- role_permissions
- user_sessions
- password_reset_tokens

Hospital Organization
- branches
- departments
- rooms
- services

Patients
- patients
- patient_contacts
- patient_insurance
- patient_allergies
- patient_conditions

Doctors
- doctors
- doctor_specialties
- doctor_schedules
- doctor_leaves

Appointments
- appointments
- appointment_status_history
- appointment_reminders

Queues
- queues
- queue_tokens
- queue_status_history

Medical Records
- visits
- medical_records
- prescriptions
- lab_orders
- medical_documents
- document_summaries

Billing
- invoices
- invoice_items
- payments
- refunds
- billing_adjustments

AI
- ai_interactions
- ai_prompt_versions
- ai_predictions
- chatbot_sessions
- chatbot_messages

Audit and Observability
- audit_logs
- security_events
- system_events
Important relationships:
users 1--1 doctors
users 1--1 patients, for patient portal accounts
departments 1--many doctors
patients 1--many appointments
doctors 1--many appointments
appointments 1--1 queue_tokens
appointments 1--many medical_records
patients 1--many medical_records
medical_records 1--many prescriptions
patients 1--many invoices
invoices 1--many invoice_items
invoices 1--many payments
patients 1--many medical_documents
medical_documents 1--many document_summaries
users 1--many audit_logs
Database requirements:
Indexes
- patients.patient_code
- patients.phone
- patients.email
- doctors.department_id
- appointments.patient_id
- appointments.doctor_id
- appointments.appointment_datetime
- appointments.status
- queue_tokens.queue_id
- queue_tokens.status
- invoices.patient_id
- invoices.status
- audit_logs.entity_type, entity_id

Constraints
- Unique patient_code
- Unique appointment_code
- Unique invoice_number
- Prevent duplicate doctor slot booking
- Foreign keys for all core relationships

Transactions
- Appointment booking
- Appointment check-in and queue token creation
- Queue call-next
- Invoice generation
- Payment recording
- Refund processing
Large files such as reports, scans, and PDFs should be stored in object storage. PostgreSQL should store metadata and secure file references only.
5. API Architecture
Use REST APIs under /api/v1.
API conventions:
Authentication
- Bearer token auth
- Refresh token flow
- Role and permission middleware

Response format
{
  "success": true,
  "data": {},
  "message": "Operation completed"
}

Error format
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": []
  }
}
Primary API groups:
Auth
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh-token
POST   /api/v1/auth/forgot-password

Patients
POST   /api/v1/patients
GET    /api/v1/patients
GET    /api/v1/patients/{patientId}
PATCH  /api/v1/patients/{patientId}
GET    /api/v1/patients/{patientId}/medical-history
GET    /api/v1/patients/{patientId}/queue-status

Doctors
POST   /api/v1/doctors
GET    /api/v1/doctors
GET    /api/v1/doctors/{doctorId}
PATCH  /api/v1/doctors/{doctorId}
GET    /api/v1/doctors/{doctorId}/schedule
POST   /api/v1/doctors/{doctorId}/schedule

Appointments
POST   /api/v1/appointments
GET    /api/v1/appointments
GET    /api/v1/appointments/{appointmentId}
PATCH  /api/v1/appointments/{appointmentId}
POST   /api/v1/appointments/{appointmentId}/cancel
POST   /api/v1/appointments/{appointmentId}/check-in

Queues
GET    /api/v1/queues
GET    /api/v1/queues/{queueId}
POST   /api/v1/queues/tokens
PATCH  /api/v1/queues/tokens/{tokenId}
POST   /api/v1/queues/{queueId}/call-next

Billing
POST   /api/v1/invoices
GET    /api/v1/invoices
GET    /api/v1/invoices/{invoiceId}
POST   /api/v1/invoices/{invoiceId}/payments
POST   /api/v1/invoices/{invoiceId}/refund

Medical Records
POST   /api/v1/medical-records
GET    /api/v1/patients/{patientId}/medical-records
GET    /api/v1/medical-records/{recordId}
PATCH  /api/v1/medical-records/{recordId}
POST   /api/v1/medical-documents

AI
POST   /api/v1/ai/symptom-analyzer
POST   /api/v1/ai/queue-wait-prediction
POST   /api/v1/ai/report-summary
POST   /api/v1/ai/chat
GET    /api/v1/ai/workload-recommendations
POST   /api/v1/ai/no-show-prediction
Cross-cutting API requirements:
- Pagination on list endpoints
- Filtering and sorting on operational lists
- OpenAPI documentation
- Request validation with Pydantic
- Consistent error codes
- Rate limiting for auth and AI endpoints
- Audit logging for sensitive actions
- Permission checks per route
- No sensitive patient data in logs