from redis import Redis

# from etb_db.DB import Db
from etb_env.ENV import Env
from etb_pg import PGDB


env_interface = Env('/.env')

DB_PARAMS = ["USER", "PASSWORD", "HOST", "PORT", "DATABASE"]
DB_VALS: dict = env_interface.get(DB_PARAMS)

DB_CONF = {
    "user" : DB_VALS.get("USER"),
    "password" : DB_VALS.get("PASSWORD"),
    "host" : DB_VALS.get("HOST"),
    "port" : DB_VALS.get("PORT"),
    "dbname" : DB_VALS.get("DATABASE"),
}

pg_interface = PGDB(DB_CONF)


REDIS_PARAMS = ["RHOST", "RPORT"]
REDIS_CONF: dict = env_interface.get(REDIS_PARAMS)

red = Redis(host=REDIS_CONF["RHOST"], port=int(REDIS_CONF["RPORT"]))
