from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. PATHS AND SETTINGS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "cleaned_events_realistic.csv"
OUTPUT_DIR = ROOT / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SESSION_GAP_MINUTES = 30


# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce"
)

required_columns = [
    "event_id",
    "developer_id",
    "timestamp",
    "event_type",
    "team",
    "duration_minutes",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

if df["event_id"].duplicated().any():
    raise ValueError("Duplicate event IDs detected.")

if df["timestamp"].isna().any():
    raise ValueError("Invalid or missing timestamps detected.")

if df["developer_id"].isna().any():
    raise ValueError("Missing developer IDs detected.")

if not df["duration_minutes"].ge(0).all():
    raise ValueError("Negative event durations detected.")


# --------------------------------------------------
# 3. SORT EVENTS
# --------------------------------------------------

df = df.sort_values(
    ["developer_id", "timestamp", "event_id"]
).reset_index(drop=True)

print("=" * 60)
print("COGNISTREAM SESSION ANALYSIS")
print("=" * 60)

print(f"Total events: {len(df):,}")
print(f"Unique developers: {df['developer_id'].nunique()}")
print(f"Teams: {df['team'].nunique()}")
print(f"Duplicate event IDs: {df['event_id'].duplicated().sum()}")


# --------------------------------------------------
# 4. IDENTIFY IDE SESSIONS
# --------------------------------------------------

# Only IDE_ACTIVE events can belong to a coding session.
ide = df.loc[df["event_type"] == "IDE_ACTIVE"].copy()

ide = ide.sort_values(
    ["developer_id", "timestamp", "event_id"]
).reset_index(drop=True)

# Calculate the time since the previous IDE event
# for the same developer.
ide["previous_ide_timestamp"] = (
    ide.groupby("developer_id")["timestamp"].shift(1)
)

ide["gap_minutes"] = (
    ide["timestamp"] - ide["previous_ide_timestamp"]
).dt.total_seconds() / 60

# Start a new session when:
# 1. This is the developer's first IDE event.
# 2. The gap exceeds the configured threshold.
ide["new_session"] = (
    ide["previous_ide_timestamp"].isna()
    | (ide["gap_minutes"] > SESSION_GAP_MINUTES)
)

# Number sessions separately for each developer.
ide["session_number"] = (
    ide.groupby("developer_id")["new_session"]
    .cumsum()
    .astype(int)
)

# Save IDE events with their session assignments.
ide_event_columns = [
    "event_id",
    "developer_id",
    "timestamp",
    "event_type",
    "team",
    "duration_minutes",
    "session_number",
]

ide[ide_event_columns].to_csv(
    OUTPUT_DIR / "ide_events_with_sessions.csv",
    index=False
)


# --------------------------------------------------
# 5. BUILD SESSION-LEVEL METRICS
# --------------------------------------------------

sessions = (
    ide.groupby(["developer_id", "session_number"], as_index=False)
    .agg(
        session_start=("timestamp", "min"),
        session_end=("timestamp", "max"),
        recorded_ide_minutes=("duration_minutes", "sum"),
        ide_event_count=("event_id", "count"),
        team=("team", "first"),
    )
)

# This is the elapsed time between the first and last
# IDE event timestamps in a session.
sessions["elapsed_minutes"] = (
    sessions["session_end"] - sessions["session_start"]
).dt.total_seconds() / 60

sessions["session_elapsed_minutes"] = sessions["elapsed_minutes"]

sessions.to_csv(
    OUTPUT_DIR / "ide_sessions.csv",
    index=False
)


# --------------------------------------------------
# 6. BUILD DEVELOPER METRICS
# --------------------------------------------------

event_counts = pd.crosstab(
    df["developer_id"],
    df["event_type"]
).reset_index()

# Make sure every expected event-type column exists.
expected_types = [
    "IDE_ACTIVE",
    "SLACK_NOTIFICATION",
    "GITHUB_COMMIT",
    "TASK_SWITCH",
    "MEETING",
]

for event_type in expected_types:
    if event_type not in event_counts.columns:
        event_counts[event_type] = 0

session_metrics = (
    sessions.groupby("developer_id", as_index=False)
    .agg(
        session_count=("session_number", "count"),
        avg_recorded_ide_minutes=("recorded_ide_minutes", "mean"),
        total_recorded_ide_minutes=("recorded_ide_minutes", "sum"),
        avg_session_elapsed_minutes=("elapsed_minutes", "mean"),
        avg_ide_events_per_session=("ide_event_count", "mean"),
    )
)

developer_metrics = event_counts.merge(
    session_metrics,
    on="developer_id",
    how="left"
)

developer_teams = (
    df.groupby("developer_id", as_index=False)
    .agg(team=("team", "first"))
)

developer_metrics = developer_teams.merge(
    developer_metrics,
    on="developer_id",
    how="left"
)

developer_metrics["session_count"] = (
    developer_metrics["session_count"].fillna(0).astype(int)
)

# These are total observed event counts, not necessarily
# interruptions that occurred during a coding session.
developer_metrics["interruption_event_count"] = (
    developer_metrics["SLACK_NOTIFICATION"]
    + developer_metrics["MEETING"]
)

developer_metrics["task_switch_event_count"] = (
    developer_metrics["TASK_SWITCH"]
)

developer_metrics.to_csv(
    OUTPUT_DIR / "developer_metrics.csv",
    index=False
)


# --------------------------------------------------
# 7. BUILD TEAM METRICS
# --------------------------------------------------

team_events = (
    df.pivot_table(
        index="team",
        columns="event_type",
        values="event_id",
        aggfunc="count",
        fill_value=0
    )
    .reset_index()
)

team_session_metrics = (
    sessions.groupby("team", as_index=False)
    .agg(
        total_sessions=("session_number", "count"),
        total_recorded_ide_minutes=("recorded_ide_minutes", "sum"),
        average_session_elapsed_minutes=("elapsed_minutes", "mean"),
        average_ide_events_per_session=("ide_event_count", "mean"),
    )
)

team_developer_counts = (
    df.groupby("team")["developer_id"]
    .nunique()
    .rename("developer_count")
    .reset_index()
)

team_metrics = (
    team_developer_counts
    .merge(team_events, on="team", how="left")
    .merge(team_session_metrics, on="team", how="left")
)

team_metrics.to_csv(
    OUTPUT_DIR / "team_metrics.csv",
    index=False
)


# --------------------------------------------------
# 8. SAVE ANALYZED EVENTS
# --------------------------------------------------

df.to_csv(
    OUTPUT_DIR / "events_analyzed.csv",
    index=False
)


# --------------------------------------------------
# 9. DISPLAY RESULTS
# --------------------------------------------------

print("\nEVENT DISTRIBUTION")
print(df["event_type"].value_counts().to_string())

print("\nSESSION SUMMARY")
print(f"Total IDE events: {len(ide):,}")
print(f"Total estimated IDE sessions: {len(sessions):,}")

print(
    "Average recorded IDE minutes per session: "
    f"{sessions['recorded_ide_minutes'].mean():.2f}"
)

print(
    "Average session elapsed minutes: "
    f"{sessions['elapsed_minutes'].mean():.2f}"
)

print(
    "Average IDE events per session: "
    f"{sessions['ide_event_count'].mean():.2f}"
)

print("\nSESSION DATA PREVIEW")
print(sessions.head(5).to_string(index=False))

print("\nTEAM METRICS")
print(team_metrics.to_string(index=False))

print("\nDEVELOPER METRICS PREVIEW")
print(developer_metrics.head(5).to_string(index=False))

print("\nFILES SAVED")
print(OUTPUT_DIR / "ide_events_with_sessions.csv")
print(OUTPUT_DIR / "ide_sessions.csv")
print(OUTPUT_DIR / "developer_metrics.csv")
print(OUTPUT_DIR / "team_metrics.csv")
print(OUTPUT_DIR / "events_analyzed.csv")

print("\nSESSION ANALYSIS COMPLETED SUCCESSFULLY")