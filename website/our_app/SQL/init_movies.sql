select id, overview, title,
poster_path, backdrop_path, genre_ids, coalesce(release_date, '1970-01-01') as release_date
from "Movies_Trending_This_Week"
where release_date != '';