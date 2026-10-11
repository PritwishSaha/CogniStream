from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# COGNISTREAM: REALISTIC SYNTHETIC DEVELOPER ACTIVITY GENERATOR
# ============================================================

SEED = 42
rng = np.random.default_rng(SEED)

PROJECT_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "developer_events_realistic.csv"
)

DEVELOPERS = [f"DEV{i:03d}" for i in range(1, 21)]

TEAMS = ["Backend", "Frontend", "Data", "DevOps"]

TEAM_MAPPING = {
    developer: TEAMS[i // 5]
    for i, developer in enumerate(DEVELOPERS)
}

EVENT_TYPES = [
    "IDE_ACTIVE",
    "GITHUB_COMMIT",
    "SLACK_NOTIFICATION",
    "TASK_SWITCH",
    "MEETING",
]

records = []
event_number = 1

START_DATE = pd.Timestamp("2026-09-01")


# ============================================================
# HELPER: RECORD AN EVENT
# ============================================================

def add_event(
    developer,
    timestamp,
    event_type,
    source,
    duration,
    task_id=None,
):
    global event_number

    records.append({
        "event_id": f"E{event_number:07d}",
        "developer_id": developer,
        "team": TEAM_MAPPING[developer],
        "timestamp": timestamp,
        "event_type": event_type,
        "source": source,
        "duration_minutes": int(duration),
        "task_id": task_id,
    })

    event_number += 1


# ============================================================
# GENERATE 30 CALENDAR DAYS OF ACTIVITY
# WEEKENDS ARE EXCLUDED
# ============================================================

for day in range(30):

    current_date = START_DATE + pd.Timedelta(days=day)

    if current_date.weekday() >= 5:
        continue

    for developer in DEVELOPERS:

        # Work begins between 9 AM and 10 AM.
        work_start = current_date + pd.Timedelta(
            minutes=int(rng.integers(9 * 60, 10 * 60 + 1))
        )

        work_end = work_start + pd.Timedelta(hours=8)

        current_time = work_start

        # ----------------------------------------------------
        # GENERATE THE WORKDAY
        # ----------------------------------------------------

        while current_time < work_end:

            activity = rng.choice(
                [
                    "CODING_BLOCK",
                    "SLACK",
                    "MEETING",
                    "TASK_SWITCH",
                ],
                p=[0.62, 0.18, 0.10, 0.10],
            )

            # =================================================
            # CODING BLOCK
            # =================================================

            if activity == "CODING_BLOCK":

                number_of_ide_events = int(rng.integers(2, 6))

                task_id = f"TASK{rng.integers(1, 101):03d}"

                for event_index in range(number_of_ide_events):

                    if current_time >= work_end:
                        break

                    remaining_minutes = int(
                        (work_end - current_time).total_seconds() / 60
                    )

                    if remaining_minutes <= 0:
                        break

                    # An IDE event represents a short observation
                    # of coding activity, not an entire coding block.
                    duration = min(
                        int(rng.integers(5, 11)),
                        remaining_minutes,
                    )

                    add_event(
                        developer=developer,
                        timestamp=current_time,
                        event_type="IDE_ACTIVE",
                        source="IDE",
                        duration=duration,
                        task_id=task_id,
                    )

                    # Advance by a short interval so consecutive
                    # IDE events can belong to the same session.
                    interval_minutes = int(rng.integers(5, 11))

                    current_time += pd.Timedelta(
                        minutes=interval_minutes
                    )

                    if current_time >= work_end:
                        break

                    # A GitHub commit can occur during coding.
                    if rng.random() < 0.12:

                        remaining_minutes = int(
                            (work_end - current_time).total_seconds()
                            / 60
                        )

                        if remaining_minutes <= 0:
                            break

                        commit_duration = min(
                            int(rng.integers(1, 4)),
                            remaining_minutes,
                        )

                        add_event(
                            developer=developer,
                            timestamp=current_time,
                            event_type="GITHUB_COMMIT",
                            source="GitHub",
                            duration=commit_duration,
                            task_id=task_id,
                        )

                        current_time += pd.Timedelta(
                            minutes=commit_duration
                        )

                # A short break after the coding block.
                if current_time < work_end:

                    break_minutes = int(rng.integers(5, 16))

                    current_time += pd.Timedelta(
                        minutes=break_minutes
                    )

            # =================================================
            # SLACK NOTIFICATION
            # =================================================

            elif activity == "SLACK":

                remaining_minutes = int(
                    (work_end - current_time).total_seconds() / 60
                )

                if remaining_minutes <= 0:
                    break

                duration = min(
                    int(rng.integers(1, 4)),
                    remaining_minutes,
                )

                add_event(
                    developer=developer,
                    timestamp=current_time,
                    event_type="SLACK_NOTIFICATION",
                    source="Slack",
                    duration=duration,
                    task_id=None,
                )

                current_time += pd.Timedelta(
                    minutes=duration + int(rng.integers(2, 8))
                )

            # =================================================
            # MEETING
            # =================================================

            elif activity == "MEETING":

                remaining_minutes = int(
                    (work_end - current_time).total_seconds() / 60
                )

                if remaining_minutes <= 0:
                    break

                duration = min(
                    int(rng.choice([15, 30, 45])),
                    remaining_minutes,
                )

                add_event(
                    developer=developer,
                    timestamp=current_time,
                    event_type="MEETING",
                    source="Calendar",
                    duration=duration,
                    task_id=None,
                )

                current_time += pd.Timedelta(
                    minutes=duration + int(rng.integers(3, 11))
                )

            # =================================================
            # TASK SWITCH
            # =================================================

            else:

                remaining_minutes = int(
                    (work_end - current_time).total_seconds() / 60
                )

                if remaining_minutes <= 0:
                    break

                duration = min(
                    int(rng.integers(1, 4)),
                    remaining_minutes,
                )

                task_id = f"TASK{rng.integers(1, 101):03d}"

                add_event(
                    developer=developer,
                    timestamp=current_time,
                    event_type="TASK_SWITCH",
                    source="IDE",
                    duration=duration,
                    task_id=task_id,
                )

                current_time += pd.Timedelta(
                    minutes=duration + int(rng.integers(3, 9))
                )


# ============================================================
# CREATE AND VALIDATE DATASET
# ============================================================

df = pd.DataFrame(records)

df = df.sort_values(
    ["developer_id", "timestamp", "event_id"]
).reset_index(drop=True)

required_columns = [
    "event_id",
    "developer_id",
    "team",
    "timestamp",
    "event_type",
    "source",
    "duration_minutes",
    "task_id",
]

assert list(df.columns) == required_columns
assert df["event_id"].is_unique
assert df["developer_id"].nunique() == 20
assert df["team"].nunique() == 4
assert df["timestamp"].notna().all()
assert df["duration_minutes"].notna().all()
assert (df["duration_minutes"] > 0).all()
assert set(df["event_type"].unique()).issubset(EVENT_TYPES)

# Verify that all expected event types are represented.
assert set(EVENT_TYPES).issubset(set(df["event_type"].unique()))

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

df.to_csv(OUTPUT_FILE, index=False)


# ============================================================
# GENERATION REPORT
# ============================================================

print("=" * 65)
print("COGNISTREAM REALISTIC SYNTHETIC DATA GENERATED")
print("=" * 65)

print(f"Total events: {len(df):,}")
print(f"Unique developers: {df['developer_id'].nunique()}")
print(f"Teams: {df['team'].nunique()}")
print(f"Unique event IDs: {df['event_id'].nunique()}")
print(f"Duplicate event IDs: {df['event_id'].duplicated().sum()}")

print(f"Start timestamp: {df['timestamp'].min()}")
print(f"End timestamp: {df['timestamp'].max()}")

print("\nEVENT DISTRIBUTION")
print(df["event_type"].value_counts().to_string())

print("\nTEAM DISTRIBUTION")
print(df["team"].value_counts().to_string())

print("\nDATA VALIDATION")
print(f"Missing timestamps: {df['timestamp'].isna().sum()}")
print(f"Missing developer IDs: {df['developer_id'].isna().sum()}")
print(f"Missing event types: {df['event_type'].isna().sum()}")
print(f"Non-positive durations: {(df['duration_minutes'] <= 0).sum()}")

print(f"\nSaved to: {OUTPUT_FILE}")
print("\nDATA GENERATION COMPLETED SUCCESSFULLY")