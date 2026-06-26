"""Doctor API schemas."""

from datetime import datetime, time

from pydantic import BaseModel, EmailStr, Field, field_validator


class DoctorBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=32)
    specialization: str = Field(min_length=1, max_length=120)
    department: str = Field(min_length=1, max_length=120)
    license_number: str = Field(min_length=1, max_length=80)
    consultation_fee: float = Field(default=0, ge=0)
    bio: str | None = None
    is_available: bool = True


class DoctorCreate(DoctorBase):
    user_id: str | None = None


class DoctorUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=7, max_length=32)
    specialization: str | None = Field(default=None, min_length=1, max_length=120)
    department: str | None = Field(default=None, min_length=1, max_length=120)
    license_number: str | None = Field(default=None, min_length=1, max_length=80)
    consultation_fee: float | None = Field(default=None, ge=0)
    bio: str | None = None
    is_available: bool | None = None
    status: str | None = Field(default=None, min_length=1, max_length=32)


class DoctorResponse(DoctorBase):
    id: str
    user_id: str | None
    doctor_code: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DoctorListResponse(BaseModel):
    items: list[DoctorResponse]
    total: int


class DoctorScheduleCreate(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    slot_duration_minutes: int = Field(default=30, ge=5, le=240)
    max_patients: int = Field(default=16, ge=1, le=200)
    is_active: bool = True

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, end_time: time, info):
        start_time = info.data.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("end_time must be after start_time")
        return end_time


class DoctorScheduleResponse(DoctorScheduleCreate):
    id: str
    doctor_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
