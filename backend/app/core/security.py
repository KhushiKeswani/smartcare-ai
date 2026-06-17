"""Authentication and authorization helpers."""

from datetime import UTC, datetime, timedelta
from enum import StrEnum
import base64
import hashlib
import hmac
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings


class UserRole(StrEnum):
    patient = "Patient"
    doctor = "Doctor"
    admin = "Admin"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def hash_password(password: str) -> str:
    iterations = 120_000
    salt = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())[:16]
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return (
        f"pbkdf2_sha256${iterations}${salt.decode()}$"
        f"{base64.b64encode(digest).decode()}"
    )


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected_hash = password_hash.split("$", 3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode(),
        salt.encode(),
        int(iterations),
    )
    candidate_hash = base64.b64encode(digest).decode()
    return hmac.compare_digest(candidate_hash, expected_hash)


def create_access_token(subject: str, role: UserRole) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    payload = {
        "sub": subject,
        "role": role.value,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, str]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def require_roles(*allowed_roles: UserRole):
    def dependency(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
        payload = decode_access_token(token)
        role = payload.get("role")
        if role not in {allowed_role.value for allowed_role in allowed_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return payload

    return dependency
