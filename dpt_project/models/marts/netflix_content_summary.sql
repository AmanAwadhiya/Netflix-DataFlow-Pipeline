WITH content_summary AS (
    SELECT
        type,
        release_year,
        COUNT(*) AS total_count
    FROM {{ ref('stg_netflix_data') }}
    GROUP BY type, release_year
)
SELECT * FROM content_summary;
