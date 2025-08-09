import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from db import DB
from user_handlers import router as user_router

async def main():
    with open("config.json", "r", encoding="utf8") as f:
        cfg = json.load(f)

    bot = Bot(token=cfg["BOT_TOKEN"], parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())

    db = DB(cfg.get("DATABASE", "./bot.db"))
    await db.init()

    # attach shared objects
    bot["DB"] = db
    bot["CONFIG"] = cfg

    dp.include_router(user_router)

    print("Bot started (polling)...")
    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
