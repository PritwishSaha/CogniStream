
-- ============================================================
-- CogniStream: Developer Activity and IDE Analytics
-- Database: DuckDB
-- ============================================================


-- ============================================================
-- 1. DATABASE TABLE INVENTORY
-- ============================================================

SHOW TABLES;


-- ============================================================
-- 2. OVERALL EVENT SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_events,
    COUNT(DISTINCT event_id) AS unique_event_ids,
    COUNT(DISTINCT developer_id) AS unique_developers,
    COUNT(DISTINCT team) AS number_of_teams,
    MIN(timestamp) AS first_event_timestamp,
    MAX(timestamp) AS last_event_timestamp
FROM events;


-- ============================================================
-- 3. EVENT TYPE DISTRIBUTION
-- ============================================================

SELECT
    event_type,
    COUNT(*) AS event_count,
    ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_events
FROM events
GROUP BY event_type
ORDER BY event_count DESC;


-- ============================================================
-- 4. DATA QUALITY: MISSING VALUES
-- ============================================================

SELECT
    COUNT(*) FILTER (WHERE event_id IS NULL)
        AS missing_event_ids,

    COUNT(*) FILTER (WHERE developer_id IS NULL)
        AS missing_developer_ids,

    COUNT(*) FILTER (WHERE timestamp IS NULL)
        AS missing_timestamps,

    COUNT(*) FILTER (WHERE event_type IS NULL)
        AS missing_event_types,

    COUNT(*) FILTER (WHERE team IS NULL)
        AS missing_teams,

    COUNT(*) FILTER (WHERE duration_minutes IS NULL)
        AS missing_durations
FROM events;


-- ============================================================
-- 5. DATA QUALITY: DUPLICATE EVENT IDS
-- ============================================================

SELECT
    event_id,
    COUNT(*) AS occurrences
FROM events
WHERE event_id IS NOT NULL
GROUP BY event_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC, event_id;


-- ============================================================
-- 6. DATA QUALITY: INVALID OR NEGATIVE DURATIONS
-- ============================================================

SELECT
    COUNT(*) FILTER (
        WHERE duration_minutes < 0
    ) AS negative_durations,

    COUNT(*) FILTER (
        WHERE duration_minutes = 0
    ) AS zero_durations,

    COUNT(*) FILTER (
        WHERE duration_minutes IS NULL
    ) AS missing_durations
FROM events;


-- ============================================================
-- 7. DEVELOPER ACTIVITY OVERVIEW
-- ============================================================

SELECT
    developer_id,
    team,
    GITHUB_COMMIT AS github_commit_events,
    IDE_ACTIVE AS ide_active_events,
    MEETING AS meeting_events,
    SLACK_NOTIFICATION AS slack_notification_events,
    TASK_SWITCH AS task_switch_events,
    session_count,
    total_recorded_ide_minutes,
    ROUND(avg_session_elapsed_minutes, 2)
        AS avg_session_elapsed_minutes,
    interruption_event_count
FROM developer_metrics
ORDER BY total_recorded_ide_minutes DESC;


-- ============================================================
-- 8. TEAM ACTIVITY COMPARISON
-- ============================================================

SELECT
    team,
    developer_count,
    GITHUB_COMMIT AS github_commit_events,
    IDE_ACTIVE AS ide_active_events,
    MEETING AS meeting_events,
    SLACK_NOTIFICATION AS slack_notification_events,
    TASK_SWITCH AS task_switch_events,
    total_sessions,
    total_recorded_ide_minutes,
    ROUND(average_session_elapsed_minutes, 2)
        AS avg_session_elapsed_minutes,
    ROUND(average_ide_events_per_session, 2)
        AS avg_ide_events_per_session
FROM team_metrics
ORDER BY total_recorded_ide_minutes DESC;


-- ============================================================
-- 9. IDE SESSION SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_sessions,
    COUNT(DISTINCT developer_id) AS developers_with_sessions,
    ROUND(AVG(recorded_ide_minutes), 2)
        AS avg_recorded_ide_minutes,
    ROUND(AVG(elapsed_minutes), 2)
        AS avg_elapsed_minutes,
    ROUND(AVG(ide_event_count), 2)
        AS avg_ide_events_per_session,
    MAX(elapsed_minutes) AS longest_elapsed_session_minutes
FROM ide_sessions;


-- ============================================================
-- 10. SESSION TIME DIFFERENCE
-- ============================================================

SELECT
    developer_id,
    team,
    session_number,
    recorded_ide_minutes,
    elapsed_minutes,
    ROUND(
        elapsed_minutes - recorded_ide_minutes,
        2
    ) AS elapsed_minus_recorded_minutes,
    ide_event_count
FROM ide_sessions
WHERE elapsed_minutes IS NOT NULL
  AND recorded_ide_minutes IS NOT NULL
ORDER BY elapsed_minus_recorded_minutes DESC
LIMIT 20;


-- ============================================================
-- 11. DAILY EVENT ACTIVITY
-- ============================================================

SELECT
    CAST(timestamp AS DATE) AS activity_date,
    COUNT(*) AS total_events,
    COUNT(DISTINCT developer_id) AS active_developers,
    COUNT(*) FILTER (
        WHERE event_type = 'GITHUB_COMMIT'
    ) AS github_commit_events,
    COUNT(*) FILTER (
        WHERE event_type = 'IDE_ACTIVE'
    ) AS ide_active_events,
    COUNT(*) FILTER (
        WHERE event_type = 'TASK_SWITCH'
    ) AS task_switch_events
FROM events
GROUP BY CAST(timestamp AS DATE)
ORDER BY activity_date;


-- ============================================================
-- 12. EVENT ACTIVITY BY TEAM
-- ============================================================

SELECT
    team,
    event_type,
    COUNT(*) AS event_count,
    ROUND(AVG(duration_minutes), 2)
        AS avg_event_duration_minutes
FROM events
GROUP BY team, event_type
ORDER BY team, event_count DESC;

