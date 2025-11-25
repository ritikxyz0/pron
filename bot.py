import asyncio
from aiogram import Bot, Dispatcher, types

# ===========================
# CONFIG
# ===========================
BOT_TOKEN = "8385007008:AAHqAVgSsoFfQggGVs_rzLjlrJS6EKzOsfI"  # <-- Yaha token daalna

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# ===========================
# COMMAND HANDLERS
# ===========================
@dp.message(commands={"start"})
async def start_cmd(message: types.Message):
    await message.answer(
        "👋 Bot chal raha hai!\n\n"
        "Commands:\n"
        "/start - Bot check\n"
        "/help - Help menu\n"
        "/search <text> - YouTube search link"
    )


@dp.message(commands={"help"})
async def help_cmd(message: types.Message):
    await message.answer(
        "📌 HELP MENU\n\n"
        "/start - Bot check\n"
        "/search <keywords> - YouTube par search karega\n"
    )


@dp.message(commands={"search"})
async def search_cmd(message: types.Message):
    query = message.get_args()

    if not query:
        await message.answer("Use: /search <keywords>")
        return

    # Basic safe keywords block
    blocked = ["porn", "sex", "xxx", "nude", "adult", "nsfw"]
    if any(b in query.lower() for b in blocked):
        await message.answer("❌ Ye search allowed nahi hai.")
        return

    import urllib.parse
    q = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={q}"

    await message.answer(f"🔎 Your search link:\n{url}")


# ===========================
# DEFAULT HANDLER
# ===========================
@dp.message()
async def all_msg(message: types.Message):
    await message.answer("❗ Command samajh nahi aaya. Use /help")


# ===========================
# MAIN LOOP
# ===========================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
