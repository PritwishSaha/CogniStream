import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible synthetic data
rng = np.random.default_rng(42)

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_DIR / "data" / "raw" / "developer_events.csv"

# Configuration
NUM_EVENTS = 10_000
NUM_DEVELOPERS = 20

developers = [
    f"DEV{i:03d}"
    for i in range(1, NUM_DEVELOPERS + 1)
]

teams = [
    "Backend",
    "Frontend",
    "Data",
    "DevOps"
]

event_types = [
    "IDE_ACTIVE",
    "GITHUB_COMMIT",
    "SLACK_NOTIFICATION",
    "TASK_SWITCH",
    "MEETING"
]

sources = {
    "IDE_ACTIVE": "IDE",
    "GITHUB_COMMIT": "GitHub",
    "SLACK_NOTIFICATION": "Slack",
    "TASK_SWITCH": "IDE",
    "MEETING": "Calendar"
}

# Generate event timestamps across 30 days
start_date = pd.Timestamp("2026-09-01")

timestamps = (
    start_date
    + pd.to_timedelta(
        rng.integers(0, 30 * 24 * 60, NUM_EVENTS),
        unit="m"
    )
)

# Generate event types
event_probabilities = [0.55, 0.12, 0.18, 0.10, 0.05]

generated_event_types = rng.choice(
    event_types,
    size=NUM_EVENTS,
    p=event_probabilities
)

# Create dataset
df = pd.DataFrame({
    "event_id": [
        f"E{i:06d}"
        for i in range(1, NUM_EVENTS + 1)
    ],
    "developer_id": rng.choice(
        developers,
        size=NUM_EVENTS
    ),
    "timestamp": timestamps,
    "event_type": generated_event_types,
})

# Assign each developer to a consistent team
team_mapping = {
    developer: teams[(i // 5)]
    for i, developer in enumerate(developers)
}

df["team"] = df["developer_id"].map(team_mapping)

# Assign source based on event type
df["source"] = df["event_type"].map(sources)

# Add synthetic duration where applicable
duration_ranges = {
    "IDE_ACTIVE": (5, 60),
    "GITHUB_COMMIT": (0, 1),
    "SLACK_NOTIFICATION": (0, 1),
    "TASK_SWITCH": (0, 1),
    "MEETING": (15, 90)
}

df["duration_minutes"] = [
    int(rng.integers(*duration_ranges[event]))
    for event in df["event_type"]
]

# Assign a task identifier where appropriate
df["task_id"] = [
    f"TASK{rng.integers(1, 101):03d}"
    if event in ["IDE_ACTIVE", "GITHUB_COMMIT", "TASK_SWITCH"]
    else None
    for event in df["event_type"]
]

# Sort events chronologically
df = df.sort_values(
    ["developer_id", "timestamp"]
).reset_index(drop=True)

# Save dataset
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(OUTPUT_FILE, index=False)

# Display basic information
print("Dataset generated successfully!")
print(f"Output file: {OUTPUT_FILE}")
print(f"Total events: {len(df)}")
print(f"Unique developers: {df['developer_id'].nunique()}")
print(f"Teams: {df['team'].nunique()}")

print("\nEvent distribution:")
print(df["event_type"].value_counts())

print("\nFirst five rows:")
print(df.head())