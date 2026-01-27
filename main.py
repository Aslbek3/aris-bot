import asyncio
import logging
from aiogram import Bot, Dispatcher
from core.config import settings
from bot.handlers import common, finance, motivator
from bot.middlewares.activity import ActivityMiddleware
from database.requests import init_db

# Setup logging
logging.basicConfig(level=logging.INFO)

async def main():
    # Initialize database
    await init_db()
    
    # Initialize bot and dispatcher
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # Register middlewares
    dp.message.middleware(ActivityMiddleware())
    
    # Register routers
    dp.include_router(common.router)
    dp.include_router(finance.router)
    dp.include_router(motivator.router)
    
    # Start polling
    logging.info("ARIS Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
