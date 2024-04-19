select name, poster_path
from "Shows_Trending_This_Week" sttw
where vote_count > 500
order by popularity desc
limit 20;