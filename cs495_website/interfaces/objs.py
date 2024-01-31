from redis import Redis

from etb_db.DB import Db
from etb_env.ENV import Env


env_interface = Env('/.env')


DB_PARAMS = env_interface.get_db_auth()
db_interface = Db(RDBMS='postgres', AUTH = DB_PARAMS)


REDIS_PARAMS = env_interface.get(["RHOST", "RPORT"])
red = Redis(host=REDIS_PARAMS["RHOST"], port=int(REDIS_PARAMS["RPORT"]))
