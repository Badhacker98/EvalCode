from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Get this value from my.telegram.org/apps
APP_ID = 25742938
# Get this value from my.telegram.org/apps
HASH_ID = "b35b715fe8dc0a58e8048988286fc5b6"
# Get your token from @BotFather on Telegram.
TOKEN = "7661882864:AAFKoGzqePt8aGTz_z1p9U_W9__ncPzx5BQ"
DB_NAME = "evalDB"
#databse
MONGO_URL = "mongodb+srv://knight_rider:GODGURU12345@knight.jm59gu9.mongodb.net/?retryWrites=true&w=majority"
LOGGER_ID = "-1002056907061"
OWNER_ID = "7009601543"
SUDOERS = "7009601543"
STRING1 = ""
STRING2 = ""

#DATABSE
mongo = MongoClient(MONGO_URL)
db = mongo["faster_finger"]
scores_col = db["scores"]
