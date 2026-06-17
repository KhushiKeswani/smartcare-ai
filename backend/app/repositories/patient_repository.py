"""Patient persistence operations."""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.patient import Patient, PatientMedicalHistory
from app.schemas.patient import MedicalHistoryCreate, PatientCreate, PatientUpdate


class PatientRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: PatientCreate, patient_code: str) -> Patient:
        patient = Patient(patient_code=patient_code, **payload.model_dump())
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def get(self, patient_id: str) -> Patient | None:
        return self.db.get(Patient, patient_id)

    def get_by_user_id(self, user_id: str) -> Patient | None:
        return self.db.scalar(select(Patient).where(Patient.user_id == user_id))

    def exists_by_contact(self, phone: str, email: str | None) -> bool:
        conditions = [Patient.phone == phone]
        if email:
            conditions.append(Patient.email == email)
        return self.db.scalar(select(Patient.id).where(or_(*conditions))) is not None

    def search(self, query: str | None, limit: int, offset: int) -> tuple[list[Patient], int]:
        statement = select(Patient)
        count_statement = select(func.count()).select_from(Patient)

        if query:
            pattern = f"%{query.lower()}%"
            filters = or_(
                func.lower(Patient.first_name).like(pattern),
                func.lower(Patient.last_name).like(pattern),
                func.lower(Patient.patient_code).like(pattern),
                func.lower(Patient.phone).like(pattern),
                func.lower(Patient.email).like(pattern),
            )
            statement = statement.where(filters)
            count_statement = count_statement.where(filters)

        items = self.db.scalars(
            statement.order_by(Patient.created_at.desc()).limit(limit).offset(offset)
        ).all()
        total = self.db.scalar(count_statement) or 0
        return list(items), total

    def update(self, patient: Patient, payload: PatientUpdate) -> Patient:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def add_history(
        self,
        patient_id: str,
        payload: MedicalHistoryCreate,
    ) -> PatientMedicalHistory:
        history = PatientMedicalHistory(patient_id=patient_id, **payload.model_dump())
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def list_history(self, patient_id: str) -> list[PatientMedicalHistory]:
        return list(
            self.db.scalars(
                select(PatientMedicalHistory)
                .where(PatientMedicalHistory.patient_id == patient_id)
                .order_by(PatientMedicalHistory.visit_date.desc())
            ).all()
        )
