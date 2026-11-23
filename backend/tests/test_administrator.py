import pytest

from app import create_app, db
from app.models import (
    Building,
    DomesticUser,
    EnterpriseUser,
    SystemAdministrator,
)


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


def create_administrator(app, name="Admin", email="admin@example.com"):
    from app import bcrypt

    with app.app_context():
        account = SystemAdministrator(
            id="ADM-ADMIN001",
            name=name,
            email=email,
            password_hash=bcrypt.generate_password_hash("strongpass").decode("utf-8"),
            contact_number="1234567",
            active=True,
        )
        db.session.add(account)
        db.session.commit()
        return account.id


def login_as(client, role, email, password="strongpass"):
    return client.post("/login", data={
        "role": role,
        "email": email,
        "password": password,
    })


def test_administrator_dashboard_requires_administrator(app, client):
    assert client.get("/administrator").status_code == 302

    create_administrator(app)
    login_as(client, "administrator", "admin@example.com")

    response = client.get("/administrator")
    assert response.status_code == 200
    assert b"Administrator Dashboard" in response.data
    assert b"Registered Users" in response.data
    assert b"Enterprise Users" in response.data
    assert b"Domestic Users" in response.data


def test_administrator_cannot_be_enterprise_or_domestic(app, client):
    from app import bcrypt

    with app.app_context():
        enterprise = EnterpriseUser(
            id="ENT-USER001",
            name="Enterprise",
            email="enterprise@example.com",
            password_hash=bcrypt.generate_password_hash("strongpass").decode("utf-8"),
            contact_number="1234567",
            organization_name="Example Org",
            organization_type="Corporate",
            active=True,
        )
        db.session.add(enterprise)
        db.session.commit()

    login_as(client, "enterprise", "enterprise@example.com")
    assert client.get("/administrator").status_code == 403


def test_administrator_account_search_and_status(app, client):
    create_administrator(app)
    with app.app_context():
        db.session.add(DomesticUser(
            id="DOM-USER001",
            name="Alex Domestic",
            email="alex@example.com",
            password_hash="$2b$12$testhash",
            contact_number="1234567",
            active=True,
        ))
        db.session.commit()

    login_as(client, "administrator", "admin@example.com")

    response = client.get("/administrator/users?role=domestic&search=Alex")
    assert response.status_code == 200
    assert b"Alex Domestic" in response.data
    assert b"alex@example.com" in response.data
    assert b"$2b$12$testhash" not in response.data

    response = client.post("/administrator/users/domestic/DOM-USER001/status", data={"active": "false"})
    assert response.status_code == 302

    with app.app_context():
        account = db.session.get(DomesticUser, "DOM-USER001")
        assert account.active is False


def test_administrator_account_removal(app, client):
    create_administrator(app)
    with app.app_context():
        db.session.add(DomesticUser(
            id="DOM-REMOVE001",
            name="Remove Me",
            email="remove@example.com",
            password_hash="$2b$12$testhash",
            contact_number="1234567",
            active=True,
        ))
        db.session.commit()

    login_as(client, "administrator", "admin@example.com")
    response = client.post("/administrator/users/domestic/DOM-REMOVE001/remove")
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(DomesticUser, "DOM-REMOVE001") is None


def test_administrator_dashboard_counts_database_records(app, client):
    create_administrator(app)
    with app.app_context():
        db.session.add_all([
            DomesticUser(
                id="DOM-COUNT001",
                name="Domestic",
                email="domestic-count@example.com",
                password_hash="$2b$12$testhash",
                contact_number="1234567",
                active=True,
            ),
            EnterpriseUser(
                id="ENT-COUNT001",
                name="Enterprise",
                email="enterprise-count@example.com",
                password_hash="$2b$12$testhash",
                contact_number="1234567",
                organization_name="Count Org",
                organization_type="Corporate",
                active=True,
            ),
        ])
        db.session.flush()
        db.session.add(Building(
            id="BLD-COUNT001",
            enterprise_user_id="ENT-COUNT001",
            name="Main Building",
            building_type="Corporate",
            address="Test Address",
        ))
        db.session.commit()

    login_as(client, "administrator", "admin@example.com")
    response = client.get("/administrator")
    assert response.status_code == 200
    assert b"2" in response.data
    assert b"Buildings" in response.data


def test_administrator_account_detail_hides_password(app, client):
    create_administrator(app)
    with app.app_context():
        db.session.add(DomesticUser(
            id="DOM-DETAIL001",
            name="Detail User",
            email="detail@example.com",
            password_hash="$2b$12$testhash",
            contact_number="1234567",
            active=True,
        ))
        db.session.commit()

    login_as(client, "administrator", "admin@example.com")
    response = client.get("/administrator/users/domestic/DOM-DETAIL001")
    assert response.status_code == 200
    assert b"Detail User" in response.data
    assert b"Assigned Rooms" in response.data
    assert b"$2b$12$testhash" not in response.data
