WITH country_data AS (
    SELECT
        country,
        COUNT(show_id) AS total_titles
    FROM {{ ref('stg_netflix_data') }}
    GROUP BY country
)
SELECT * FROM country_data;
