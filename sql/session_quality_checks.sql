
-- ============================================================
-- CogniStream: IDE Session Quality Checks
-- Database: DuckDB
-- ============================================================


-- 1. SESSION DURATION DISTRIBUTION

SELECT
    COUNT(*) AS total_sessions,

    COUNT(*) FILTER (
        WHERE elapsed_minutes < 0
    ) AS negative_elapsed_sessions,

    COUNT(*) FILTER (
        WHERE elapsed_minutes = 0
    ) AS zero_elapsed_sessions,

    COUNT(*) FILTER (
        WHERE elapsed_minutes > 240
    ) AS sessions_over_four_hours,

    COUNT(*) FILTER (
        WHERE elapsed_minutes > 480
    ) AS sessions_over_eight_hours,

    ROUND(AVG(elapsed_minutes), 2)
        AS avg_elapsed_minutes,

    ROUND(MEDIAN(elapsed_minutes), 2)
        AS median_elapsed_minutes,

    MAX(elapsed_minutes)
        AS max_elapsed_minutes

FROM ide_sessions;


-- 2. RECORDED TIME VERSUS ELAPSED TIME

SELECT
    ROUND(AVG(recorded_ide_minutes), 2)
        AS avg_recorded_minutes,

    ROUND(AVG(elapsed_minutes), 2)
        AS avg_elapsed_minutes,

    ROUND(
        AVG(elapsed_minutes - recorded_ide_minutes),
        2
    ) AS avg_time_difference,

    ROUND(
        100.0 * COUNT(*) FILTER (
            WHERE recorded_ide_minutes > elapsed_minutes
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS pct_sessions_recorded_time_exceeds_elapsed

FROM ide_sessions
WHERE recorded_ide_minutes IS NOT NULL
  AND elapsed_minutes IS NOT NULL;


-- 3. LONGEST SESSIONS

SELECT
    developer_id,
    team,
    session_number,
    session_start,
    session_end,
    recorded_ide_minutes,
    elapsed_minutes,

    ROUND(
        elapsed_minutes - recorded_ide_minutes,
        2
    ) AS time_difference_minutes,

    ide_event_count

FROM ide_sessions

ORDER BY elapsed_minutes DESC

LIMIT 15;


-- 4. SESSION START AND END CONSISTENCY

SELECT
    COUNT(*) FILTER (
        WHERE session_start IS NULL
    ) AS missing_session_starts,

    COUNT(*) FILTER (
        WHERE session_end IS NULL
    ) AS missing_session_ends,

    COUNT(*) FILTER (
        WHERE session_start > session_end
    ) AS end_before_start,

    COUNT(*) FILTER (
        WHERE ABS(
            DATE_DIFF(
                'second',
                session_start,
                session_end
            ) / 60.0 - elapsed_minutes
        ) > 1
    ) AS elapsed_duration_mismatches

FROM ide_sessions
WHERE session_start IS NOT NULL
  AND session_end IS NOT NULL;


-- 5. DEVELOPER SESSION COUNT RECONCILIATION

SELECT
    d.developer_id,
    d.team,

    d.session_count AS reported_session_count,

    COUNT(s.session_number)
        AS actual_session_count,

    d.session_count - COUNT(s.session_number)
        AS session_count_difference

FROM developer_metrics d

LEFT JOIN ide_sessions s
    ON d.developer_id = s.developer_id

GROUP BY
    d.developer_id,
    d.team,
    d.session_count

ORDER BY
    ABS(d.session_count - COUNT(s.session_number)) DESC,
    d.developer_id;

-- CHECK 6: Classify sessions by data quality

SELECT
    developer_id,
    team,
    session_number,
    session_start,
    session_end,
    recorded_ide_minutes,
    elapsed_minutes,
    ide_event_count,

    CASE
        WHEN session_start IS NULL OR session_end IS NULL
            THEN 'MISSING_TIMESTAMP'

        WHEN session_end < session_start
            THEN 'INVALID_TIME_ORDER'

        WHEN elapsed_minutes = 0 AND ide_event_count = 1
            THEN 'ZERO_DURATION_SINGLE_EVENT'

        WHEN elapsed_minutes = 0
            THEN 'ZERO_DURATION_REVIEW'

        WHEN elapsed_minutes > 480
            THEN 'LONG_SESSION_REVIEW'

        ELSE 'OK'
    END AS session_quality_flag

FROM ide_sessions

ORDER BY
    CASE
        WHEN elapsed_minutes = 0 THEN 1
        WHEN elapsed_minutes > 480 THEN 2
        ELSE 3
    END,
    developer_id,
    session_number;