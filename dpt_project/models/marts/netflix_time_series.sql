WITH time_series AS (
    SELECT
        DATE_TRUNC(date_added, MONTH) AS month,
        COUNT(show_id) AS total_titles
    FROM {{ ref('stg_netflix_data') }}
    GROUP BY month
    ORDER BY month
)
SELECT * FROM time_series;
