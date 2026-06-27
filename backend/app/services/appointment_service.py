"""Appointment booking use cases."""

from datetime import date, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException, status

from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.patient_repository import PatientRepository
from app.schemas.appointment import AppointmentCreate, AppointmentReschedule, AppointmentSlotResponse


class AppointmentService:
    def __init__(
        self,
        repository: AppointmentRepository,
        patient_repository: PatientRepository,
        doctor_repository: DoctorRepository,
    ) -> None:
        self.repository = repository
        self.patient_repository = patient_repository
        self.doctor_repository = doctor_repository

    def book_appointment(self, payload: AppointmentCreate, created_by: str | None):
        self._ensure_patient_and_doctor(payload.patient_id, payload.doctor_id)
        self._ensure_slot_is_valid(payload.doctor_id, payload.appointment_datetime)
        self._ensure_no_conflict(payload.doctor_id, payload.appointment_datetime)
        return self.repository.create(
            payload,
            appointment_code=self._generate_appointment_code(),
            created_by=created_by,
        )

    def search_appointments(
        self,
        doctor_id: str | None,
        patient_id: str | None,
        start_at: datetime | None,
        end_at: datetime | None,
        status: str | None,
        limit: int,
        offset: int,
    ):
        return self.repository.search(
            doctor_id=doctor_id,
            patient_id=patient_id,
            start_at=start_at,
            end_at=end_at,
            status=status,
            limit=limit,
            offset=offset,
        )

    def get_appointment(self, appointment_id: str):
        appointment = self.repository.get(appointment_id)
        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
        return appointment

    def cancel_appointment(self, appointment_id: str, cancellation_reason: str | None):
        appointment = self.get_appointment(appointment_id)
        if appointment.status == "Cancelled":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Appointment is already cancelled",
            )
        return self.repository.cancel(appointment, cancellation_reason)

    def reschedule_appointment(self, appointment_id: str, payload: AppointmentReschedule):
        appointment = self.get_appointment(appointment_id)
        if appointment.status == "Cancelled":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cancelled appointments cannot be rescheduled",
            )
        self._ensure_slot_is_valid(appointment.doctor_id, payload.appointment_datetime)
        self._ensure_no_conflict(
            appointment.doctor_id,
            payload.appointment_datetime,
            exclude_appointment_id=appointment.id,
        )
        return self.repository.update_datetime(appointment, payload.appointment_datetime)

    def list_slots(self, doctor_id: str, slot_date: date) -> list[AppointmentSlotResponse]:
        doctor = self.doctor_repository.get(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

        schedules = self.repository.list_doctor_schedules_for_day(doctor_id, slot_date.weekday())
        booked_slots = self.repository.list_booked_slots(doctor_id, slot_date)
        slots: list[AppointmentSlotResponse] = []

        for schedule in schedules:
            current = datetime.combine(slot_date, schedule.start_time)
            end_boundary = datetime.combine(slot_date, schedule.end_time)
            while current + timedelta(minutes=schedule.slot_duration_minutes) <= end_boundary:
                slots.append(
                    AppointmentSlotResponse(
                        doctor_id=doctor_id,
                        slot_date=slot_date,
                        start_time=current.time(),
                        end_time=(current + timedelta(minutes=schedule.slot_duration_minutes)).time(),
                        is_available=current not in booked_slots,
                    )
                )
                current += timedelta(minutes=schedule.slot_duration_minutes)

        return slots

    def _ensure_patient_and_doctor(self, patient_id: str, doctor_id: str) -> None:
        if not self.patient_repository.get(patient_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        if not self.doctor_repository.get(doctor_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    def _ensure_slot_is_valid(self, doctor_id: str, appointment_datetime: datetime) -> None:
        available_slots = self.list_slots(doctor_id, appointment_datetime.date())
        if not any(slot.start_time == appointment_datetime.time() for slot in available_slots):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Selected appointment time is outside doctor availability",
            )

    def _ensure_no_conflict(
        self,
        doctor_id: str,
        appointment_datetime: datetime,
        exclude_appointment_id: str | None = None,
    ) -> None:
        if self.repository.has_conflict(
            doctor_id=doctor_id,
            appointment_datetime=appointment_datetime,
            exclude_appointment_id=exclude_appointment_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Selected appointment slot is already booked",
            )

    @staticmethod
    def _generate_appointment_code() -> str:
        return f"APT-{uuid4().hex[:8].upper()}"
