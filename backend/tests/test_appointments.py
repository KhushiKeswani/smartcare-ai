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


def patient_payload(**overrides):
    payload = {
        "first_name": "Priya",
        "last_name": "Sharma",
        "date_of_birth": "1990-01-15",
        "gender": "Female",
        "phone": "9876543210",
        "email": "priya@example.com",
    }
    payload.update(overrides)
    return payload


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
        "is_available": True,
    }
    payload.update(overrides)
    return payload


def setup_patient_doctor_and_schedule():
    patient = client.post(
        "/api/v1/patients",
        json=patient_payload(),
        headers=auth_headers("admin@smartcare.ai"),
    ).json()
    doctor = client.post(
        "/api/v1/doctors",
        json=doctor_payload(),
        headers=auth_headers("admin@smartcare.ai"),
    ).json()
    client.post(
        f"/api/v1/doctors/{doctor['id']}/schedule",
        json={
            "day_of_week": 0,
            "start_time": "09:00:00",
            "end_time": "11:00:00",
            "slot_duration_minutes": 30,
            "max_patients": 4,
        },
        headers=auth_headers("admin@smartcare.ai"),
    )
    return patient, doctor


def appointment_payload(patient_id: str, doctor_id: str, appointment_datetime="2026-06-29T09:00:00"):
    return {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "appointment_datetime": appointment_datetime,
        "appointment_type": "In-person",
        "reason": "Routine consultation",
    }


def test_lists_available_slots_from_doctor_schedule():
    _, doctor = setup_patient_doctor_and_schedule()

    response = client.get(
        f"/api/v1/appointments/slots?doctor_id={doctor['id']}&slot_date=2026-06-29",
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 4
    assert body[0]["start_time"] == "09:00:00"
    assert body[0]["is_available"] is True


def test_patient_can_book_appointment_and_calendar_lists_it():
    patient, doctor = setup_patient_doctor_and_schedule()

    response = client.post(
        "/api/v1/appointments",
        json=appointment_payload(patient["id"], doctor["id"]),
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 201
    assert response.json()["appointment_code"].startswith("APT-")

    calendar = client.get(
        f"/api/v1/appointments?doctor_id={doctor['id']}&start_at=2026-06-29T00:00:00&end_at=2026-06-29T23:59:59",
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert calendar.status_code == 200
    assert calendar.json()["total"] == 1


def test_conflict_detection_blocks_double_booking():
    patient, doctor = setup_patient_doctor_and_schedule()
    payload = appointment_payload(patient["id"], doctor["id"])

    client.post("/api/v1/appointments", json=payload, headers=auth_headers("patient@smartcare.ai"))
    response = client.post(
        "/api/v1/appointments",
        json=payload,
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert response.status_code == 409


def test_can_cancel_appointment():
    patient, doctor = setup_patient_doctor_and_schedule()
    appointment = client.post(
        "/api/v1/appointments",
        json=appointment_payload(patient["id"], doctor["id"]),
        headers=auth_headers("patient@smartcare.ai"),
    ).json()

    response = client.post(
        f"/api/v1/appointments/{appointment['id']}/cancel",
        json={"cancellation_reason": "Patient requested cancellation"},
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Cancelled"


def test_can_reschedule_to_available_slot():
    patient, doctor = setup_patient_doctor_and_schedule()
    appointment = client.post(
        "/api/v1/appointments",
        json=appointment_payload(patient["id"], doctor["id"]),
        headers=auth_headers("patient@smartcare.ai"),
    ).json()

    response = client.post(
        f"/api/v1/appointments/{appointment['id']}/reschedule",
        json={"appointment_datetime": "2026-06-29T09:30:00"},
        headers=auth_headers("admin@smartcare.ai"),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Rescheduled"
    assert response.json()["appointment_datetime"].startswith("2026-06-29T09:30:00")


def test_rejects_booking_outside_doctor_schedule():
    patient, doctor = setup_patient_doctor_and_schedule()

    response = client.post(
        "/api/v1/appointments",
        json=appointment_payload(patient["id"], doctor["id"], "2026-06-29T14:00:00"),
        headers=auth_headers("patient@smartcare.ai"),
    )

    assert response.status_code == 422
