"""Patient API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import UserRole, require_roles
from app.database.session import get_db
from app.repositories.patient_repository import PatientRepository
from app.schemas.patient import (
    MedicalHistoryCreate,
    MedicalHistoryResponse,
    PatientCreate,
    PatientListResponse,
    PatientResponse,
    PatientUpdate,
)
from app.services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patients"])


def get_patient_service(db: Annotated[Session, Depends(get_db)]) -> PatientService:
    return PatientService(PatientRepository(db))


@router.post("", response_model=PatientResponse, status_code=201)
def register_patient(
    payload: PatientCreate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.register_patient(payload)


@router.get("", response_model=PatientListResponse)
def search_patients(
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor))],
    service: Annotated[PatientService, Depends(get_patient_service)],
    q: str | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    items, total = service.search_patients(query=q, limit=limit, offset=offset)
    return PatientListResponse(items=items, total=total)


@router.get("/me", response_model=PatientResponse)
def get_my_profile(
    token_payload: Annotated[dict[str, str], Depends(require_roles(UserRole.patient))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.get_profile_for_user(token_payload["sub"])


@router.get("/me/medical-history", response_model=list[MedicalHistoryResponse])
def get_my_medical_history(
    token_payload: Annotated[dict[str, str], Depends(require_roles(UserRole.patient))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    patient = service.get_profile_for_user(token_payload["sub"])
    return service.list_medical_history(patient.id)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.get_patient(patient_id)


@router.patch("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: str,
    payload: PatientUpdate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.update_patient(patient_id, payload)


@router.post("/{patient_id}/medical-history", response_model=MedicalHistoryResponse, status_code=201)
def add_medical_history(
    patient_id: str,
    payload: MedicalHistoryCreate,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.add_medical_history(patient_id, payload)


@router.get("/{patient_id}/medical-history", response_model=list[MedicalHistoryResponse])
def list_medical_history(
    patient_id: str,
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin, UserRole.doctor))],
    service: Annotated[PatientService, Depends(get_patient_service)],
):
    return service.list_medical_history(patient_id)
