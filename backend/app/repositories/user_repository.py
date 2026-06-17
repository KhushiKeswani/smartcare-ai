"""User persistence boundary for authentication."""

from dataclasses import dataclass

from app.core.security import UserRole


@dataclass(frozen=True)
class UserRecord:
    id: str
    name: str
    email: str
    role: UserRole
    password_hash: str
    is_active: bool = True


class UserRepository:
    def __init__(self) -> None:
        self._users_by_email = {
            "patient@smartcare.ai": UserRecord(
                id="user_patient_001",
                name="Priya Sharma",
                email="patient@smartcare.ai",
                role=UserRole.patient,
                password_hash="pbkdf2_sha256$60000$patient-auth-salt$eCGVlJc2c1x8whxELgj5i98ZYq0heGcqBhhfvrLEj30=",
            ),
            "doctor@smartcare.ai": UserRecord(
                id="user_doctor_001",
                name="Dr. Arjun Mehta",
                email="doctor@smartcare.ai",
                role=UserRole.doctor,
                password_hash="pbkdf2_sha256$60000$doctor-auth-salt$CNDR8nN1pQLl3Ia3GtkgWkX4R7J0m8hLPqtdMSfD2wY=",
            ),
            "admin@smartcare.ai": UserRecord(
                id="user_admin_001",
                name="Meera Rao",
                email="admin@smartcare.ai",
                role=UserRole.admin,
                password_hash="pbkdf2_sha256$60000$admin-auth-salt$hP22eShpcJUXbi0DCagIOB7zseFJc+fEa8CDWBYitpA=",
            ),
        }

    def get_by_email(self, email: str) -> UserRecord | None:
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> UserRecord | None:
        return next(
            (user for user in self._users_by_email.values() if user.id == user_id),
            None,
        )


user_repository = UserRepository()
