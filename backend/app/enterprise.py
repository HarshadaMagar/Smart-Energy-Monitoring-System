from datetime import datetime, time, timedelta, timezone
import uuid

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from sqlalchemy import func

from app import db
from app.auth import role_required
from app.models import (
    Alert,
    AssignedTo,
    Appliance,
    Building,
    EnergyConsumption,
    EnergyLimit,
    Report,
    Room,
)

enterprise_bp = Blueprint("enterprise", __name__, url_prefix="/enterprise")


def _new_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


def _owned_building(building_id):
    building = Building.query.filter_by(
        id=building_id,
        enterprise_user_id=session["account_id"],
    ).first()
    if building is None:
        abort(403)
    return building


def _owned_room(room_id):
    room = (
        Room.query.join(Building, Room.building_id == Building.id)
        .filter(
            Room.id == room_id,
            Building.enterprise_user_id == session["account_id"],
        )
        .first()
    )
    if room is None:
        abort(403)
    return room


def _owned_appliance(appliance_id):
    appliance = (
        Appliance.query.join(Room, Appliance.room_id == Room.id)
        .join(Building, Room.building_id == Building.id)
        .filter(
            Appliance.id == appliance_id,
            Building.enterprise_user_id == session["account_id"],
        )
        .first()
    )
    if appliance is None:
        abort(403)
    return appliance


def _period_start(period):
    now = datetime.now(timezone.utc)
    if period == "daily":
        return datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    first_of_month = now.date().replace(day=1)
    return datetime.combine(first_of_month, time.min, tzinfo=timezone.utc)


def _week_start():
    today = datetime.now(timezone.utc).date()
    return datetime.combine(today - timedelta(days=6), time.min, tzinfo=timezone.utc)


def _room_energy(room_id, period="daily"):
    start = _period_start(period)
    total = (
        db.session.query(func.coalesce(func.sum(EnergyConsumption.energy), 0.0))
        .join(Appliance, EnergyConsumption.appliance_id == Appliance.id)
        .filter(Appliance.room_id == room_id, EnergyConsumption.recorded_at >= start)
        .scalar()
    )
    return float(total or 0)


def _room_limits(buildings):
    building_ids = [building.id for building in buildings]
    room_ids = [
        room.id for room in Room.query.filter(Room.building_id.in_(building_ids)).all()
    ] if building_ids else []
    if not room_ids:
        return []
    limits = EnergyLimit.query.filter(
        EnergyLimit.room_id.in_(room_ids),
        EnergyLimit.active.is_(True),
    ).all()
    return [
        {
            "room_id": limit.room_id,
            "period": limit.period,
            "limit_kwh": limit.limit_kwh,
            "consumed": _room_energy(limit.room_id, limit.period),
        }
        for limit in limits
    ]


@enterprise_bp.route("")
@role_required("enterprise")
def dashboard():
    account_id = session["account_id"]
    buildings = Building.query.filter_by(enterprise_user_id=account_id).all()
    building_ids = [building.id for building in buildings]
    rooms = Room.query.filter(Room.building_id.in_(building_ids)).all() if building_ids else []
    room_ids = [room.id for room in rooms]
    appliances = Appliance.query.filter(Appliance.room_id.in_(room_ids)).all() if room_ids else []
    appliance_ids = [appliance.id for appliance in appliances]

    today = _period_start("daily")
    readings = []
    if appliance_ids:
        readings = EnergyConsumption.query.filter(
            EnergyConsumption.appliance_id.in_(appliance_ids),
            EnergyConsumption.recorded_at >= today,
        ).order_by(EnergyConsumption.recorded_at.desc()).all()

    latest_by_appliance = {}
    for reading in readings:
        latest_by_appliance.setdefault(reading.appliance_id, reading)
    energy_today = sum(reading.energy for reading in readings)
    current_power = sum(reading.power for reading in latest_by_appliance.values())
    rate = current_app.config["ELECTRICITY_RATE_PER_KWH"]
    active_alerts = Alert.query.filter_by(
        recipient_role="enterprise",
        recipient_account_id=account_id,
        resolved=False,
    ).count()
    room_energy = [
        {"label": room.name, "value": _room_energy(room.id)}
        for room in rooms
    ]
    building_energy = [
        {
            "label": building.name,
            "value": sum(_room_energy(room.id) for room in building.rooms),
        }
        for building in buildings
    ]
    now = datetime.now(timezone.utc)
    week_readings = [
        {
            "label": (now - timedelta(days=offset)).strftime("%a"),
            "value": float(
                db.session.query(func.coalesce(func.sum(EnergyConsumption.energy), 0.0))
                .filter(
                    EnergyConsumption.appliance_id.in_(appliance_ids),
                    EnergyConsumption.recorded_at >= datetime.combine(
                        (now - timedelta(days=offset)).date(),
                        time.min,
                        tzinfo=timezone.utc,
                    ),
                    EnergyConsumption.recorded_at < datetime.combine(
                        (now - timedelta(days=offset - 1)).date(),
                        time.min,
                        tzinfo=timezone.utc,
                    ),
                )
                .scalar()
                or 0
            ),
        }
        for offset in range(6, -1, -1)
    ] if appliance_ids else []

    return render_template(
        "enterprise/dashboard.html",
        buildings=buildings,
        building_count=len(buildings),
        floor_count=len({(room.building_id, room.floor_number) for room in rooms}),
        room_count=len(rooms),
        appliance_count=len(appliances),
        online_count=sum(appliance.connection_status == "online" for appliance in appliances),
        energy_today=energy_today,
        current_power=current_power,
        estimated_bill=energy_today * rate,
        active_alerts=active_alerts,
        limits=_room_limits(buildings),
        room_energy=room_energy,
        building_energy=building_energy,
        week_readings=week_readings,
    )


@enterprise_bp.route("/buildings", methods=["GET", "POST"])
@role_required("enterprise")
def buildings():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        building_type = request.form.get("building_type", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not building_type or not address:
            flash("Building name, type, and address are required.", "error")
            return redirect(url_for("enterprise.buildings"))
        building = Building(
            id=_new_id("BLD"),
            enterprise_user_id=session["account_id"],
            name=name,
            building_type=building_type,
            address=address,
        )
        db.session.add(building)
        db.session.commit()
        flash("Building created.", "success")
        return redirect(url_for("enterprise.building_detail", building_id=building.id))

    owned_buildings = Building.query.filter_by(
        enterprise_user_id=session["account_id"],
    ).order_by(Building.name).all()
    return render_template("enterprise/buildings.html", buildings=owned_buildings)


@enterprise_bp.route("/buildings/<building_id>")
@role_required("enterprise")
def building_detail(building_id):
    building = _owned_building(building_id)
    return render_template("enterprise/building_detail.html", building=building)


@enterprise_bp.route("/buildings/<building_id>/update", methods=["POST"])
@role_required("enterprise")
def update_building(building_id):
    building = _owned_building(building_id)
    name = request.form.get("name", "").strip()
    building_type = request.form.get("building_type", "").strip()
    address = request.form.get("address", "").strip()
    if not name or not building_type or not address:
        flash("Building name, type, and address are required.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=building_id))
    building.name = name
    building.building_type = building_type
    building.address = address
    db.session.commit()
    flash("Building updated.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=building_id))


@enterprise_bp.route("/buildings/<building_id>/delete", methods=["POST"])
@role_required("enterprise")
def delete_building(building_id):
    building = _owned_building(building_id)
    if Room.query.filter_by(building_id=building.id).first():
        flash("Remove the building's rooms and appliances before deleting it.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=building_id)), 409
    db.session.delete(building)
    db.session.commit()
    flash("Building deleted.", "success")
    return redirect(url_for("enterprise.buildings"))


@enterprise_bp.route("/rooms/<room_id>/update", methods=["POST"])
@role_required("enterprise")
def update_room(room_id):
    room = _owned_room(room_id)
    name = request.form.get("name", "").strip()
    room_type = request.form.get("room_type", "").strip()
    try:
        floor_number = int(request.form.get("floor_number", ""))
    except ValueError:
        floor_number = 0
    if not name or not room_type or floor_number < 1:
        flash("Provide a room name, type, and positive floor number.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=room.building_id))
    room.name = name
    room.room_type = room_type
    room.floor_number = floor_number
    db.session.commit()
    flash("Room updated.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=room.building_id))


@enterprise_bp.route("/rooms/<room_id>/delete", methods=["POST"])
@role_required("enterprise")
def delete_room(room_id):
    room = _owned_room(room_id)
    if (
        Appliance.query.filter_by(room_id=room.id).first()
        or EnergyLimit.query.filter_by(room_id=room.id).first()
        or AssignedTo.query.filter_by(room_id=room.id).first()
    ):
        flash("Remove the room's appliances, energy limits, and user assignments before deleting it.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=room.building_id)), 409
    building_id = room.building_id
    db.session.delete(room)
    db.session.commit()
    flash("Room deleted.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=building_id))


@enterprise_bp.route("/buildings/<building_id>/rooms", methods=["POST"])
@role_required("enterprise")
def create_room(building_id):
    building = _owned_building(building_id)
    name = request.form.get("name", "").strip()
    room_type = request.form.get("room_type", "").strip()
    try:
        floor_number = int(request.form.get("floor_number", ""))
    except ValueError:
        floor_number = 0
    if not name or not room_type or floor_number < 1:
        flash("Provide a room name, type, and positive floor number.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=building_id))

    room = Room(
        id=_new_id("ROOM"),
        building_id=building.id,
        name=name,
        floor_number=floor_number,
        room_type=room_type,
    )
    db.session.add(room)
    db.session.commit()
    flash("Room created.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=building_id))


@enterprise_bp.route("/rooms/<room_id>/appliances", methods=["POST"])
@role_required("enterprise")
def create_appliance(room_id):
    room = _owned_room(room_id)
    name = request.form.get("name", "").strip()
    appliance_type = request.form.get("appliance_type", "").strip()
    connection_status = request.form.get("connection_status", "offline").strip().lower()
    try:
        rated_power = float(request.form.get("rated_power", ""))
    except ValueError:
        rated_power = 0
    if not name or not appliance_type or rated_power <= 0 or connection_status not in {"online", "offline"}:
        flash("Provide valid appliance details and a positive rated power.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=room.building_id))

    appliance = Appliance(
        id=_new_id("APP"),
        room_id=room.id,
        name=name,
        appliance_type=appliance_type,
        rated_power=rated_power,
        connection_status=connection_status,
    )
    db.session.add(appliance)
    db.session.commit()
    flash("Appliance created.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=room.building_id))


@enterprise_bp.route("/appliances/<appliance_id>/update", methods=["POST"])
@role_required("enterprise")
def update_appliance(appliance_id):
    appliance = _owned_appliance(appliance_id)
    name = request.form.get("name", "").strip()
    appliance_type = request.form.get("appliance_type", "").strip()
    try:
        rated_power = float(request.form.get("rated_power", ""))
    except ValueError:
        rated_power = 0
    if not name or not appliance_type or rated_power <= 0:
        flash("Provide valid appliance details and a positive rated power.", "error")
        return redirect(url_for("enterprise.appliance_detail", appliance_id=appliance_id))
    appliance.name = name
    appliance.appliance_type = appliance_type
    appliance.rated_power = rated_power
    db.session.commit()
    flash("Appliance updated.", "success")
    return redirect(url_for("enterprise.appliance_detail", appliance_id=appliance_id))


@enterprise_bp.route("/appliances/<appliance_id>/delete", methods=["POST"])
@role_required("enterprise")
def delete_appliance(appliance_id):
    appliance = _owned_appliance(appliance_id)
    if EnergyConsumption.query.filter_by(appliance_id=appliance.id).first():
        flash("This appliance has readings and cannot be deleted.", "error")
        return redirect(url_for("enterprise.appliance_detail", appliance_id=appliance_id)), 409
    room = db.session.get(Room, appliance.room_id)
    building_id = room.building_id
    db.session.delete(appliance)
    db.session.commit()
    flash("Appliance deleted.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=building_id))


@enterprise_bp.route("/appliances/<appliance_id>")
@role_required("enterprise")
def appliance_detail(appliance_id):
    appliance = _owned_appliance(appliance_id)
    readings = EnergyConsumption.query.filter_by(
        appliance_id=appliance.id,
    ).order_by(EnergyConsumption.recorded_at.desc()).limit(50).all()
    return render_template(
        "enterprise/appliance_detail.html",
        appliance=appliance,
        readings=readings,
    )


@enterprise_bp.route("/appliances/<appliance_id>/status", methods=["POST"])
@role_required("enterprise")
def update_appliance_status(appliance_id):
    appliance = _owned_appliance(appliance_id)
    status = request.form.get("connection_status", "").strip().lower()
    if status not in {"online", "offline"}:
        flash("Choose online or offline status.", "error")
        return redirect(url_for("enterprise.appliance_detail", appliance_id=appliance_id))
    appliance.connection_status = status
    if status == "offline":
        existing = Alert.query.filter_by(
            recipient_role="enterprise",
            recipient_account_id=session["account_id"],
            resolved=False,
            title="Appliance offline",
            message=appliance.id,
        ).first()
        if existing is None:
            db.session.add(Alert(
                recipient_role="enterprise",
                recipient_account_id=session["account_id"],
                title="Appliance offline",
                message=appliance.id,
            ))
    else:
        Alert.query.filter_by(
            recipient_role="enterprise",
            recipient_account_id=session["account_id"],
            resolved=False,
            title="Appliance offline",
            message=appliance.id,
        ).update({"resolved": True})
    db.session.commit()
    flash("Appliance status updated.", "success")
    return redirect(url_for("enterprise.appliance_detail", appliance_id=appliance_id))


@enterprise_bp.route("/rooms/<room_id>/limits", methods=["POST"])
@role_required("enterprise")
def save_room_limit(room_id):
    room = _owned_room(room_id)
    period = request.form.get("period", "").strip().lower()
    try:
        limit_kwh = float(request.form.get("limit_kwh", ""))
    except ValueError:
        limit_kwh = 0
    if period not in {"daily", "monthly"} or limit_kwh <= 0:
        flash("Choose a daily or monthly period and a positive energy limit.", "error")
        return redirect(url_for("enterprise.building_detail", building_id=room.building_id))

    limit = EnergyLimit.query.filter_by(room_id=room.id, period=period).first()
    if limit is None:
        limit = EnergyLimit(room_id=room.id, period=period, limit_kwh=limit_kwh, active=True)
        db.session.add(limit)
    else:
        limit.limit_kwh = limit_kwh
        limit.active = True
    db.session.commit()
    flash("Energy limit saved.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=room.building_id))


@enterprise_bp.route("/rooms/<room_id>/check-limit", methods=["POST"])
@role_required("enterprise")
def check_room_limit(room_id):
    room = _owned_room(room_id)
    limits = EnergyLimit.query.filter_by(room_id=room.id, active=True).all()
    for limit in limits:
        consumed = _room_energy(room.id, limit.period)
        if consumed > limit.limit_kwh:
            message = f"{room.id}:{limit.period}"
            alert = Alert.query.filter_by(
                recipient_role="enterprise",
                recipient_account_id=session["account_id"],
                resolved=False,
                title="Energy limit exceeded",
                message=message,
            ).first()
            if alert is None:
                db.session.add(Alert(
                    recipient_role="enterprise",
                    recipient_account_id=session["account_id"],
                    title="Energy limit exceeded",
                    message=message,
                ))
            high_consumption = Alert.query.filter_by(
                recipient_role="enterprise",
                recipient_account_id=session["account_id"],
                resolved=False,
                title="High consumption",
                message=message,
            ).first()
            if high_consumption is None:
                db.session.add(Alert(
                    recipient_role="enterprise",
                    recipient_account_id=session["account_id"],
                    title="High consumption",
                    message=message,
                ))
        else:
            Alert.query.filter_by(
                recipient_role="enterprise",
                recipient_account_id=session["account_id"],
                resolved=False,
                title="Energy limit exceeded",
                message=f"{room.id}:{limit.period}",
            ).update({"resolved": True})
    db.session.commit()
    flash("Room limits checked against recorded readings.", "success")
    return redirect(url_for("enterprise.building_detail", building_id=room.building_id))


@enterprise_bp.route("/alerts")
@role_required("enterprise")
def alerts():
    alerts = Alert.query.filter_by(
        recipient_role="enterprise",
        recipient_account_id=session["account_id"],
    ).order_by(Alert.created_at.desc()).all()
    return render_template("enterprise/alerts.html", alerts=alerts)


@enterprise_bp.route("/reports", methods=["GET", "POST"])
@role_required("enterprise")
def reports():
    account_id = session["account_id"]
    owned_appliances = (
        Appliance.query.join(Room, Appliance.room_id == Room.id)
        .join(Building, Room.building_id == Building.id)
        .filter(Building.enterprise_user_id == account_id)
        .order_by(Appliance.name)
        .all()
    )
    if request.method == "POST":
        report_type = request.form.get("report_type", "").strip().lower()
        if report_type not in {"daily", "weekly", "monthly", "asset"}:
            flash("Choose a daily, weekly, monthly, or asset-wise report.", "error")
            return redirect(url_for("enterprise.reports"))
        start = None
        appliance_id = None
        if report_type == "daily":
            start = _period_start("daily")
        elif report_type == "weekly":
            start = _week_start()
        elif report_type == "monthly":
            start = _period_start("monthly")
        else:
            appliance_id = request.form.get("appliance_id", "")
            _owned_appliance(appliance_id)

        query = (
            db.session.query(func.coalesce(func.sum(EnergyConsumption.energy), 0.0))
            .join(Appliance, EnergyConsumption.appliance_id == Appliance.id)
            .join(Room, Appliance.room_id == Room.id)
            .join(Building, Room.building_id == Building.id)
            .filter(Building.enterprise_user_id == account_id)
        )
        if start is not None:
            query = query.filter(EnergyConsumption.recorded_at >= start)
        if appliance_id is not None:
            query = query.filter(EnergyConsumption.appliance_id == appliance_id)
        energy_total = float(query.scalar() or 0)
        rate = current_app.config["ELECTRICITY_RATE_PER_KWH"]
        report_title = (
            f"{report_type.title()} Enterprise Report"
            if appliance_id is None
            else f"Asset Report: {next(item.name for item in owned_appliances if item.id == appliance_id)}"
        )
        report = Report(
            owner_role="enterprise",
            owner_account_id=account_id,
            report_type=report_type,
            title=report_title,
            summary=f"{energy_total:g} kWh; estimated bill {energy_total * rate:.2f}",
        )
        db.session.add(report)
        db.session.commit()
        flash("Report generated.", "success")
        return redirect(url_for("enterprise.reports"))

    owned_reports = Report.query.filter_by(
        owner_role="enterprise",
        owner_account_id=account_id,
    ).order_by(Report.generated_at.desc()).all()
    return render_template(
        "enterprise/reports.html",
        reports=owned_reports,
        appliances=owned_appliances,
    )


@enterprise_bp.route("/monitoring")
@role_required("enterprise")
def monitoring():
    buildings = Building.query.filter_by(enterprise_user_id=session["account_id"]).all()
    return render_template("enterprise/monitoring.html", buildings=buildings)
