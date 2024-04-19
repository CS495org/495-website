from redis import Redis

from etb_env import ENV
from etb_pg import PGDB


env = ENV()

DB_PARAMS = ["USER", "PASSWORD", "HOST", "PORT", "DATABASE"]
DB_VALS: dict = env.get(DB_PARAMS)

DB_CONF = {
    "user" : DB_VALS.get("USER"),
    "password" : DB_VALS.get("PASSWORD"),
    "host" : DB_VALS.get("HOST"),
    "port" : DB_VALS.get("PORT"),
    "dbname" : DB_VALS.get("DATABASE"),
}

pg_interface = PGDB(DB_CONF, sql_dir='/app/our_app/SQL')


REDIS_PARAMS = ["RHOST", "RPORT"]
REDIS_CONF: dict = env.get(REDIS_PARAMS)

red = Redis(host=REDIS_CONF["RHOST"], port=int(REDIS_CONF["RPORT"]))
