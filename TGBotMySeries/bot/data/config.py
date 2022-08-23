from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SERIES_IP = env.str("SERIES_IP")
NEW_SERIES_IP = env.str("NEW_SERIES_IP")
ADMINS = env.str("ADMIN").split(",")

