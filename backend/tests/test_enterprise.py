from datetime import datetime, timedelta, timezone

import pytest

from app import bcrypt, create_app, db
from app.models import (
    Alert,
    Appliance,
    Building,
    EnergyConsumption,
    EnergyLimit,
    EnterpriseUser,
    Report,
    Room,
)


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
        "ELECTRICITY_RATE_PER_KWH": 10,
    })
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def create_enterprise(app, enterprise_id="ENT-ONE", email="enterprise1@example.com", name="Enterprise One"):
    with app.app_context():
        account = EnterpriseUser(
            id=enterprise_id,
            name=name,
            email=email,
            password_hash=bcrypt.generate_password_hash("strongpass").decode("utf-8"),
            contact_number="1234567",
            organization_name=f"{name} Org",
            organization_type="Corporate",
            active=True,
        )
        db.session.add(account)
        db.session.commit()


def login_as(client, email="enterprise1@example.com"):
    return client.post("/login", data={
        "role": "enterprise",
        "email": email,
        "password": "strongpass",
    })


def create_hierarchy(app, enterprise_id="ENT-ONE"):
    with app.app_context():
        building = Building(
            id=f"BLD-{enterprise_id}",
            enterprise_user_id=enterprise_id,
            name="Main Building",
            building_type="Corporate",
            address="1 Test Street",
        )
        db.session.add(building)
        db.session.flush()
        room = Room(
            id=f"ROOM-{enterprise_id}",
            building_id=building.id,
            name="Server Room",
            floor_number=2,
            room_type="Server",
        )
        db.session.add(room)
        db.session.flush()
        appliance = Appliance(
            id=f"APP-{enterprise_id}",
            room_id=room.id,
            name="Server Rack",
            appliance_type="Server",
            rated_power=500,
            connection_status="online",
        )
        db.session.add(appliance)
        db.session.commit()
        return building.id, room.id, appliance.id


def test_enterprise_dashboard_requires_enterprise(app, client):
    assert client.get("/enterprise").status_code == 302
    create_enterprise(app)
    login_as(client)
    response = client.get("/enterprise")
    assert response.status_code == 200
    assert b"Enterprise Dashboard" in response.data
    assert b"Buildings" in response.data


def test_enterprise_cross_organization_access_is_forbidden(app, client):
    create_enterprise(app)
    create_enterprise(app, "ENT-TWO", "enterprise2@example.com", "Enterprise Two")
    _, _, _ = create_hierarchy(app, "ENT-TWO")

    login_as(client)
    response = client.get("/enterprise/buildings/BLD-ENT-TWO")
    assert response.status_code == 403


def test_enterprise_building_room_and_appliance_crud(app, client):
    create_enterprise(app)
    login_as(client)

    response = client.post("/enterprise/buildings", data={
        "name": "New Building",
        "building_type": "Corporate",
        "address": "10 Energy Road",
    })
    assert response.status_code == 302

    with app.app_context():
        building = Building.query.filter_by(name="New Building").first()
        assert building is not None
        building_id = building.id

    response = client.post(f"/enterprise/buildings/{building_id}/rooms", data={
        "name": "Lab",
        "floor_number": "3",
        "room_type": "Laboratory",
    })
    assert response.status_code == 302

    with app.app_context():
        room = Room.query.filter_by(building_id=building_id, name="Lab").first()
        assert room is not None
        room_id = room.id

    response = client.post(f"/enterprise/rooms/{room_id}/appliances", data={
        "name": "Microscope",
        "appliance_type": "Laboratory",
        "rated_power": "300",
        "connection_status": "online",
    })
    assert response.status_code == 302

    with app.app_context():
        appliance = Appliance.query.filter_by(room_id=room_id, name="Microscope").first()
        assert appliance is not None


def test_enterprise_update_and_delete_hierarchy(app, client):
    create_enterprise(app)
    building_id, room_id, appliance_id = create_hierarchy(app)
    login_as(client)

    response = client.post(
        f"/enterprise/buildings/{building_id}/update",
        data={"name": "Updated", "building_type": "Office", "address": "New Address"},
    )
    assert response.status_code == 302
    response = client.post(f"/enterprise/buildings/{building_id}/delete")
    assert response.status_code == 409

    response = client.post(
        f"/enterprise/rooms/{room_id}/update",
        data={"name": "Updated Room", "floor_number": "4", "room_type": "Office"},
    )
    assert response.status_code == 302
    response = client.post(
        f"/enterprise/appliances/{appliance_id}/update",
        data={"name": "Updated Appliance", "appliance_type": "Office", "rated_power": "600"},
    )
    assert response.status_code == 302
    response = client.post(f"/enterprise/rooms/{room_id}/delete")
    assert response.status_code == 409

    response = client.post(f"/enterprise/appliances/{appliance_id}/delete")
    assert response.status_code == 302
    response = client.post(f"/enterprise/rooms/{room_id}/delete")
    assert response.status_code == 302
    response = client.post(f"/enterprise/buildings/{building_id}/delete")
    assert response.status_code == 302


def test_monitoring_reads_simulated_source_and_totals(app, client):
    create_enterprise(app)
    building_id, room_id, appliance_id = create_hierarchy(app)
    with app.app_context():
        db.session.add(EnergyConsumption(
            appliance_id=appliance_id,
            voltage=230,
            current=2,
            power=460,
            energy=1.5,
            source="simulated",
            recorded_at=datetime.now(timezone.utc),
        ))
        db.session.commit()

    login_as(client)
    response = client.get(f"/enterprise/appliances/{appliance_id}")
    assert response.status_code == 200
    assert b"230" in response.data
    assert b"2.0" in response.data or b"2" in response.data
    assert b"460" in response.data
    assert b"1.5" in response.data
    assert b"simulated" in response.data


def test_room_limit_and_alert_generation(app, client):
    create_enterprise(app)
    _, room_id, appliance_id = create_hierarchy(app)
    with app.app_context():
        db.session.add(EnergyLimit(
            room_id=room_id,
            period="daily",
            limit_kwh=1,
            active=True,
        ))
        db.session.add(EnergyConsumption(
            appliance_id=appliance_id,
            voltage=230,
            current=5,
            power=1150,
            energy=1.25,
            source="simulated",
            recorded_at=datetime.now(timezone.utc),
        ))
        db.session.commit()

    login_as(client)
    response = client.post(f"/enterprise/rooms/{room_id}/limits", data={
        "period": "daily",
        "limit_kwh": "1",
    })
    assert response.status_code == 302

    response = client.post(f"/enterprise/rooms/{room_id}/check-limit")
    assert response.status_code == 302

    with app.app_context():
        alert = Alert.query.filter_by(recipient_account_id="ENT-ONE", resolved=False).first()
        assert alert is not None
        assert "limit" in alert.title.lower()
        high_consumption_alert = Alert.query.filter_by(
            recipient_account_id="ENT-ONE",
            title="High consumption",
            resolved=False,
        ).first()
        assert high_consumption_alert is not None


def test_appliance_offline_alert_is_resolved_when_online(app, client):
    create_enterprise(app)
    _, _, appliance_id = create_hierarchy(app)
    login_as(client)

    assert client.post(
        f"/enterprise/appliances/{appliance_id}/status",
        data={"connection_status": "offline"},
    ).status_code == 302
    assert client.post(
        f"/enterprise/appliances/{appliance_id}/status",
        data={"connection_status": "online"},
    ).status_code == 302

    with app.app_context():
        alert = Alert.query.filter_by(
            recipient_account_id="ENT-ONE",
            title="Appliance offline",
            message=appliance_id,
        ).first()
        assert alert is not None
        assert alert.resolved is True


def test_enterprise_reports_belong_to_enterprise(app, client):
    create_enterprise(app)
    _, _, appliance_id = create_hierarchy(app)
    with app.app_context():
        db.session.add(EnergyConsumption(
            appliance_id=appliance_id,
            voltage=230,
            current=2,
            power=460,
            energy=1.5,
            source="simulated",
            recorded_at=datetime.now(timezone.utc),
        ))
        db.session.add(Report(
            owner_role="enterprise",
            owner_account_id="ENT-ONE",
            report_type="daily",
            title="Daily Enterprise Report",
        ))
        db.session.add(Report(
            owner_role="enterprise",
            owner_account_id="ENT-TWO",
            report_type="daily",
            title="Another Organization Report",
        ))
        db.session.commit()

    login_as(client)
    response = client.get("/enterprise/reports")
    assert response.status_code == 200
    assert b"Daily Enterprise Report" in response.data
    assert b"Another Organization Report" not in response.data

    response = client.post("/enterprise/reports", data={"report_type": "daily"})
    assert response.status_code == 302
    with app.app_context():
        generated = Report.query.filter_by(
            owner_account_id="ENT-ONE",
            title="Daily Enterprise Report",
        ).order_by(Report.id.desc()).first()
        assert generated is not None
        assert "1.5 kWh" in generated.summary


@pytest.mark.parametrize("report_type", ["weekly", "monthly", "asset"])
def test_enterprise_generates_period_and_asset_reports(app, client, report_type):
    create_enterprise(app)
    _, _, appliance_id = create_hierarchy(app)
    with app.app_context():
        db.session.add(EnergyConsumption(
            appliance_id=appliance_id,
            voltage=230,
            current=2,
            power=460,
            energy=2.25,
            source="simulated",
            recorded_at=datetime.now(timezone.utc),
        ))
        db.session.commit()

    login_as(client)
    data = {"report_type": report_type}
    if report_type == "asset":
        data["appliance_id"] = appliance_id
    response = client.post("/enterprise/reports", data=data)
    assert response.status_code == 302

    with app.app_context():
        report = Report.query.filter_by(
            owner_account_id="ENT-ONE",
            report_type=report_type,
        ).first()
        assert report is not None
        assert "2.25 kWh" in report.summary


def test_enterprise_cannot_mutate_another_organizations_building(app, client):
    create_enterprise(app)
    create_enterprise(app, "ENT-TWO", "enterprise2@example.com", "Enterprise Two")
    building_id, _, _ = create_hierarchy(app, "ENT-TWO")
    login_as(client)

    response = client.post(
        f"/enterprise/buildings/{building_id}/update",
        data={
            "name": "Stolen Building",
            "building_type": "Corporate",
            "address": "Tampered",
        },
    )
    assert response.status_code == 403
