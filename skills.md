# SmartCare AI Project Skills

## Project Overview

SmartCare AI is a production-grade Smart Hospital Management System designed to support patient management, doctor management, appointment booking, queue management, billing, medical records, and AI-assisted healthcare workflows.

The project should be built with clean architecture, secure engineering practices, reusable UI patterns, mobile-first design, accessibility, and automated testing as core expectations.

## Tech Stack

### Frontend

- Next.js 15
- TypeScript
- Tailwind CSS
- Mobile-first responsive design
- Reusable component architecture
- Accessible UI patterns

### Backend

- FastAPI
- Python
- RESTful API design
- Clean service, repository, and domain layering
- Strong request validation
- Background task support where needed

### Database

- PostgreSQL
- Relational schema design
- Transaction-safe workflows
- Indexing for search-heavy hospital operations
- Migration-based schema management

### AI

- Gemini API
- AI-assisted symptom analysis
- Medical report summarization
- Smart chatbot workflows
- Queue waiting time prediction support
- No-show prediction support
- Doctor workload optimization support

### Deployment

- Vercel for frontend deployment
- Railway for backend and database deployment
- Environment-based configuration
- CI-friendly build and test workflows

## Architecture Principles

### Clean Architecture

The system should separate concerns across clear layers:

- Presentation layer: pages, UI components, forms, and user interactions
- Application layer: use cases, workflows, orchestration, and validation
- Domain layer: business rules, entities, value objects, and policies
- Infrastructure layer: database access, external APIs, authentication, file storage, and AI integrations

Business rules should not be tightly coupled to frameworks, UI code, database queries, or third-party APIs.

### Frontend Structure

Frontend code should favor:

- Feature-based organization
- Shared reusable components
- Strong TypeScript types
- Server components where appropriate
- Client components only when interactivity is required
- Form validation with clear error states
- Consistent loading, empty, error, and success states

Recommended frontend areas:

- `app/` for Next.js routes and layouts
- `components/` for reusable UI
- `features/` for domain-specific screens and workflows
- `lib/` for shared utilities and API clients
- `types/` for shared TypeScript types
- `tests/` for frontend tests

### Backend Structure

Backend code should favor:

- Clear API route modules
- Pydantic schemas for request and response validation
- Service classes for business workflows
- Repository classes for database operations
- Dependency injection for database sessions, auth, and integrations
- Explicit error handling
- Testable domain logic

Recommended backend areas:

- `api/` for FastAPI routers
- `core/` for settings, security, logging, and shared configuration
- `models/` for database models
- `schemas/` for Pydantic schemas
- `services/` for business logic
- `repositories/` for persistence
- `integrations/` for Gemini API and external services
- `tests/` for backend tests

## Frontend Requirements

### Reusable Components

Build reusable components for repeated hospital workflows:

- Buttons
- Inputs
- Selects
- Date and time pickers
- Tables
- Pagination
- Modals
- Tabs
- Status badges
- Search filters
- Patient summary cards
- Appointment cards
- Billing line items
- Medical record timelines

Components should be typed, composable, accessible, and visually consistent.

### Mobile First

All screens must be designed for mobile first and progressively enhanced for tablet and desktop.

Important expectations:

- Responsive layouts
- Touch-friendly controls
- Readable text sizes
- Avoid horizontal scrolling
- Compact but usable tables on small screens
- Clear navigation for staff and patient portals

### Accessibility

The interface should follow WCAG 2.1 AA principles where practical.

Requirements:

- Semantic HTML
- Keyboard navigability
- Visible focus states
- Proper labels for form fields
- ARIA attributes only when needed
- Sufficient color contrast
- Error messages connected to inputs
- Screen-reader friendly status messages
- No interaction that depends only on color

## Backend Requirements

### API Design

APIs should be predictable, versioned, and secure.

Requirements:

- Use `/api/v1` route prefix
- Use consistent JSON response formats
- Use pagination for list endpoints
- Use filtering and sorting where needed
- Return appropriate HTTP status codes
- Validate all incoming data
- Avoid exposing internal errors
- Document APIs with OpenAPI

### Core Domains

Backend services should support the following domains:

- Patient management
- Doctor management
- Appointment booking
- Queue management
- Billing
- Medical records
- Authentication and authorization
- Notifications
- AI workflows

## Database Requirements

PostgreSQL should be used as the source of truth for transactional data.

Requirements:

- Use normalized relational models for core hospital data
- Use foreign keys for important relationships
- Use indexes for frequent searches and filters
- Use transactions for appointment booking, queue updates, billing, and payments
- Use migrations for schema changes
- Store large files in object storage, not directly in PostgreSQL
- Track `created_at` and `updated_at` for important entities
- Use soft deletes where legally and operationally appropriate

Important entities include:

- Users
- Roles
- Patients
- Doctors
- Departments
- Doctor schedules
- Appointments
- Queues
- Queue tokens
- Medical records
- Prescriptions
- Lab orders
- Medical documents
- Invoices
- Invoice items
- Payments
- AI interactions
- Audit logs

## AI Requirements

### Gemini API Integration

Gemini API usage should be isolated behind a dedicated integration layer.

Requirements:

- Do not call Gemini directly from UI components
- Keep prompts versioned and reviewable
- Store only necessary AI interaction metadata
- Avoid sending unnecessary patient data to AI services
- Add medical disclaimers where AI output may influence care decisions
- Mark AI-generated content clearly
- Allow doctors to review, edit, approve, or reject clinical AI summaries
- Log AI feature usage for monitoring and auditability

### AI Safety

AI must assist healthcare users, not replace clinicians.

The system must:

- Avoid presenting AI output as a final diagnosis
- Escalate emergency symptoms to urgent care guidance
- Support human review for medical summaries
- Monitor AI quality and failure cases
- Avoid discriminatory prediction factors
- Provide fallback behavior when Gemini API is unavailable

## Security Best Practices

Security must be treated as a core product requirement.

Requirements:

- Use secure authentication and authorization
- Apply role-based access control
- Hash passwords with a strong algorithm
- Use HTTPS in production
- Store secrets only in environment variables or secret managers
- Validate and sanitize all inputs
- Protect against OWASP Top 10 risks
- Rate-limit sensitive endpoints
- Avoid logging sensitive patient data
- Encrypt sensitive data at rest where required
- Use signed URLs for private medical documents
- Maintain audit logs for medical record access and billing changes
- Apply least privilege access to database and external services

## Testing Requirements

### Unit Testing

Unit tests are required for critical business logic.

Frontend tests should cover:

- Reusable components
- Form validation
- User interaction states
- Utility functions
- API client behavior

Backend tests should cover:

- Service logic
- Repository behavior
- API validation
- Authentication and authorization rules
- Appointment booking rules
- Queue status transitions
- Billing calculations
- AI integration fallback handling

### Test Quality

Tests should be:

- Fast
- Deterministic
- Easy to run locally
- Focused on behavior
- Included in CI before deployment

## Deployment Requirements

### Vercel

Use Vercel for the Next.js frontend.

Requirements:

- Configure production environment variables
- Run build checks before deployment
- Use preview deployments for pull requests
- Avoid exposing server-only secrets to the browser

### Railway

Use Railway for FastAPI backend and PostgreSQL.

Requirements:

- Configure backend environment variables securely
- Run database migrations during release workflow
- Configure health checks
- Monitor logs and errors
- Separate development, staging, and production environments where possible

## Code Quality Standards

All code should follow these standards:

- Strong typing
- Clear naming
- Small focused functions
- Minimal duplication
- Explicit error handling
- Consistent formatting
- No hardcoded secrets
- No unused code
- Meaningful tests for important behavior
- Clear separation between UI, business logic, data access, and integrations

## Definition of Done

A feature is considered complete when:

- Requirements are implemented
- UI is responsive and accessible
- Backend validation is in place
- Security implications are handled
- Unit tests are added or updated
- API changes are documented
- Database migrations are included when needed
- Errors, loading states, and empty states are handled
- The feature works in local development
- The implementation follows clean architecture principles
