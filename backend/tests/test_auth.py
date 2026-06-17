from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_login_returns_jwt_for_patient_role():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "patient@smartcare.ai", "password": "Password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == "Patient"


def test_login_rejects_invalid_credentials():
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "patient@smartcare.ai", "password": "WrongPass123"},
    )

    assert response.status_code == 401


def test_rbac_allows_admin_access():
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@smartcare.ai", "password": "Password123"},
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"allowed": True}


def test_rbac_blocks_patient_from_admin_route():
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "patient@smartcare.ai", "password": "Password123"},
    )
    token = login.json()["access_token"]

    response = client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
