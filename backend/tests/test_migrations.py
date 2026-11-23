from sqlalchemy import create_engine, inspect, text

from migrations.upgrade import upgrade_report_summary


def test_report_summary_migration_is_idempotent():
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE REPORT (id INTEGER PRIMARY KEY, title VARCHAR(180) NOT NULL)"
        ))

    upgrade_report_summary(engine)
    upgrade_report_summary(engine)

    columns = {column["name"] for column in inspect(engine).get_columns("REPORT")}
    assert "summary" in columns
