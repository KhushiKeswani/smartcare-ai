"""Doctor persistence operations."""

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.doctor import Doctor, DoctorSchedule
from app.schemas.doctor import DoctorCreate, DoctorScheduleCreate, DoctorUpdate


class DoctorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: DoctorCreate, doctor_code: str) -> Doctor:
        doctor = Doctor(doctor_code=doctor_code, **payload.model_dump())
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def get(self, doctor_id: str) -> Doctor | None:
        return self.db.get(Doctor, doctor_id)

    def get_by_user_id(self, user_id: str) -> Doctor | None:
        return self.db.scalar(select(Doctor).where(Doctor.user_id == user_id))

    def exists_unique_fields(
        self,
        *,
        email: str,
        phone: str,
        license_number: str,
    ) -> bool:
        return (
            self.db.scalar(
                select(Doctor.id).where(
                    or_(
                        Doctor.email == email,
                        Doctor.phone == phone,
                        Doctor.license_number == license_number,
                    )
                )
            )
            is not None
        )

    def search(
        self,
        query: str | None,
        specialization: str | None,
        availability: bool | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Doctor], int]:
        statement = select(Doctor)
        count_statement = select(func.count()).select_from(Doctor)
        filters = []

        if query:
            pattern = f"%{query.lower()}%"
            filters.append(
                or_(
                    func.lower(Doctor.first_name).like(pattern),
                    func.lower(Doctor.last_name).like(pattern),
                    func.lower(Doctor.doctor_code).like(pattern),
                    func.lower(Doctor.department).like(pattern),
                    func.lower(Doctor.specialization).like(pattern),
                    func.lower(Doctor.email).like(pattern),
                )
            )

        if specialization:
            filters.append(func.lower(Doctor.specialization) == specialization.lower())

        if availability is not None:
            filters.append(Doctor.is_available == availability)

        for item in filters:
            statement = statement.where(item)
            count_statement = count_statement.where(item)

        items = self.db.scalars(
            statement.order_by(Doctor.created_at.desc()).limit(limit).offset(offset)
        ).all()
        total = self.db.scalar(count_statement) or 0
        return list(items), total

    def update(self, doctor: Doctor, payload: DoctorUpdate) -> Doctor:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(doctor, field, value)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def add_schedule(
        self,
        doctor_id: str,
        payload: DoctorScheduleCreate,
    ) -> DoctorSchedule:
        schedule = DoctorSchedule(doctor_id=doctor_id, **payload.model_dump())
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule

    def list_schedules(self, doctor_id: str) -> list[DoctorSchedule]:
        return list(
            self.db.scalars(
                select(DoctorSchedule)
                .where(DoctorSchedule.doctor_id == doctor_id)
                .order_by(DoctorSchedule.day_of_week, DoctorSchedule.start_time)
            ).all()
        )
