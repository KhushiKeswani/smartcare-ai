```text
smartcare-ai/
│
├── frontend/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   └── forgot-password/
│   │   │
│   │   ├── (patient)/
│   │   │   ├── dashboard/
│   │   │   ├── appointments/
│   │   │   ├── queue/
│   │   │   ├── medical-records/
│   │   │   ├── billing/
│   │   │   └── chatbot/
│   │   │
│   │   ├── (doctor)/
│   │   │   ├── dashboard/
│   │   │   ├── queue/
│   │   │   ├── appointments/
│   │   │   ├── patients/
│   │   │   ├── consultations/
│   │   │   ├── medical-records/
│   │   │   └── workload/
│   │   │
│   │   ├── (admin)/
│   │   │   ├── dashboard/
│   │   │   ├── patients/
│   │   │   ├── doctors/
│   │   │   ├── appointments/
│   │   │   ├── queues/
│   │   │   ├── billing/
│   │   │   ├── medical-records/
│   │   │   ├── ai-insights/
│   │   │   └── settings/
│   │   │
│   │   ├── api/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   ├── loading.tsx
│   │   ├── error.tsx
│   │   └── not-found.tsx
│   │
│   ├── components/
│   │   ├── ui/
│   │   ├── layout/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── charts/
│   │   ├── feedback/
│   │   ├── patient/
│   │   ├── doctor/
│   │   ├── admin/
│   │   ├── appointment/
│   │   ├── queue/
│   │   ├── billing/
│   │   ├── medical-records/
│   │   └── ai/
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── patients/
│   │   ├── doctors/
│   │   ├── appointments/
│   │   ├── queues/
│   │   ├── billing/
│   │   ├── medical-records/
│   │   ├── chatbot/
│   │   ├── ai/
│   │   └── admin/
│   │
│   ├── hooks/
│   │   ├── use-auth.ts
│   │   ├── use-debounce.ts
│   │   ├── use-pagination.ts
│   │   └── use-permissions.ts
│   │
│   ├── services/
│   │   ├── auth.service.ts
│   │   ├── patient.service.ts
│   │   ├── doctor.service.ts
│   │   ├── appointment.service.ts
│   │   ├── queue.service.ts
│   │   ├── billing.service.ts
│   │   ├── medical-record.service.ts
│   │   └── ai.service.ts
│   │
│   ├── lib/
│   │   ├── api-client.ts
│   │   ├── auth.ts
│   │   ├── constants.ts
│   │   ├── permissions.ts
│   │   ├── validations.ts
│   │   ├── utils.ts
│   │   └── config.ts
│   │
│   ├── types/
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   ├── patient.ts
│   │   ├── doctor.ts
│   │   ├── appointment.ts
│   │   ├── queue.ts
│   │   ├── billing.ts
│   │   ├── medical-record.ts
│   │   ├── ai.ts
│   │   └── api.ts
│   │
│   ├── styles/
│   ├── public/
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── accessibility/
│   │
│   ├── middleware.ts
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── __init__.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── patients.py
│   │   │       ├── doctors.py
│   │   │       ├── appointments.py
│   │   │       ├── queues.py
│   │   │       ├── billing.py
│   │   │       ├── medical_records.py
│   │   │       ├── documents.py
│   │   │       ├── ai.py
│   │   │       ├── notifications.py
│   │   │       └── admin.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── permissions.py
│   │   │   ├── exceptions.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── patient_service.py
│   │   │   ├── doctor_service.py
│   │   │   ├── appointment_service.py
│   │   │   ├── queue_service.py
│   │   │   ├── billing_service.py
│   │   │   ├── medical_record_service.py
│   │   │   ├── document_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── notification_service.py
│   │   │   └── audit_service.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── patient_repository.py
│   │   │   ├── doctor_repository.py
│   │   │   ├── appointment_repository.py
│   │   │   ├── queue_repository.py
│   │   │   ├── billing_repository.py
│   │   │   ├── medical_record_repository.py
│   │   │   ├── document_repository.py
│   │   │   ├── ai_repository.py
│   │   │   └── audit_repository.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── role.py
│   │   │   ├── patient.py
│   │   │   ├── doctor.py
│   │   │   ├── department.py
│   │   │   ├── appointment.py
│   │   │   ├── queue.py
│   │   │   ├── billing.py
│   │   │   ├── medical_record.py
│   │   │   ├── document.py
│   │   │   ├── ai.py
│   │   │   └── audit_log.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── doctor.py
│   │   │   ├── appointment.py
│   │   │   ├── queue.py
│   │   │   ├── billing.py
│   │   │   ├── medical_record.py
│   │   │   ├── document.py
│   │   │   ├── ai.py
│   │   │   └── common.py
│   │   │
│   │   ├── database/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── init_db.py
│   │   │   └── migrations/
│   │   │
│   │   ├── integrations/
│   │   │   ├── gemini/
│   │   │   │   ├── client.py
│   │   │   │   ├── prompts.py
│   │   │   │   └── safety.py
│   │   │   ├── storage/
│   │   │   ├── email/
│   │   │   ├── sms/
│   │   │   └── payments/
│   │   │
│   │   ├── workers/
│   │   │   ├── appointment_reminders.py
│   │   │   ├── queue_predictions.py
│   │   │   ├── report_summaries.py
│   │   │   └── cleanup_tasks.py
│   │   │
│   │   └── utils/
│   │       ├── pagination.py
│   │       ├── date_time.py
│   │       ├── validators.py
│   │       └── response.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── api/
│   │
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
│
├── database/
│   ├── migrations/
│   ├── seeds/
│   ├── schema/
│   └── backups/
│
├── docs/
│   ├── prd.md
│   ├── architecture.md
│   ├── api.md
│   ├── database.md
│   ├── security.md
│   ├── deployment.md
│   ├── ai.md
│   └── testing.md
│
├── prompts/
│   ├── symptom-analyzer.md
│   ├── report-summarizer.md
│   ├── chatbot.md
│   ├── queue-prediction.md
│   ├── workload-optimization.md
│   └── no-show-prediction.md
│
├── scripts/
│   ├── setup-dev.sh
│   ├── run-tests.sh
│   ├── migrate-db.sh
│   └── seed-db.sh
│
├── .github/
│   └── workflows/
│       ├── frontend-ci.yml
│       ├── backend-ci.yml
│       └── deploy.yml
│
├── .env.example
├── .gitignore
├── README.md
├── prd.md
└── skills.md
```

This structure keeps the project clean, scalable, testable, and aligned with the PRD plus `skills.md`: clean architecture, reusable components, mobile-first frontend, secure FastAPI backend, PostgreSQL persistence, Gemini AI integration, and deployment readiness for Vercel + Railway.