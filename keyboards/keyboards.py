from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

DAYS_OF_WEEK = ('Mon' ,'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

def kb_on_start() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    btn = KeyboardButton(text="Show shifts")
    builder.add(btn)
    return builder.as_markup(resize_keyboard=True,input_field_placeholder="Just press button")

def kb_choose_week() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    btns = [KeyboardButton(text="<"), KeyboardButton(text="This one"),KeyboardButton(text=">")]
    btn_back = [KeyboardButton(text="come back")]
    builder.row(*btns)
    builder.row(*btn_back)
    return builder.as_markup(resize_keyboard=True,input_field_placeholder="Just press button")

def kb_choose_day() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    r_1_btns = [KeyboardButton(text="Mon"),
                KeyboardButton(text="Tue"),
                KeyboardButton(text="Wed"),
                KeyboardButton(text="Thu")]
    r_2_btns = [KeyboardButton(text="Fri"),
                KeyboardButton(text="Sat"),
                KeyboardButton(text="Sun")]
    btn_back = [KeyboardButton(text="Back")]
    builder.row(*r_1_btns)
    builder.row(*r_2_btns)
    builder.row(*btn_back)
    return builder.as_markup(resize_keyboard=True,input_field_placeholder="Just press button")

def kb_choose_dayshift() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    btns = [KeyboardButton(text="1 shift"), KeyboardButton(text="2 shift")]
    btn_back = [KeyboardButton(text="Back")]
    builder.row(*btns)
    builder.row(*btn_back)
    return builder.as_markup(resize_keyboard=True,input_field_placeholder="Just press button")

def kb_test():
    btn = InlineKeyboardButton(text='Update!', callback_data="update_shift")
    builder = InlineKeyboardBuilder()
    builder.add(btn)
    return builder.as_markup()

