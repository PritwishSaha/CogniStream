
from pathlib import Path

import duckdb


# ---------------------------------------------------------
# CogniStream: Export analytical views for Power BI
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = PROJECT_ROOT / "cognistream.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "data" / "powerbi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


VIEWS = {
    "vw_event_overview": "event_overview.csv",
    "vw_team_activity": "team_activity.csv",
    "vw_session_quality": "session_quality.csv",
}


def main():
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"DuckDB database not found: {DATABASE_PATH}"
        )

    print("=" * 65)
    print("COGNISTREAM - POWER BI DATA EXPORT")
    print("=" * 65)

    con = duckdb.connect(
        str(DATABASE_PATH),
        read_only=True,
    )

    try:
        for view_name, filename in VIEWS.items():
            output_path = OUTPUT_DIR / filename

            row_count = con.execute(
                f"SELECT COUNT(*) FROM {view_name}"
            ).fetchone()[0]

            con.execute(
                f"""
                COPY (
                    SELECT *
                    FROM {view_name}
                )
                TO '{output_path.as_posix()}'
                (HEADER, DELIMITER ',');
                """
            )

            print(f"\nView: {view_name}")
            print(f"File: {output_path}")
            print(f"Rows: {row_count:,}")
            print("Status: Export successful")

    finally:
        con.close()

    print("\n" + "=" * 65)
    print("POWER BI EXPORT COMPLETED")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 65)


if __name__ == "__main__":
    main()

