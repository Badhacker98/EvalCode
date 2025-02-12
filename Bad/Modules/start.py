from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Bad import app

@app.on_message(filters.command("start") & ~filters.forwarded & ~filters.via_bot)
async def start_command(client, message):
    # Start command message delete karne ke liye
    await message.delete()

    text = """🐋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ᴇᴠᴀʟ ʙᴏᴛ! ✨

📊 ꜰᴏʀ ᴇᴠᴀʟᴜᴀᴛɪᴏɴ ᴀɴᴅ ɪɴꜰᴏ, ꜱɪᴍᴘʟʏ ᴛʏᴘᴇ ʙᴏᴛ ᴀᴄᴛɪᴠɪᴛʏ ʙᴇʟᴏᴡ!

🌟 ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛᴏ ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ʀᴇᴀᴄᴛ ᴡɪᴛʜ ᴡɪᴛᴛʏ ꜰᴇᴇᴅʙᴀᴄᴋ!"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 ᴏᴡɴᴇʀ", url="https://t.me/II_BAD_BABY_II")],
    ],
    [
        [InlineKeyboardButton("🔔 sᴜᴘᴘᴏʀᴛ", url="https://t.me/PBX_CHAT")],
        [InlineKeyboardButton("🛠 ᴜᴘᴅᴀᴛᴇ", url="https://t.me/HEROKUBIN_01")]
    ])

    await message.reply_text(text, reply_markup=keyboard)
