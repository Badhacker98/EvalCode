from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Get this value from my.telegram.org/apps
APP_ID = 25742938
# Get this value from my.telegram.org/apps
HASH_ID = "b35b715fe8dc0a58e8048988286fc5b6"
# Get your token from @BotFather on Telegram.
TOKEN = "7073124607:AAFXcqEcH_7iQJ5hxfUdUxIDe3gwAp1GvXY"
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
