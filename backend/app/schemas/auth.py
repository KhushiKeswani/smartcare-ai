"""Authentication schemas."""

from pydantic import BaseModel, EmailStr, Field

from app.core.security import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class AuthenticatedUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthenticatedUser


class CurrentUserResponse(BaseModel):
    user: AuthenticatedUser
