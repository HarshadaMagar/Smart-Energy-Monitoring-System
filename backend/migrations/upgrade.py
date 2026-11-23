import os
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BACKEND_DIR)

from sqlalchemy import inspect, text

from app import create_app, db


def upgrade_report_summary(engine):
    inspector = inspect(engine)
    if "REPORT" not in inspector.get_table_names():
        raise RuntimeError("REPORT table is missing; initialize the application schema first.")

    columns = {column["name"] for column in inspector.get_columns("REPORT")}
    if "summary" not in columns:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE REPORT ADD COLUMN summary TEXT NULL"))


def main():
    app = create_app()
    with app.app_context():
        upgrade_report_summary(db.engine)
    print("Database schema is up to date.")


if __name__ == "__main__":
    main()
