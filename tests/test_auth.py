"""Auth + health API tests (skipped automatically if fastapi/httpx/bcrypt/pymongo are not installed)."""
from tests.conftest import register


def test_health_ok(client, monkeypatch):
    from types import SimpleNamespace

    import app.main as main

    monkeypatch.setattr(main, "get_client", lambda: SimpleNamespace(admin=SimpleNamespace(command=lambda *_: {"ok": 1})))
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_health_reports_database_down(client, monkeypatch):
    import app.main as main

    def boom():
        raise RuntimeError("no db")

    monkeypatch.setattr(main, "get_client", boom)
    r = client.get("/api/health")
    assert r.status_code == 503 and r.json()["database"] == "unavailable"


def test_register_success_hides_password(client, fake_db):
    r = register(client)
    assert r.status_code == 201
    body = r.json()
    assert body["user"]["email"] == "alice@example.com" and body["access_token"]
    assert "password" not in r.text and "hashed" not in r.text
    stored = fake_db.users.find_one({"email": "alice@example.com"})
    assert stored["hashed_password"] != "correct-horse-1"
    assert stored["hashed_password"].startswith("$2")  # bcrypt


def test_register_duplicate_email(client):
    register(client)
    assert register(client, username="alice2").status_code == 409


def test_register_validation(client):
    assert register(client, password="short").status_code == 422
    assert register(client, email="not-an-email").status_code == 422
    assert register(client, username="ab").status_code == 422


def test_login_success(client):
    register(client)
    r = client.post("/api/auth/login", json={"email": "ALICE@example.com", "password": "correct-horse-1"})
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    register(client)
    assert client.post("/api/auth/login", json={"email": "alice@example.com", "password": "wrong-password"}).status_code == 401
    assert client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "whatever123"}).status_code == 401


def test_me_requires_valid_token(client, auth_headers):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"}).status_code == 401
    r = client.get("/api/auth/me", headers=auth_headers)
    assert r.status_code == 200 and r.json()["username"] == "alice"
