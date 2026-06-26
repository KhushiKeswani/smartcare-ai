"""Doctor database models."""

from datetime import datetime, time
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True, index=True)
    doctor_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    specialization: Mapped[str] = mapped_column(String(120), index=True)
    department: Mapped[str] = mapped_column(String(120), index=True)
    license_number: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    consultation_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="Active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    schedules: Mapped[list["DoctorSchedule"]] = relationship(
        back_populates="doctor",
        cascade="all, delete-orphan",
    )


class DoctorSchedule(Base):
    __tablename__ = "doctor_schedules"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    doctor_id: Mapped[str] = mapped_column(ForeignKey("doctors.id", ondelete="CASCADE"), index=True)
    day_of_week: Mapped[int] = mapped_column(Integer, index=True)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    slot_duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    max_patients: Mapped[int] = mapped_column(Integer, default=16)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    doctor: Mapped[Doctor] = relationship(back_populates="schedules")
