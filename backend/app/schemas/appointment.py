"""Appointment API schemas."""

from datetime import date, datetime, time

from pydantic import BaseModel, Field, field_validator


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_datetime: datetime
    appointment_type: str = Field(default="In-person", min_length=1, max_length=40)
    reason: str | None = None


class AppointmentReschedule(BaseModel):
    appointment_datetime: datetime


class AppointmentCancel(BaseModel):
    cancellation_reason: str | None = None


class AppointmentResponse(BaseModel):
    id: str
    appointment_code: str
    patient_id: str
    doctor_id: str
    appointment_datetime: datetime
    appointment_type: str
    status: str
    reason: str | None
    cancellation_reason: str | None
    created_by: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AppointmentListResponse(BaseModel):
    items: list[AppointmentResponse]
    total: int


class AppointmentSlotResponse(BaseModel):
    doctor_id: str
    slot_date: date
    start_time: time
    end_time: time
    is_available: bool


class AppointmentCalendarRequest(BaseModel):
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def validate_date_range(cls, end_date: date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be on or after start_date")
        return end_date
