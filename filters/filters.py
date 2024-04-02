from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDay(BaseFilter):
    def __init__(self, day: tuple[str]) -> None:
        self.day = day

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in self.day


class ShiftAction(BaseFilter):
    def __init__(self, shift_actions: tuple[str]) -> None:
        self.shift_actions = shift_actions

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data in self.shift_actions
