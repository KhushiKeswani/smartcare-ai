"""Doctor management use cases."""

from uuid import uuid4

from fastapi import HTTPException, status

from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import DoctorCreate, DoctorScheduleCreate, DoctorUpdate


class DoctorService:
    def __init__(self, repository: DoctorRepository) -> None:
        self.repository = repository

    def create_doctor(self, payload: DoctorCreate):
        if self.repository.exists_unique_fields(
            email=payload.email,
            phone=payload.phone,
            license_number=payload.license_number,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A doctor with this email, phone, or license already exists",
            )

        return self.repository.create(payload, doctor_code=self._generate_doctor_code())

    def get_doctor(self, doctor_id: str):
        doctor = self.repository.get(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor

    def get_profile_for_user(self, user_id: str):
        doctor = self.repository.get_by_user_id(user_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No doctor profile is linked to this user",
            )
        return doctor

    def search_doctors(
        self,
        query: str | None,
        specialization: str | None,
        availability: bool | None,
        limit: int,
        offset: int,
    ):
        return self.repository.search(
            query=query,
            specialization=specialization,
            availability=availability,
            limit=limit,
            offset=offset,
        )

    def update_doctor(self, doctor_id: str, payload: DoctorUpdate):
        doctor = self.get_doctor(doctor_id)
        return self.repository.update(doctor, payload)

    def add_schedule(self, doctor_id: str, payload: DoctorScheduleCreate):
        self.get_doctor(doctor_id)
        return self.repository.add_schedule(doctor_id, payload)

    def list_schedules(self, doctor_id: str):
        self.get_doctor(doctor_id)
        return self.repository.list_schedules(doctor_id)

    @staticmethod
    def _generate_doctor_code() -> str:
        return f"DOC-{uuid4().hex[:8].upper()}"
