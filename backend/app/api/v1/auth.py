"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import UserRole, require_roles
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    return auth_service.authenticate(payload.email, payload.password)


@router.get("/me", response_model=CurrentUserResponse)
def get_current_user(
    token_payload: Annotated[
        dict[str, str],
        Depends(require_roles(UserRole.patient, UserRole.doctor, UserRole.admin)),
    ],
) -> CurrentUserResponse:
    return CurrentUserResponse(
        user=auth_service.get_current_user(user_id=token_payload["sub"])
    )


@router.get("/admin-only")
def admin_only(
    _: Annotated[dict[str, str], Depends(require_roles(UserRole.admin))],
) -> dict[str, bool]:
    return {"allowed": True}
