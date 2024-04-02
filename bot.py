import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from Routers.cb_router import router as shift_router
from Routers.exceptions_handler import router as exception_router
import utility.utility as uti
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apsched.apsched import init_scheduler
from storage.storage import Storage


async def main():
    token, session, admin = uti.init_bot_cfg(with_proxy=False)
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=token, session=session)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(exception_router)
    dp.include_router(shift_router)

    Scheduler = AsyncIOScheduler()
    init_scheduler(storage=Storage, bot=bot, Scheduler=Scheduler, admin=admin)
    Scheduler.start()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'[x] Bot was stopped via KeyboardInterrupt')
