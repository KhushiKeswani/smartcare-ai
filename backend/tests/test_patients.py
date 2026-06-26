from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models.patient import Patient


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


def patient_payload(**overrides):
    payload = {
        "first_name": "Priya",
        "last_name": "Sharma",
        "date_of_birth": "1990-01-15",
        "gender": "Female",
        "phone": "9876543210",
        "email": "priya@example.com",
        "address": "12 Park Road",
        "emergency_contact": "Rahul Sharma 9876500000",
        "blood_group": "B+",
        "insurance_provider": "Care Health",
        "insurance_number": "INS-1001",
    }
    payload.update(overrides)
    return payload


def test_admin_can_register_patient():
    response = client.post(
        "/api/v1/patients",
        json=patient_payload(user_id="user_patient_001"),
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["patient_code"].startswith("PAT-")
    assert body["first_name"] == "Priya"


def test_patient_role_cannot_register_patient():
    response = client.post(
        "/api/v1/patients",
        json=patient_payload(),
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 403


def test_doctor_can_search_patients():
    client.post(
        "/api/v1/patients",
        json=patient_payload(),
        headers=auth_headers("admin@smartcare.ai"),
    )

    response = client.get(
        "/api/v1/patients?q=Priya",
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["email"] == "priya@example.com"


def test_patient_can_view_linked_profile():
    client.post(
        "/api/v1/patients",
        json=patient_payload(user_id="user_patient_001"),
        headers=auth_headers("admin@smartcare.ai"),
    )

    response = client.get(
        "/api/v1/patients/me",
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["user_id"] == "user_patient_001"


def test_doctor_can_add_and_read_medical_history():
    created = client.post(
        "/api/v1/patients",
        json=patient_payload(),
        headers=auth_headers("admin@smartcare.ai"),
    ).json()

    history_response = client.post(
        f"/api/v1/patients/{created['id']}/medical-history",
        json={
            "visit_date": "2026-06-17",
            "doctor_name": "Dr. Arjun Mehta",
            "department": "Cardiology",
            "diagnosis": "Hypertension follow-up",
            "notes": "Continue monitoring blood pressure.",
        },
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert history_response.status_code == 201

    response = client.get(
        f"/api/v1/patients/{created['id']}/medical-history",
        headers=auth_headers("doctor@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()[0]["diagnosis"] == "Hypertension follow-up"


def test_patient_can_read_own_medical_history():
    created = client.post(
        "/api/v1/patients",
        json=patient_payload(user_id="user_patient_001"),
        headers=auth_headers("admin@smartcare.ai"),
    ).json()
    client.post(
        f"/api/v1/patients/{created['id']}/medical-history",
        json={
            "visit_date": "2026-06-17",
            "doctor_name": "Dr. Arjun Mehta",
            "department": "Cardiology",
            "diagnosis": "Hypertension follow-up",
            "notes": "Continue monitoring blood pressure.",
        },
        headers=auth_headers("doctor@smartcare.ai"),
    )

    response = client.get(
        "/api/v1/patients/me/medical-history",
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()[0]["patient_id"] == created["id"]
