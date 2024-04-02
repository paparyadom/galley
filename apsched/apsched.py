import datetime
from typing import Any

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from storage.storage import SqliteDB
from utility.text import new_week_added


async def add_new_week(storage: SqliteDB | Any, bot: Bot, admin: int):
    storage.add_new_week()
    storage.update_info()
    await bot.send_message(chat_id=admin, text=new_week_added)


async def update_current_week_id(storage: SqliteDB | Any):
    storage.update_info()


def init_scheduler(storage: SqliteDB | Any, bot: Bot, admin: int, Scheduler: AsyncIOScheduler):
    Scheduler.add_job(func=add_new_week,
                      trigger='cron',
                      day_of_week='fri',
                      hour=8,
                      minute=0,
                      args=(storage, bot, admin))
    Scheduler.add_job(func=update_current_week_id,
                      trigger='cron',
                      day_of_week='mon',
                      hour=0,
                      minute=1,
                      args=(storage,))
