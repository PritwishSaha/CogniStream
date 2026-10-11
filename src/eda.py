import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# -----------------------------------------
# 1. LOAD THE CLEANED DATASET
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "cleaned_events_realistic.csv"
)

OUTPUT_DIR = PROJECT_DIR / "reports" / "eda_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

sns.set_theme(style="whitegrid")

print("=" * 55)
print("COGNISTREAM - EXPLORATORY DATA ANALYSIS")
print("=" * 55)

# -----------------------------------------
# 2. BASIC DATASET SUMMARY
# -----------------------------------------

print("\n1. DATASET OVERVIEW")

print(f"Total events: {len(df):,}")
print(f"Unique developers: {df['developer_id'].nunique()}")
print(f"Number of teams: {df['team'].nunique()}")
print(f"Start date: {df['timestamp'].min()}")
print(f"End date: {df['timestamp'].max()}")

print("\nDataset information:")
print(df.info())

print("\nNumerical summary:")
print(df[["duration_minutes"]].describe())

# -----------------------------------------
# 3. EVENT TYPE DISTRIBUTION
# -----------------------------------------

event_counts = df["event_type"].value_counts()

print("\n2. EVENT TYPE DISTRIBUTION")
print(event_counts)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=event_counts.index,
    y=event_counts.values
)

plt.title("Distribution of Developer Events")
plt.xlabel("Event Type")
plt.ylabel("Number of Events")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "event_distribution.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 4. TEAM ACTIVITY
# -----------------------------------------

team_counts = (
    df.groupby("team")
    .size()
    .sort_values(ascending=False)
)

print("\n3. TEAM ACTIVITY")
print(team_counts)

plt.figure(figsize=(9, 5))

sns.barplot(
    x=team_counts.index,
    y=team_counts.values
)

plt.title("Recorded Events by Team")
plt.xlabel("Team")
plt.ylabel("Number of Events")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "team_activity.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 5. DEVELOPER ACTIVITY
# -----------------------------------------

developer_counts = (
    df.groupby("developer_id")
    .size()
    .sort_values(ascending=False)
)

print("\n4. TOP 10 DEVELOPERS BY EVENT COUNT")
print(developer_counts.head(10))

plt.figure(figsize=(10, 6))

sns.barplot(
    x=developer_counts.head(10).values,
    y=developer_counts.head(10).index
)

plt.title("Top 10 Developers by Recorded Events")
plt.xlabel("Number of Events")
plt.ylabel("Developer")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "developer_activity.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 6. DAILY ACTIVITY TREND
# -----------------------------------------

df["date"] = df["timestamp"].dt.date

daily_activity = (
    df.groupby("date")
    .size()
    .rename("event_count")
)

print("\n5. DAILY ACTIVITY SUMMARY")
print(daily_activity.describe())

plt.figure(figsize=(12, 5))

sns.lineplot(
    x=daily_activity.index,
    y=daily_activity.values
)

plt.title("Daily Developer Event Volume")
plt.xlabel("Date")
plt.ylabel("Number of Events")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "daily_activity.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 7. EVENT DURATION DISTRIBUTION
# -----------------------------------------

print("\n6. DURATION STATISTICS")
print(df["duration_minutes"].describe())

plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="duration_minutes",
    bins=30,
    kde=True
)

plt.title("Distribution of Recorded Event Durations")
plt.xlabel("Duration in Minutes")
plt.ylabel("Number of Events")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "duration_distribution.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 8. ACTIVITY BY HOUR
# -----------------------------------------

df["hour"] = df["timestamp"].dt.hour

hourly_activity = (
    df.groupby("hour")
    .size()
    .reindex(range(24), fill_value=0)
)

print("\n7. ACTIVITY BY HOUR")
print(hourly_activity)

plt.figure(figsize=(11, 5))

sns.barplot(
    x=hourly_activity.index,
    y=hourly_activity.values
)

plt.title("Recorded Events by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Events")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "hourly_activity.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 9. EVENT TYPE BY TEAM
# -----------------------------------------

team_event_counts = pd.crosstab(
    df["team"],
    df["event_type"]
)

print("\n8. EVENT TYPE BY TEAM")
print(team_event_counts)

plt.figure(figsize=(11, 6))

sns.heatmap(
    team_event_counts,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title("Event Type Distribution by Team")
plt.xlabel("Event Type")
plt.ylabel("Team")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "team_event_heatmap.png",
    dpi=150
)

plt.close()

# -----------------------------------------
# 10. NUMPY SUMMARY
# -----------------------------------------

durations = df["duration_minutes"].to_numpy()

print("\n9. NUMPY ANALYSIS")

print(f"Mean duration: {np.mean(durations):.2f} minutes")
print(f"Median duration: {np.median(durations):.2f} minutes")
print(f"Standard deviation: {np.std(durations):.2f} minutes")

# -----------------------------------------
# 11. SAVE SUMMARY TABLES
# -----------------------------------------

event_counts.rename("event_count").to_csv(
    OUTPUT_DIR / "event_summary.csv"
)

team_counts.rename("event_count").to_csv(
    OUTPUT_DIR / "team_summary.csv"
)

developer_counts.rename("event_count").to_csv(
    OUTPUT_DIR / "developer_summary.csv"
)

daily_activity.to_csv(
    OUTPUT_DIR / "daily_summary.csv"
)

team_event_counts.to_csv(
    OUTPUT_DIR / "team_event_summary.csv"
)

print("\n" + "=" * 55)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 55)

print(f"Charts and summary tables saved to:\n{OUTPUT_DIR}")
# --------------------------------------------------
# 12. IDE SESSION ANALYSIS
# --------------------------------------------------

SESSION_FILE = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "ide_sessions.csv"
)

sessions = pd.read_csv(SESSION_FILE)

print("\n10. IDE SESSION ANALYSIS")

print(f"Total estimated IDE sessions: {len(sessions):,}")

print("\nSession elapsed-time statistics:")
print(sessions["elapsed_minutes"].describe())


# --------------------------------------------------
# 13. SESSION DURATION DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(10, 5))

sns.histplot(
    data=sessions,
    x="elapsed_minutes",
    bins=30,
    kde=True
)

plt.title("Distribution of Estimated IDE Session Duration")
plt.xlabel("Elapsed Session Duration (Minutes)")
plt.ylabel("Number of Sessions")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "session_duration_distribution.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 14. AVERAGE SESSION DURATION BY TEAM
# --------------------------------------------------

team_session_duration = (
    sessions.groupby("team")["elapsed_minutes"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE SESSION ELAPSED TIME BY TEAM")
print(team_session_duration)

plt.figure(figsize=(9, 5))

sns.barplot(
    x=team_session_duration.index,
    y=team_session_duration.values
)

plt.title("Average Estimated IDE Session Duration by Team")
plt.xlabel("Team")
plt.ylabel("Average Elapsed Duration (Minutes)")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "average_session_duration_by_team.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 15. SESSION COUNT BY DEVELOPER
# --------------------------------------------------

developer_sessions = (
    sessions.groupby("developer_id")
    .size()
    .sort_values(ascending=False)
)

print("\nIDE SESSION COUNT BY DEVELOPER")
print(developer_sessions.to_string())

plt.figure(figsize=(11, 7))

sns.barplot(
    x=developer_sessions.values,
    y=developer_sessions.index
)

plt.title("Estimated IDE Sessions by Developer")
plt.xlabel("Number of Sessions")
plt.ylabel("Developer")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "developer_session_counts.png",
    dpi=150
)

plt.close()


# --------------------------------------------------
# 16. SAVE SESSION SUMMARY TABLES
# --------------------------------------------------

team_session_duration.rename(
    "average_elapsed_minutes"
).to_csv(
    OUTPUT_DIR / "team_session_duration_summary.csv"
)

developer_sessions.rename(
    "session_count"
).to_csv(
    OUTPUT_DIR / "developer_session_summary.csv"
)

print("\nSESSION EDA COMPLETED SUCCESSFULLY")