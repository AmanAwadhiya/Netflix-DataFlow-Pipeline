WITH raw_netflix AS (
    SELECT
        show_id,
        type,
        title,
        director,
        cast,
        country,
        DATE(date_added) AS date_added,
        release_year,
        rating,
        duration
    FROM {{ source('netflix_dataset', 'raw_netflix') }}
)
SELECT * FROM raw_netflix
WHERE date_added IS NOT NULL;
