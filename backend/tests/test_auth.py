import pytest

from app import create_app, db
from app.models import DomesticUser, EnterpriseUser, SystemAdministrator


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
    })
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, role="domestic", email="user@example.com", **overrides):
    data = {
        "role": role,
        "name": "Test User",
        "email": email,
        "password": "strongpass",
        "contact_number": "1234567",
    }
    if role == "enterprise":
        data.update({
            "organization_name": "Test Org",
            "organization_type": "Corporate",
        })
    data.update(overrides)
    return client.post("/register", data=data)


def test_health_and_app_start(client):
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200


@pytest.mark.parametrize(
    ("role", "model", "prefix"),
    [
        ("administrator", SystemAdministrator, "ADM"),
        ("enterprise", EnterpriseUser, "ENT"),
        ("domestic", DomesticUser, "DOM"),
    ],
)
def test_registers_each_role_and_hashes_password(app, client, role, model, prefix):
    response = register(client, role=role, email=f"{role}@example.com")
    assert response.status_code == 302

    with app.app_context():
        account = model.query.filter_by(email=f"{role}@example.com").first()
        assert account is not None
        assert account.id.startswith(prefix + "-")
        assert account.password_hash.startswith("$2")
        assert "strongpass" not in account.password_hash


def test_duplicate_email_is_unique_within_role(app, client):
    assert register(client, role="domestic", email="same@example.com").status_code == 302
    response = register(client, role="domestic", email="same@example.com")
    assert response.status_code == 409

    assert register(client, role="enterprise", email="same@example.com").status_code == 302


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("email", "invalid", "valid email"),
        ("contact_number", "123", "seven digits"),
        ("password", "short", "eight characters"),
    ],
)
def test_registration_validation(client, field, value, error):
    response = register(client, role="domestic", **{field: value})
    assert response.status_code == 400
    assert error.encode() in response.data


def test_enterprise_requires_organization_fields(client):
    response = register(
        client,
        role="enterprise",
        organization_name="",
        organization_type="Unknown",
    )
    assert response.status_code == 400
    assert b"Organization name is required" in response.data
    assert b"valid organization type" in response.data


def test_login_and_role_authorization(app, client):
    assert register(client, role="enterprise", email="ent@example.com").status_code == 302
    response = client.post("/login", data={
        "role": "enterprise",
        "email": "ent@example.com",
        "password": "strongpass",
    })
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/enterprise")

    assert client.get("/enterprise").status_code == 200
    assert client.get("/domestic").status_code == 403


def test_wrong_password_and_inactive_account(app, client):
    assert register(client, role="domestic", email="locked@example.com").status_code == 302

    response = client.post("/login", data={
        "role": "domestic",
        "email": "locked@example.com",
        "password": "wrongpass",
    })
    assert response.status_code == 401

    with app.app_context():
        account = DomesticUser.query.filter_by(email="locked@example.com").first()
        account.active = False
        db.session.commit()

    response = client.post("/login", data={
        "role": "domestic",
        "email": "locked@example.com",
        "password": "strongpass",
    })
    assert response.status_code == 401


def test_logout(client):
    assert register(client, role="domestic", email="logout@example.com").status_code == 302
    client.post("/login", data={
        "role": "domestic",
        "email": "logout@example.com",
        "password": "strongpass",
    })
    response = client.post("/logout")
    assert response.status_code == 302
    assert client.get("/domestic").status_code == 302
