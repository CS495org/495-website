select id, overview, name,
poster_path, backdrop_path, genre_ids, coalesce(first_air_date, '1970-01-01') as first_air_date, vote_count, vote_average
from "Shows_Trending_This_Week"
where first_air_date != '';