from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_

from app import db
from app.auth import role_required
from app.models import (
    Alert,
    Appliance,
    Building,
    DomesticUser,
    EnterpriseUser,
    Report,
    SystemAdministrator,
)

admin_bp = Blueprint("admin", __name__, url_prefix="/administrator")

ROLE_MODELS = {
    "domestic": DomesticUser,
    "enterprise": EnterpriseUser,
}


@admin_bp.route("")
@role_required("administrator")
def administrator_dashboard():
    domestic_count = DomesticUser.query.count()
    enterprise_count = EnterpriseUser.query.count()
    building_count = Building.query.count()
    appliance_count = Appliance.query.count()
    alert_count = Alert.query.filter_by(resolved=False).count()

    return render_template(
        "administrator/dashboard.html",
        registered_users=SystemAdministrator.query.count() + domestic_count + enterprise_count,
        domestic_users=domestic_count,
        enterprise_users=enterprise_count,
        buildings=building_count,
        appliances=appliance_count,
        active_alerts=alert_count,
        total_consumption=0,
        estimated_bills=0,
    )


@admin_bp.route("/users")
@role_required("administrator")
def users():
    role = request.args.get("role", "domestic")
    search = request.args.get("search", "").strip()
    model = ROLE_MODELS.get(role)
    if model is None:
        flash("Select a valid account type.", "error")
        return redirect(url_for("admin.users"))

    query = model.query
    if search:
        expression = f"%{search}%"
        query = query.filter(or_(model.name.ilike(expression), model.email.ilike(expression)))
    accounts = query.order_by(model.created_at.desc()).all()

    return render_template(
        "administrator/users.html",
        role=role,
        search=search,
        accounts=accounts,
    )


@admin_bp.route("/users/<role>/<account_id>/status", methods=["POST"])
@role_required("administrator")
def update_user_status(role, account_id):
    model = ROLE_MODELS.get(role)
    if model is None:
        flash("Select a valid account type.", "error")
        return redirect(url_for("admin.users"))

    account = db.session.get(model, account_id)
    if account is None:
        flash("Account not found.", "error")
        return redirect(url_for("admin.users", role=role))

    account.active = request.form.get("active", "true").lower() == "true"
    db.session.commit()
    flash("Account status updated.", "success")
    return redirect(url_for("admin.users", role=role))


@admin_bp.route("/users/<role>/<account_id>")
@role_required("administrator")
def account_detail(role, account_id):
    model = ROLE_MODELS.get(role)
    if model is None:
        flash("Select a valid account type.", "error")
        return redirect(url_for("admin.users"))

    account = db.session.get(model, account_id)
    if account is None:
        flash("Account not found.", "error")
        return redirect(url_for("admin.users", role=role))

    buildings = []
    if role == "enterprise":
        buildings = Building.query.filter_by(enterprise_user_id=account_id).all()

    return render_template(
        "administrator/account_detail.html",
        role=role,
        account=account,
        buildings=buildings,
    )


@admin_bp.route("/users/<role>/<account_id>/remove", methods=["POST"])
@role_required("administrator")
def remove_user(role, account_id):
    model = ROLE_MODELS.get(role)
    if model is None:
        flash("Select a valid account type.", "error")
        return redirect(url_for("admin.users"))

    account = db.session.get(model, account_id)
    if account is None:
        flash("Account not found.", "error")
        return redirect(url_for("admin.users", role=role))

    db.session.delete(account)
    db.session.commit()
    flash("Account removed.", "success")
    return redirect(url_for("admin.users", role=role))


@admin_bp.route("/analytics")
@role_required("administrator")
def analytics():
    return render_template(
        "administrator/analytics.html",
        domestic_users=DomesticUser.query.count(),
        enterprise_users=EnterpriseUser.query.count(),
        buildings=Building.query.count(),
        appliances=Appliance.query.count(),
    )


@admin_bp.route("/alerts")
@role_required("administrator")
def alerts():
    active = Alert.query.filter_by(resolved=False).order_by(Alert.created_at.desc()).all()
    resolved = Alert.query.filter_by(resolved=True).order_by(Alert.created_at.desc()).all()
    return render_template("administrator/alerts.html", active=active, resolved=resolved)


@admin_bp.route("/reports")
@role_required("administrator")
def reports():
    reports = Report.query.filter(
        or_(Report.owner_role == "system", Report.owner_role == "system-wide")
    ).order_by(Report.generated_at.desc()).all()
    return render_template("administrator/reports.html", reports=reports)
