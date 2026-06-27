"""Appointment booking API routes."""

from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import UserRole, require_roles
from app.database.session import get_db
from app.repositories.appointment_repository import AppointmentRepository
from app.repositories.doctor_repository import DoctorRepository
from app.repositories.patient_repository import PatientRepository
from app.schemas.appointment import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentListResponse,
    AppointmentReschedule,
    AppointmentResponse,
    AppointmentSlotResponse,
)
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def get_appointment_service(db: Annotated[Session, Depends(get_db)]) -> AppointmentService:
    return AppointmentService(
        AppointmentRepository(db),
        PatientRepository(db),
        DoctorRepository(db),
    )


@router.post("", response_model=AppointmentResponse, status_code=201)
def book_appointment(
    payload: AppointmentCreate,
    token_payload: Annotated[
        dict[str, str],
        Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient)),
    ],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return service.book_appointment(payload, created_by=token_payload["sub"])


@router.get("", response_model=AppointmentListResponse)
def list_appointments(
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
    doctor_id: str | None = None,
    patient_id: str | None = None,
    start_at: datetime | None = None,
    end_at: datetime | None = None,
    status: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    items, total = service.search_appointments(
        doctor_id=doctor_id,
        patient_id=patient_id,
        start_at=start_at,
        end_at=end_at,
        status=status,
        limit=limit,
        offset=offset,
    )
    return AppointmentListResponse(items=items, total=total)


@router.get("/slots", response_model=list[AppointmentSlotResponse])
def list_slots(
    doctor_id: str,
    slot_date: date,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return service.list_slots(doctor_id, slot_date)


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: str,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return service.get_appointment(appointment_id)


@router.post("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: str,
    payload: AppointmentCancel,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return service.cancel_appointment(appointment_id, payload.cancellation_reason)


@router.post("/{appointment_id}/reschedule", response_model=AppointmentResponse)
def reschedule_appointment(
    appointment_id: str,
    payload: AppointmentReschedule,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[AppointmentService, Depends(get_appointment_service)],
):
    return service.reschedule_appointment(appointment_id, payload)
