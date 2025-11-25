# bot.py
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import urllib.parse
import os

# CONFIG
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8385007008:AAHqAVgSsoFfQggGVs_rzLjlrJS6EKzOsfI"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Commands list that we refuse
REFUSE_COMMANDS = {"/porn", "/pron", "/adult", "/nsfw", "/xxx"}

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    text = (
        "Hi! Main ek safe media bot hoon.\n\n"
        "Use /search <keywords> to find videos (YouTube search link).\n"
        "Note: Main explicit/adult content share nahi karunga.\n\n"
        "Examples:\n"
        "/search funny cats\n"
        "/search programming tutorial\n"
    )
    await message.reply(text)

@dp.message_handler(commands=["search"])
async def handle_search(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("Use: /search <keywords>\nExample: /search motivational speech")
        return

    # Basic safety: block obviously explicit queries (simple keyword check)
    blocked_keywords = ["porn", "xxx", "nude", "sexual", "sex", "adult", "nsfw", "erotic"]
    lower_args = args.lower()
    if any(k in lower_args for k in blocked_keywords):
        await message.reply("Sorry — main explicit content search mein madad nahi kar sakta. Koi aur search batao.")
        return

    query = urllib.parse.quote_plus(args)
    yt_search_url = f"https://www.youtube.com/results?search_query={query}"
    resp = f"Yeh raha search link (YouTube):\n{yt_search_url}\n\nNote: Agar tum chaho to main future me resmi API se results fetch karke thumbnails aur titles bhej dunga."
    await message.reply(resp)

# Catch specific refuse commands and reply politely
@dp.message_handler()
async def catch_all(message: types.Message):
    text = message.text or ""
    cmd = text.strip().split()[0].lower()
    if cmd in REFUSE_COMMANDS or any(k in text.lower() for k in ["porn", "pron", "xxx", "nude", "sex"]):
        await message.reply(
            "Main explicit/adult content share karne mein madad nahi kar sakta. "
            "Agar tum chaho to main non-explicit videos, memes, ya tutorials dhoondhne mein madad kar sakta hoon.\n"
            "Use /search <keywords> for safe searches."
        )
        return

    # Default help
    await message.reply("Command samajh nahi aaya. Use /help for instructions.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
