from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from aiogram.types import ErrorEvent
from Logger.logger import Logger
router = Router()


@router.errors()
async def error_handler(event: ErrorEvent):
    """
    Catch all exceptions. Not handling
    """
    if isinstance(event.exception, TelegramBadRequest):
        Logger.error(f'event.update {event.update}')
    else:
        Logger.error(f'event.exception {event.exception}')
        Logger.error(f'event.update {event.update}')



