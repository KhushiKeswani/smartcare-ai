"""Patient use cases."""

from fastapi import HTTPException, status

from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import MedicalHistoryCreate, PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, repository: PatientRepository) -> None:
        self.repository = repository

    def register_patient(self, payload: PatientCreate):
        if self.repository.exists_by_contact(payload.phone, payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A patient with this phone or email already exists",
            )

        code = self._generate_patient_code()
        return self.repository.create(payload, patient_code=code)

    def get_patient(self, patient_id: str):
        patient = self.repository.get(patient_id)
        if not patient:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        return patient

    def get_profile_for_user(self, user_id: str):
        patient = self.repository.get_by_user_id(user_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No patient profile is linked to this user",
            )
        return patient

    def search_patients(self, query: str | None, limit: int, offset: int):
        return self.repository.search(query=query, limit=limit, offset=offset)

    def update_patient(self, patient_id: str, payload: PatientUpdate):
        patient = self.get_patient(patient_id)
        return self.repository.update(patient, payload)

    def add_medical_history(self, patient_id: str, payload: MedicalHistoryCreate):
        self.get_patient(patient_id)
        return self.repository.add_history(patient_id, payload)

    def list_medical_history(self, patient_id: str):
        self.get_patient(patient_id)
        return self.repository.list_history(patient_id)

    @staticmethod
    def _generate_patient_code() -> str:
        from uuid import uuid4

        return f"PAT-{uuid4().hex[:8].upper()}"
