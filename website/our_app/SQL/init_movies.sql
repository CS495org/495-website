with movie_cte as (
    SELECT
        t1.id, t1.overview, t1.title,
        t1.poster_path, t1.backdrop_path, coalesce(t1.release_date, '1970-01-01') as release_date,
        jsonb_agg(t2.genre_name) AS genre_names
    FROM
        "Top_Rated_Movies" t1
    CROSS JOIN LATERAL
        jsonb_array_elements_text(t1.genre_ids) AS genre_id
    JOIN
        genre_map t2 ON t2.id = genre_id::int
    GROUP BY
        t1.id, t1.overview, t1.title, t1.poster_path, t1.backdrop_path, t1.release_date )
select * from movie_cte where release_date != '' and genre_names is not null;