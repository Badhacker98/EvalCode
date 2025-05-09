from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import StringSession
from telegram.ext import Application
import Config

# Pyrogram Bot Client (With Bot Token)
app = Client(
    name="app", 
    api_id=Config.APP_ID, 
    api_hash=Config.HASH_ID, 
    bot_token=Config.TOKEN,
    plugins=dict(root="Bad.Modules")
)

# Pyrogram User Client (Without Bot Token)
Shizu = Client(
    name="Shizu", 
    api_id=Config.APP_ID, 
    api_hash=Config.HASH_ID, 
    session_string=Config.STRING1,
    plugins=dict(root="Bad.Modules")
)

# Telethon Bot Client (With Bot Token)
Bad = TelegramClient(
             session="Bad",  # Add a session name here
             api_id=Config.APP_ID, 
             api_hash=Config.HASH_ID
             ).start(bot_token=Config.TOKEN)


# Telethon User Client (Without Bot Token)
Sukh = TelegramClient(
    session=StringSession(Config.STRING2),
    api_id=Config.APP_ID, 
    api_hash=Config.HASH_ID
)

plugins = dict(root="Bad.Modules")


# Telegram (python-telegram-bot) Client
application = Application.builder().token(Config.TOKEN).build()

plugins = dict(root="Bad.Modules")
