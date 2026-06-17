"""Authentication use cases."""

from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRecord, user_repository
from app.schemas.auth import AuthenticatedUser, TokenResponse


class AuthService:
    def authenticate(self, email: str, password: str) -> TokenResponse:
        user = user_repository.get_by_email(email)
        if not user or not user.is_active or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenResponse(
            access_token=create_access_token(subject=user.id, role=user.role),
            user=self._to_authenticated_user(user),
        )

    def get_current_user(self, user_id: str) -> AuthenticatedUser:
        user = user_repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authenticated user was not found",
            )
        return self._to_authenticated_user(user)

    @staticmethod
    def _to_authenticated_user(user: UserRecord) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
        )


auth_service = AuthService()
