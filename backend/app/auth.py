import re
import uuid
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import bcrypt, db
from app.models import DomesticUser, EnterpriseUser, SystemAdministrator

auth_bp = Blueprint("auth", __name__)

ROLE_MODELS = {
    "administrator": (SystemAdministrator, "ADM"),
    "enterprise": (EnterpriseUser, "ENT"),
    "domestic": (DomesticUser, "DOM"),
}

ORGANIZATION_TYPES = (
    "Corporate",
    "Educational",
    "Healthcare",
    "Government",
    "Industrial",
    "Retail",
    "Other",
)


def generate_account_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:10].upper()}"


def validate_email(email):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email or "", re.ASCII))


def validate_registration(role, form):
    errors = {}
    required = ("name", "email", "password", "contact_number")

    for field in required:
        if not form.get(field, "").strip():
            errors[field] = "This field is required."

    if form.get("email") and not validate_email(form["email"].strip()):
        errors["email"] = "Enter a valid email address."

    digits = re.sub(r"\D", "", form.get("contact_number", ""))
    if digits and len(digits) < 7:
        errors["contact_number"] = "Contact number must contain at least seven digits."

    password = form.get("password", "")
    if password and len(password) < 8:
        errors["password"] = "Password must contain at least eight characters."

    if role == "enterprise":
        if not form.get("organization_name", "").strip():
            errors["organization_name"] = "Organization name is required."
        if form.get("organization_type") not in ORGANIZATION_TYPES:
            errors["organization_type"] = "Select a valid organization type."

    return errors


def find_account(role, email):
    model, _ = ROLE_MODELS[role]
    return model.query.filter_by(email=email.lower()).first()


def role_required(role):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "role" not in session or "account_id" not in session:
                flash("Please log in to continue.", "error")
                return redirect(url_for("auth.login"))
            if session["role"] != role:
                return "Forbidden", 403
            return view(*args, **kwargs)
        return wrapped
    return decorator


@auth_bp.route("/auth", methods=["GET"])
def auth_entry():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if role not in ROLE_MODELS:
            flash("Select a valid role.", "error")
            return render_template("auth.html", mode="login", organization_types=ORGANIZATION_TYPES), 400

        account = find_account(role, email)
        if account is None or not account.active:
            flash("Invalid email, password, or inactive account.", "error")
            return render_template("auth.html", mode="login", organization_types=ORGANIZATION_TYPES), 401

        if not bcrypt.check_password_hash(account.password_hash, password):
            flash("Invalid email, password, or inactive account.", "error")
            return render_template("auth.html", mode="login", organization_types=ORGANIZATION_TYPES), 401

        session.clear()
        session["account_id"] = account.id
        session["role"] = role
        session["name"] = account.name
        flash("Login successful.", "success")
        dashboard_endpoints = {
            "administrator": "admin.administrator_dashboard",
            "enterprise": "enterprise.dashboard",
            "domestic": "main.domestic_dashboard",
        }
        return redirect(url_for(dashboard_endpoints[role]))

    return render_template("auth.html", mode="login", organization_types=ORGANIZATION_TYPES)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    role = request.args.get("role", "domestic")

    if request.method == "POST":
        role = request.form.get("role")
        if role not in ROLE_MODELS:
            flash("Select a valid role.", "error")
            return render_template("auth.html", mode="register", organization_types=ORGANIZATION_TYPES), 400

        errors = validate_registration(role, request.form)
        if errors:
            return render_template(
                "auth.html",
                mode="register",
                role=role,
                organization_types=ORGANIZATION_TYPES,
                errors=errors,
                form=request.form,
            ), 400

        email = request.form["email"].strip().lower()
        model, prefix = ROLE_MODELS[role]
        if model.query.filter_by(email=email).first():
            errors["email"] = "This email is already registered for this role."
            return render_template(
                "auth.html",
                mode="register",
                role=role,
                organization_types=ORGANIZATION_TYPES,
                errors=errors,
                form=request.form,
            ), 409

        values = {
            "id": generate_account_id(prefix),
            "name": request.form["name"].strip(),
            "email": email,
            "password_hash": bcrypt.generate_password_hash(request.form["password"]).decode("utf-8"),
            "contact_number": request.form["contact_number"].strip(),
            "active": True,
        }

        if role == "enterprise":
            values["organization_name"] = request.form["organization_name"].strip()
            values["organization_type"] = request.form["organization_type"]

        account = model(**values)
        db.session.add(account)
        db.session.commit()

        flash("Account created successfully.", "success")
        return redirect(url_for("auth.login"))

    if role not in ROLE_MODELS:
        role = "domestic"
    return render_template(
        "auth.html",
        mode="register",
        role=role,
        organization_types=ORGANIZATION_TYPES,
        form=request.args,
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
