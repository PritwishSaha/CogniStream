import pandas as pd
from pathlib import Path

# ==========================================
# COGNISTREAM: DATA CLEANING AND VALIDATION
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Input: realistic synthetic developer events
INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "developer_events_realistic.csv"
)

# Output: cleaned realistic dataset
OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "cleaned_events_realistic.csv"
)

# Output: data quality report
REPORT_FILE = (
    PROJECT_DIR
    / "reports"
    / "data_quality_report.txt"
)

# Valid event types in CogniStream
VALID_EVENT_TYPES = {
    "IDE_ACTIVE",
    "GITHUB_COMMIT",
    "SLACK_NOTIFICATION",
    "TASK_SWITCH",
    "MEETING",
}


def main():
    # 1. Check whether the input file exists
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_FILE}\n"
            "Run src/generate_realistic_data.py first."
        )

    # 2. Load raw data
    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "event_id",
        "timestamp",
        "developer_id",
        "team",
        "event_type",
        "duration_minutes",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {sorted(missing_columns)}"
        )

    original_rows = len(df)

    print("=" * 60)
    print("COGNISTREAM DATA QUALITY CHECK")
    print("=" * 60)

    print("\n1. Original Dataset")
    print(f"Rows: {original_rows}")
    print(f"Columns: {len(df.columns)}")

    # 3. Check missing values before cleaning
    print("\n2. Missing Values Before Cleaning")
    print(df.isnull().sum())

    # 4. Check duplicate event IDs
    duplicate_ids = df["event_id"].duplicated().sum()

    print("\n3. Duplicate Event IDs")
    print(duplicate_ids)

    # 5. Convert timestamps
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )

    invalid_timestamps = df["timestamp"].isna().sum()

    print("\n4. Invalid Timestamps")
    print(invalid_timestamps)

    # 6. Validate event types
    invalid_event_types = ~df["event_type"].isin(
        VALID_EVENT_TYPES
    )

    print("\n5. Invalid Event Types")
    print(invalid_event_types.sum())

    # 7. Convert duration to numeric
    df["duration_minutes"] = pd.to_numeric(
        df["duration_minutes"],
        errors="coerce",
    )

    invalid_durations = (
        df["duration_minutes"].isna()
        | (df["duration_minutes"] < 0)
    )

    print("\n6. Invalid Durations")
    print(invalid_durations.sum())

    # 8. Remove duplicate event IDs
    df = df.drop_duplicates(
        subset=["event_id"],
        keep="first",
    )

    # 9. Remove rows missing essential information
    df = df.dropna(
        subset=[
            "event_id",
            "developer_id",
            "team",
            "timestamp",
            "event_type",
            "duration_minutes",
        ]
    )

    # 10. Remove invalid event types
    df = df[
        df["event_type"].isin(VALID_EVENT_TYPES)
    ]

    # 11. Remove negative durations
    df = df[
        df["duration_minutes"] >= 0
    ]

    # 12. Sort events chronologically
    df = df.sort_values(
        ["developer_id", "timestamp"]
    ).reset_index(drop=True)

    # 13. Save cleaned data
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # 14. Generate data quality report
    report = f"""
COGNISTREAM DATA QUALITY REPORT
================================

Input Dataset: {INPUT_FILE.name}
Output Dataset: {OUTPUT_FILE.name}

Original Rows: {original_rows}
Cleaned Rows: {len(df)}
Removed Rows: {original_rows - len(df)}

Number of Columns: {len(df.columns)}
Unique Developers: {df['developer_id'].nunique()}
Unique Teams: {df['team'].nunique()}

Remaining Duplicate Event IDs:
{df['event_id'].duplicated().sum()}

Missing Values After Cleaning:
{df.isnull().sum().to_string()}

Event Distribution:
{df['event_type'].value_counts().to_string()}

Duration Summary:
{df['duration_minutes'].describe().to_string()}

Timestamp Range:
Start: {df['timestamp'].min()}
End: {df['timestamp'].max()}
"""

    REPORT_FILE.write_text(
        report,
        encoding="utf-8",
    )

    # 15. Display results
    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETED")
    print("=" * 60)

    print(f"\nInput file: {INPUT_FILE}")
    print(f"Cleaned file: {OUTPUT_FILE}")
    print(f"Quality report: {REPORT_FILE}")

    print(f"\nRows before cleaning: {original_rows}")
    print(f"Rows after cleaning: {len(df)}")
    print(f"Rows removed: {original_rows - len(df)}")

    print("\nCleaned dataset preview:")
    print(df.head())

    print("\nMissing values after cleaning:")
    print(df.isnull().sum())


if __name__ == "__main__":
    main()