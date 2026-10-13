from pathlib import Path

import duckdb


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_PATH = PROJECT_ROOT / "cognistream.duckdb"

# CSV files to import
CSV_FILES = {
    "events": "events_analyzed.csv",
    "developer_metrics": "developer_metrics.csv",
    "ide_sessions": "ide_sessions.csv",
    "ide_events_with_sessions": "ide_events_with_sessions.csv",
    "team_metrics": "team_metrics.csv",
}


def main():
    print("=" * 60)
    print("CogniStream - DuckDB Data Loader")
    print("=" * 60)

    # Verify that every required CSV exists before importing.
    missing_files = [
        filename
        for filename in CSV_FILES.values()
        if not (DATA_DIR / filename).is_file()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Missing required CSV files: {missing_files}"
        )

    connection = duckdb.connect(str(DATABASE_PATH))

    try:
        for table_name, filename in CSV_FILES.items():
            csv_path = (DATA_DIR / filename).resolve()

            # Read the CSV and replace the corresponding imported table.
            connection.execute(
                f"""
                CREATE OR REPLACE TABLE {table_name} AS
                SELECT *
                FROM read_csv_auto(?, header = true)
                """,
                [str(csv_path)],
            )

            row_count = connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            columns = connection.execute(
                f"DESCRIBE {table_name}"
            ).fetchall()

            print(f"\nTable: {table_name}")
            print(f"Source: {filename}")
            print(f"Rows imported: {row_count}")
            print("Columns:")

            for column in columns:
                print(f"  - {column[0]} ({column[1]})")

        print("\n" + "=" * 60)
        print("DATABASE IMPORT COMPLETED")
        print(f"Database: {DATABASE_PATH}")
        print("=" * 60)

        # Final table inventory
        print("\nImported table summary:")

        tables = connection.execute(
            "SHOW TABLES"
        ).fetchall()

        for (table_name,) in tables:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(f"{table_name}: {count:,} rows")

    finally:
        connection.close()


if __name__ == "__main__":
    main()

