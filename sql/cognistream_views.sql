-- =========================================================
-- CogniStream: Reusable Analytical Views
-- =========================================================


-- VIEW 1: Event-level analytical data
CREATE OR REPLACE VIEW vw_event_overview AS
SELECT
    event_id,
    developer_id,
    team,
    timestamp,
    CAST(timestamp AS DATE) AS activity_date,
    event_type,
    source,
    duration_minutes,
    task_id
FROM events;


-- VIEW 2: Team-level activity summary
CREATE OR REPLACE VIEW vw_team_activity AS
SELECT
    team,
    COUNT(*) AS total_events,

    COUNT(DISTINCT developer_id)
        AS active_developers,

    COUNT(*) FILTER (
        WHERE event_type = 'IDE_ACTIVE'
    ) AS ide_active_events,

    COUNT(*) FILTER (
        WHERE event_type = 'GITHUB_COMMIT'
    ) AS github_commit_events,

    COUNT(*) FILTER (
        WHERE event_type = 'SLACK_NOTIFICATION'
    ) AS slack_notification_events,

    COUNT(*) FILTER (
        WHERE event_type = 'TASK_SWITCH'
    ) AS task_switch_events,

    COUNT(*) FILTER (
        WHERE event_type = 'MEETING'
    ) AS meeting_events

FROM events
GROUP BY team;


-- VIEW 3: Session-level data-quality analysis
CREATE OR REPLACE VIEW vw_session_quality AS
SELECT
    developer_id,
    team,
    session_number,
    session_start,
    session_end,
    recorded_ide_minutes,
    elapsed_minutes,
    ide_event_count,

    elapsed_minutes - recorded_ide_minutes
        AS elapsed_minus_recorded_minutes,

    CASE
        WHEN session_start IS NULL
          OR session_end IS NULL
            THEN 'MISSING_TIMESTAMP'

        WHEN session_end < session_start
            THEN 'INVALID_TIME_ORDER'

        WHEN elapsed_minutes = 0
         AND ide_event_count = 1
            THEN 'ZERO_DURATION_SINGLE_EVENT'

        WHEN elapsed_minutes = 0
            THEN 'ZERO_DURATION_REVIEW'

        WHEN elapsed_minutes > 480
            THEN 'LONG_SESSION_REVIEW'

        ELSE 'OK'
    END AS session_quality_flag

FROM ide_sessions;