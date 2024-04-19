select name, poster_path
from "Top_Rated_Shows" trs
where vote_count > 500
order by popularity desc
limit 20;