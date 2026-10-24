
from pathlib import Path

import duckdb

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "cognistream.duckdb"
OUTPUT_DIR = PROJECT_ROOT / "data" / "powerbi"
OUTPUT_FILE = OUTPUT_DIR / "developer_analytics.csv"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    connection = duckdb.connect(
        str(DATABASE_PATH),
        read_only=True
    )

    try:
        query = """
        SELECT
            developer_id,
            team,
            GITHUB_COMMIT,
            IDE_ACTIVE,
            MEETING,
            SLACK_NOTIFICATION,
            TASK_SWITCH,
            session_count,
            avg_recorded_ide_minutes,
            total_recorded_ide_minutes,
            avg_session_elapsed_minutes,
            avg_ide_events_per_session,
            interruption_event_count,
            task_switch_event_count
        FROM developer_metrics
        ORDER BY team, developer_id
        """

        df = connection.execute(query).fetchdf()

        df.to_csv(OUTPUT_FILE, index=False)

        print("Developer analytics export completed.")
        print(f"Output file: {OUTPUT_FILE}")
        print(f"Rows exported: {len(df)}")
        print(f"Columns exported: {len(df.columns)}")

        print("\nDeveloper counts by team:")
        print(df.groupby("team")["developer_id"].nunique())

        print("\nPreview:")
        print(df.head().to_string(index=False))

    finally:
        connection.close()

if __name__ == "__main__":
    main()