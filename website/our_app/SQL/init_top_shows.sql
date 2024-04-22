with show_cte as (
    SELECT
        t1.id, t1.overview, t1.name,
        t1.poster_path, t1.backdrop_path, coalesce(t1.first_air_date, '1970-01-01') as first_air_date,
        jsonb_agg(t2.genre_name) AS genre_names
    FROM
        "Top_Rated_Shows" t1
    CROSS JOIN LATERAL
        jsonb_array_elements_text(t1.genre_ids) AS genre_id
    JOIN
        genre_map t2 ON t2.id = genre_id::int
    GROUP BY
        t1.id, t1.overview, t1.name, t1.poster_path, t1.backdrop_path, t1.first_air_date )
select * from show_cte where first_air_date != '' and genre_names is not null;