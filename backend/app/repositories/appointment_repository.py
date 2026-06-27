"""Appointment persistence operations."""

from datetime import date, datetime

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import DoctorSchedule
from app.schemas.appointment import AppointmentCreate


ACTIVE_APPOINTMENT_STATUSES = ("Scheduled", "Confirmed", "Checked in")


class AppointmentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: AppointmentCreate, appointment_code: str, created_by: str | None) -> Appointment:
        appointment = Appointment(
            appointment_code=appointment_code,
            created_by=created_by,
            **payload.model_dump(),
        )
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def get(self, appointment_id: str) -> Appointment | None:
        return self.db.get(Appointment, appointment_id)

    def search(
        self,
        *,
        doctor_id: str | None,
        patient_id: str | None,
        start_at: datetime | None,
        end_at: datetime | None,
        status: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Appointment], int]:
        statement = select(Appointment)
        count_statement = select(func.count()).select_from(Appointment)
        filters = []

        if doctor_id:
            filters.append(Appointment.doctor_id == doctor_id)
        if patient_id:
            filters.append(Appointment.patient_id == patient_id)
        if start_at:
            filters.append(Appointment.appointment_datetime >= start_at)
        if end_at:
            filters.append(Appointment.appointment_datetime <= end_at)
        if status:
            filters.append(Appointment.status == status)

        for item in filters:
            statement = statement.where(item)
            count_statement = count_statement.where(item)

        items = self.db.scalars(
            statement.order_by(Appointment.appointment_datetime.asc()).limit(limit).offset(offset)
        ).all()
        total = self.db.scalar(count_statement) or 0
        return list(items), total

    def has_conflict(
        self,
        *,
        doctor_id: str,
        appointment_datetime: datetime,
        exclude_appointment_id: str | None = None,
    ) -> bool:
        statement = select(Appointment.id).where(
            and_(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_datetime == appointment_datetime,
                Appointment.status.in_(ACTIVE_APPOINTMENT_STATUSES),
            )
        )
        if exclude_appointment_id:
            statement = statement.where(Appointment.id != exclude_appointment_id)
        return self.db.scalar(statement) is not None

    def update_datetime(self, appointment: Appointment, appointment_datetime: datetime) -> Appointment:
        appointment.appointment_datetime = appointment_datetime
        appointment.status = "Rescheduled"
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def cancel(self, appointment: Appointment, cancellation_reason: str | None) -> Appointment:
        appointment.status = "Cancelled"
        appointment.cancellation_reason = cancellation_reason
        self.db.commit()
        self.db.refresh(appointment)
        return appointment

    def list_doctor_schedules_for_day(self, doctor_id: str, day_of_week: int) -> list[DoctorSchedule]:
        return list(
            self.db.scalars(
                select(DoctorSchedule)
                .where(
                    DoctorSchedule.doctor_id == doctor_id,
                    DoctorSchedule.day_of_week == day_of_week,
                    DoctorSchedule.is_active.is_(True),
                )
                .order_by(DoctorSchedule.start_time)
            ).all()
        )

    def list_booked_slots(self, doctor_id: str, slot_date: date) -> set[datetime]:
        start_at = datetime.combine(slot_date, datetime.min.time())
        end_at = datetime.combine(slot_date, datetime.max.time())
        return set(
            self.db.scalars(
                select(Appointment.appointment_datetime).where(
                    Appointment.doctor_id == doctor_id,
                    Appointment.appointment_datetime >= start_at,
                    Appointment.appointment_datetime <= end_at,
                    Appointment.status.in_(ACTIVE_APPOINTMENT_STATUSES),
                )
            ).all()
        )
