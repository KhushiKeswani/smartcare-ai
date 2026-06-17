"""Patient API schemas."""

from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class PatientBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    gender: str = Field(min_length=1, max_length=32)
    phone: str = Field(min_length=7, max_length=32)
    email: EmailStr | None = None
    address: str | None = None
    emergency_contact: str | None = None
    blood_group: str | None = Field(default=None, max_length=8)
    insurance_provider: str | None = None
    insurance_number: str | None = None


class PatientCreate(PatientBase):
    user_id: str | None = None


class PatientUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, min_length=7, max_length=32)
    email: EmailStr | None = None
    address: str | None = None
    emergency_contact: str | None = None
    blood_group: str | None = Field(default=None, max_length=8)
    insurance_provider: str | None = None
    insurance_number: str | None = None


class PatientResponse(PatientBase):
    id: str
    patient_code: str
    user_id: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MedicalHistoryCreate(BaseModel):
    visit_date: date
    doctor_name: str = Field(min_length=1, max_length=160)
    department: str = Field(min_length=1, max_length=120)
    diagnosis: str = Field(min_length=1, max_length=255)
    notes: str | None = None


class MedicalHistoryResponse(MedicalHistoryCreate):
    id: str
    patient_id: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PatientListResponse(BaseModel):
    items: list[PatientResponse]
    total: int
