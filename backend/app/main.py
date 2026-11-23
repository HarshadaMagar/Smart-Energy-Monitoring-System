from flask import Blueprint, render_template

from app.auth import role_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/health")
def health():
    return {"status": "ok"}, 200



@main_bp.route("/domestic")
@role_required("domestic")
def domestic_dashboard():
    return render_template("dashboard.html", role="domestic", title="Domestic Dashboard")
