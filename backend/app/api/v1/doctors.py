"""Doctor management API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import UserRole, require_roles
from app.database.session import get_db
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import (
    DoctorCreate,
    DoctorListResponse,
    DoctorResponse,
    DoctorScheduleCreate,
    DoctorScheduleResponse,
    DoctorUpdate,
)
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


def get_doctor_service(db: Annotated[Session, Depends(get_db)]) -> DoctorService:
    return DoctorService(DoctorRepository(db))


@router.post("", response_model=DoctorResponse, status_code=201)
def create_doctor(
    payload: DoctorCreate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.create_doctor(payload)


@router.get("", response_model=DoctorListResponse)
def search_doctors(
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
    q: str | None = None,
    specialization: str | None = None,
    available: bool | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = service.search_doctors(
        query=q,
        specialization=specialization,
        availability=available,
        limit=limit,
        offset=offset,
    )
    return DoctorListResponse(items=items, total=total)


@router.get("/me", response_model=DoctorResponse)
def get_my_doctor_profile(
    token_payload: Annotated[dict[str, str], Depends(require_roles(UserRole.doctor))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.get_profile_for_user(token_payload["sub"])


@router.get("/me/schedule", response_model=list[DoctorScheduleResponse])
def get_my_schedule(
    token_payload: Annotated[dict[str, str], Depends(require_roles(UserRole.doctor))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    doctor = service.get_profile_for_user(token_payload["sub"])
    return service.list_schedules(doctor.id)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: str,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.get_doctor(doctor_id)


@router.patch("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: str,
    payload: DoctorUpdate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.update_doctor(doctor_id, payload)


@router.post("/{doctor_id}/schedule", response_model=DoctorScheduleResponse, status_code=201)
def add_schedule(
    doctor_id: str,
    payload: DoctorScheduleCreate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.add_schedule(doctor_id, payload)


@router.get("/{doctor_id}/schedule", response_model=list[DoctorScheduleResponse])
def list_schedule(
    doctor_id: str,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor, UserRole.patient))],
    service: Annotated[DoctorService, Depends(get_doctor_service)],
):
    return service.list_schedules(doctor_id)
