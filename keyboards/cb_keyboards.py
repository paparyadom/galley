from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def kb_on_start() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    btn = KeyboardButton(text="Schedule")
    builder.add(btn)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Just press button")


def kb_choose_week(first_week: bool = None, last_week: bool = None, gone_week: bool = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btn_update = InlineKeyboardButton(text='Update!', callback_data="update")
    if first_week and not gone_week:
        btns = [InlineKeyboardButton(text='This one', callback_data='this one'),
                InlineKeyboardButton(text='>', callback_data='>')]
    elif last_week:
        btns = [InlineKeyboardButton(text='<', callback_data='<'),
                InlineKeyboardButton(text='This one', callback_data='this one')]
    elif first_week and gone_week:
        btns = [InlineKeyboardButton(text='>', callback_data='>')]
    elif gone_week:
        btns = [InlineKeyboardButton(text='<', callback_data='<'),
                InlineKeyboardButton(text='>', callback_data='>')]
    else:
        btns = [InlineKeyboardButton(text='<', callback_data='<'),
                InlineKeyboardButton(text='This one', callback_data='this one'),
                InlineKeyboardButton(text='>', callback_data='>')]
    builder.row(btn_update)
    builder.row(*btns)
    return builder.as_markup()


def kb_choose_day() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    r_1_btns = [InlineKeyboardButton(text="Mon", callback_data='monday'),
                InlineKeyboardButton(text="Tue", callback_data='tuesday'),
                InlineKeyboardButton(text="Wed", callback_data='wednesday'),
                InlineKeyboardButton(text="Thu", callback_data='thursday')]
    r_2_btns = [InlineKeyboardButton(text="Fri", callback_data='friday'),
                InlineKeyboardButton(text="Sat", callback_data='saturday'),
                InlineKeyboardButton(text="Sun", callback_data='sunday')]
    back_btn = InlineKeyboardButton(text="Back", callback_data='back')
    builder.row(*r_1_btns)
    builder.row(*r_2_btns)
    builder.row(back_btn)
    return builder.as_markup()


def kb_choose_dayshift() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    btns = [InlineKeyboardButton(text="1 shift", callback_data='1'),
            InlineKeyboardButton(text="2 shift", callback_data='2'),
            InlineKeyboardButton(text="Leave", callback_data='del')]
    back_btn = InlineKeyboardButton(text="Back", callback_data='back')
    builder.row(*btns)
    builder.row(back_btn)
    return builder.as_markup()


def kb_test():
    btn = InlineKeyboardButton(text='Update!', callback_data="update")
    builder = InlineKeyboardBuilder()
    builder.add(btn)
    return builder.as_markup()
