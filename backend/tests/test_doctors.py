from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.base import Base
from app.database.session import get_db
from app.main import app


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)


def setup_function() -> None:
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_token(email: str) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "Password123"},
    )
    return response.json()["access_token"]


def auth_headers(email: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {get_token(email)}"}


def doctor_payload(**overrides):
    payload = {
        "first_name": "Arjun",
        "last_name": "Mehta",
        "email": "arjun.mehta@example.com",
        "phone": "9988776655",
        "specialization": "Cardiology",
        "department": "Cardiology",
        "license_number": "MED-12345",
        "consultation_fee": 800,
        "bio": "Senior cardiologist",
        "is_available": True,
    }
    payload.update(overrides)
    return payload


def create_doctor(**overrides):
    return client.post(
        "/api/v1/doctors",
        json=doctor_payload(**overrides),
        headers=auth_headers("admin@smartcare.ai"),
    )


def test_admin_can_create_doctor_profile():
    response = create_doctor(user_id="user_doctor_001")

    assert response.status_code == 201
    body = response.json()
    assert body["doctor_code"].startswith("DOC-")
    assert body["specialization"] == "Cardiology"


def test_patient_cannot_create_doctor_profile():
    response = client.post(
        "/api/v1/doctors",
        json=doctor_payload(),
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 403


def test_search_doctors_by_specialization_and_availability():
    create_doctor()

    response = client.get(
        "/api/v1/doctors?specialization=Cardiology&available=true",
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["department"] == "Cardiology"


def test_doctor_can_view_linked_profile():
    create_doctor(user_id="user_doctor_001")

    response = client.get(
        "/api/v1/doctors/me",
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == "user_doctor_001"


def test_admin_can_update_doctor_availability():
    doctor = create_doctor().json()

    response = client.patch(
        f"/api/v1/doctors/{doctor['id']}",
        json={"is_available": False},
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["is_available"] is False


def test_admin_can_create_and_read_doctor_schedule():
    doctor = create_doctor().json()

    schedule_response = client.post(
        f"/api/v1/doctors/{doctor['id']}/schedule",
        json={
            "day_of_week": 1,
            "start_time": "09:00:00",
            "end_time": "13:00:00",
            "slot_duration_minutes": 30,
            "max_patients": 12,
            "is_active": True,
        },
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert schedule_response.status_code == 201

    response = client.get(
        f"/api/v1/doctors/{doctor['id']}/schedule",
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()[0]["day_of_week"] == 1


def test_doctor_can_read_own_schedule():
    doctor = create_doctor(user_id="user_doctor_001").json()
    client.post(
        f"/api/v1/doctors/{doctor['id']}/schedule",
        json={
            "day_of_week": 2,
            "start_time": "10:00:00",
            "end_time": "15:00:00",
            "slot_duration_minutes": 20,
            "max_patients": 15,
        },
        headers=auth_headers("admin@smartcare.ai"),
    )

    response = client.get(
        "/api/v1/doctors/me/schedule",
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()[0]["doctor_id"] == doctor["id"]
