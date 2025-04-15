from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import random
from Bad import app
from Config import MONGO_URL

# Word list (5-letter words)
WORDS = [
    "apple", "grape", "peach", "mango", "lemon", "berry", "melon", "olive", "guava", "plums",
    "crown", "flips", "south", "house", "mouse", "night", "query", "eight", "blame", "bring", "charm",
    "draft", "entry", "field", "glove", "hover", "input", "joker", "knife", "liver", "mirth", "nerds",
    "orbit", "piano", "quiet", "reach", "slide", "table", "uncle", "vapor", "weird", "xenon", "yield",
    "zebra", "adobe", "bison", "canal", "daisy", "eagle", "fancy", "giant", "hinge", "icily", "jolly",
    "karma", "latch", "motel", "noisy", "ocean", "pound", "quilt", "radar", "shelf", "thorn", "under",
    "vivid", "whale", "yacht", "zesty", "adapt", "banjo", "cabin", "dodge", "embed", "ferry", "gloom",
    "hippo", "index", "jumpy", "kayak", "lunar", "manor", "naval", "oxide", "polar", "quack", "robot",
    "siren", "trick", "utter", "vigor", "woven", "yummy", "zoned", "amber", "broom", "couch", "drown",
    "exile", "fraud", "gleam", "hatch", "inlet", "joint", "kneel", "label", "macro", "needy", "optic",
    "prime", "quart", "reign", "sweep", "tango", "urged", "visit", "wager", "xerox", "young", "zippy",
    "angel", "beach", "civic", "dizzy", "elite", "flesh", "gorge", "haste", "ideal", "jewel", "knock",
    "loyal", "major", "noble", "organ", "pride", "quell", "rival", "sheep", "thump", "upset", "vocal",
    "witty", "xylem", "yeast", "zebra", "actor", "brisk", "chant", "devil", "evoke", "flame", "grasp",
    "haste", "issue", "judge", "knees", "lucky", "might", "ninth", "occur", "plant", "quote", "rigid",
    "scale", "tried", "usual", "vague", "wrath", "xenon", "youth", "zonal", "agent", "blade", "coral",
    "drake", "enjoy", "fable", "grain", "haste", "imply", "joker", "kiosk", "lodge", "match", "nurse",
    "oxide", "piano", "quirk", "roast", "swirl", "toxic", "urban", "vault", "waltz", "xenon", "yeast",
    "zebra", "alert", "boast", "crush", "delta", "eager", "fleet", "gauge", "honey", "inbox", "jazzy",
    "kneel", "lunch", "model", "nicer", "occur", "plead", "quota", "risky", "squad", "truce", "unite",
    "vivid", "wreak", "xerox", "yield", "zesty", "abbey", "bride", "craft", "deter", "extra", "final",
    "gland", "hoist", "inlet", "jumps", "kinda", "latch", "miner", "niche", "optic", "prone", "queen",
    "rapid", "shard", "trace", "ultra", "vigil", "wrist", "xeric", "youth", "zebra", "arena", "brave",
    "creek", "dwell", "epoxy", "flick", "grief", "hinge", "inbox", "jiffy", "knead", "latch", "mirth",
    "noble", "orbit", "pluck", "quack", "rinse", "spend", "treat", "unzip", "vowel", "wharf", "xenon",
    "youth", "zippy", "abide", "basil", "chain", "drown", "edict", "faint", "golem", "haste", "ivory",
    "jelly", "karma", "lemon", "medal", "night", "ozone", "poker", "quest", "rider", "straw", "trend",
    "urine", "vixen", "wound", "xerox", "yeast", "zonal"
]

# MongoDB setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["wordseek_bot"]
games_col = db["games"]
scores_col = db["scores"]

def get_hint(secret, guess):
    result = ""
    for i in range(5):
        if guess[i] == secret[i]:
            result += "🟩"
        elif guess[i] in secret:
            result += "🟨"
        else:
            result += "🟥"
    return result

@app.on_message(filters.command("new"))
async def new_game(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if a game is already active for this user/group
    existing_game = games_col.find_one({"chat_id": chat_id, "user_id": user_id, "active": True})
    if existing_game:
        return await message.reply("You already have an active game! Finish it before starting a new one.")

    # Only admins can start a game in groups
    if message.chat.type in ["group", "supergroup"]:
        member = await client.get_chat_member(chat_id, user_id)
        if member.status not in ("administrator", "creator"):
            return await message.reply("Only admins can start a new game in this group.")

    word = random.choice(WORDS)
    games_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"word": word, "guesses": [], "active": True, "max_points": 30}},
        upsert=True
    )
    await message.reply(
        "Game started! Guess the 5-letter word! Your guess must be a 5-letter word composed of letters only!"
    )

@app.on_message(filters.text & ~filters.command(["new", "leaderboard", "myscore"]))
async def handle_guess(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_input = message.text.strip().lower()

    # Fetch the game for the specific user/group
    game = games_col.find_one({"chat_id": chat_id, "user_id": user_id, "active": True})
    if not game:
        return  # No active game for this user/group

    # Validate if the input is 5 letters and alphabetical
    if len(user_input) != 5 or not user_input.isalpha():
        return  # Skip replying to avoid spam

    # Validate if the word is in the predefined word list
    if user_input not in WORDS:
        return await message.reply(f"`{user_input.upper()}` is not a valid word!")

    correct_word = game["word"]
    guesses = game.get("guesses", [])
    hint = get_hint(correct_word, user_input)

    guesses.append({
        "user_id": user_id,
        "guess": user_input,
        "hint": hint
    })

    if user_input == correct_word:
        points_earned = max(0, game["max_points"] - len(guesses))
        scores_col.update_one(
            {"user_id": user_id, "chat_id": chat_id},
            {
                "$inc": {"score": points_earned},
                "$setOnInsert": {
                    "username": message.from_user.username or "",
                    "name": message.from_user.first_name
                }
            },
            upsert=True
        )
        games_col.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"active": False}})
        board = "\n".join([f"{g['hint']} `{g['guess'].upper()}`" for g in guesses])
        return await message.reply(
            f"{board}\n\n**{message.from_user.first_name}** guessed it correctly! The word was **{correct_word.upper()}**.\n"
            f"Added {points_earned} to the leaderboard.\nStart a new game with /new."
        )

    if len(guesses) >= 30:
        games_col.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"active": False}})
        board = "\n".join([f"{g['hint']} `{g['guess'].upper()}`" for g in guesses])
        return await message.reply(f"{board}\n\nGame over! The correct word was **{correct_word.upper()}**.")

    games_col.update_one({"chat_id": chat_id, "user_id": user_id}, {"$set": {"guesses": guesses}})
    board = "\n".join([f"{g['hint']} `{g['guess'].upper()}`" for g in guesses])
    await message.reply(board)

@app.on_message(filters.command("leaderboard"))
async def leaderboard(client, message: Message):
    chat_id = message.chat.id
    top = list(scores_col.find({"chat_id": chat_id}).sort("score", -1).limit(10))
    if not top:
        return await message.reply("No scores yet!")

    text = "**🏆 Leaderboard:**\n"
    for i, user in enumerate(top, 1):
        name = user.get("name") or "Unknown"
        score = user.get("score", 0)
        text += f"{i}. {name} — {score} point(s)\n"

    await message.reply(text)

@app.on_message(filters.command("myscore"))
async def myscore(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    entry = scores_col.find_one({"user_id": user_id, "chat_id": chat_id})

    score = entry.get("score", 0) if entry else 0
    await message.reply(f"**Your score:** {score} point(s).")
