from datetime import datetime, timezone

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app import db


class SystemAdministrator(db.Model):
    __tablename__ = "SYSTEM_ADMINISTRATOR"

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(32), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("email", name="uq_administrator_email"),)


class EnterpriseUser(db.Model):
    __tablename__ = "ENTERPRISE_USER"

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(32), nullable=False)
    organization_name = db.Column(db.String(180), nullable=False)
    organization_type = db.Column(db.String(32), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("email", name="uq_enterprise_email"),)


class DomesticUser(db.Model):
    __tablename__ = "DOMESTIC_USER"

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(32), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (UniqueConstraint("email", name="uq_domestic_email"),)


class Building(db.Model):
    __tablename__ = "BUILDING"

    id = db.Column(db.String(32), primary_key=True)
    enterprise_user_id = db.Column(db.String(32), ForeignKey("ENTERPRISE_USER.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    building_type = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    rooms = relationship("Room", back_populates="building")


class Room(db.Model):
    __tablename__ = "ROOM"

    id = db.Column(db.String(32), primary_key=True)
    building_id = db.Column(db.String(32), ForeignKey("BUILDING.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    floor_number = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(64), nullable=False)
    building = relationship("Building", back_populates="rooms")
    appliances = relationship("Appliance", back_populates="room")

    __table_args__ = (
        UniqueConstraint("building_id", "floor_number", "name", name="uq_room_location"),
    )


class Appliance(db.Model):
    __tablename__ = "APPLIANCE"

    id = db.Column(db.String(32), primary_key=True)
    room_id = db.Column(db.String(32), ForeignKey("ROOM.id"), nullable=False, index=True)
    name = db.Column(db.String(180), nullable=False)
    appliance_type = db.Column(db.String(64), nullable=False)
    rated_power = db.Column(db.Float, nullable=False)
    connection_status = db.Column(db.String(32), nullable=False, default="offline")
    room = relationship("Room", back_populates="appliances")
    readings = relationship("EnergyConsumption", back_populates="appliance")


class EnergyConsumption(db.Model):
    __tablename__ = "ENERGY_CONSUMPTION"

    id = db.Column(db.Integer, primary_key=True)
    appliance_id = db.Column(db.String(32), ForeignKey("APPLIANCE.id"), nullable=False, index=True)
    voltage = db.Column(db.Float, nullable=False)
    current = db.Column(db.Float, nullable=False)
    power = db.Column(db.Float, nullable=False)
    energy = db.Column(db.Float, nullable=False)
    source = db.Column(db.String(16), nullable=False, default="simulated")
    recorded_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)
    appliance = relationship("Appliance", back_populates="readings")


class EnergyLimit(db.Model):
    __tablename__ = "ENERGY_LIMIT"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(32), ForeignKey("ROOM.id"), nullable=False, index=True)
    period = db.Column(db.String(16), nullable=False)
    limit_kwh = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("room_id", "period", name="uq_energy_limit_room_period"),
    )


class Alert(db.Model):
    __tablename__ = "ALERT"

    id = db.Column(db.Integer, primary_key=True)
    recipient_role = db.Column(db.String(32), nullable=False, index=True)
    recipient_account_id = db.Column(db.String(32), nullable=True, index=True)
    title = db.Column(db.String(180), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    resolved = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)


class Report(db.Model):
    __tablename__ = "REPORT"

    id = db.Column(db.Integer, primary_key=True)
    owner_role = db.Column(db.String(32), nullable=False, index=True)
    owner_account_id = db.Column(db.String(32), nullable=True, index=True)
    report_type = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    generated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)


class AssignedTo(db.Model):
    __tablename__ = "ASSIGNED_TO"

    domestic_user_id = db.Column(db.String(32), ForeignKey("DOMESTIC_USER.id"), primary_key=True)
    room_id = db.Column(db.String(32), ForeignKey("ROOM.id"), primary_key=True)

