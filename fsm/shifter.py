from aiogram.fsm.state import StatesGroup, State


class ShiftChoiceState(StatesGroup):
    pre_choosing = State()
    choosing_week = State()
    choosing_day = State()
    choosing_shift = State()
