import datetime
import random

from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext

import keyboards.cb_keyboards as cbk
import utility as uti
from Logger.logger import Logger
from fsm.shifter import ShiftChoiceState
from storage.storage import Storage, pswd_adm, pswd_usr
from utility import text, utility as uti
from filters.filters import IsDay, ShiftAction

router = Router()


# --------------------------------------------
# commands
# --------------------------------------------
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id in Storage.user_data:
        await message.answer('...', reply_markup=cbk.kb_on_start())
    else:
        await message.answer(text.pre_start)


@router.message(Command("reg"))
async def cmd_reg(message: types.Message):
    """
    Check if user is not exists:
        parsing message from user and extracting password and user name ->
        adding user to database by Storage.add_user
    else:
        sending message that current user already in database
    """
    if message.from_user.id not in Storage.user_data:
        Logger.warning(f'{message.from_user.id} is trying to join')
        try:
            _, password, name = message.text.split(maxsplit=2)
        except ValueError:
            await message.answer(text.incorrect_reg_pattern)
        else:
            if password == pswd_adm:
                Storage.add_new_user(message.from_user.id, message.chat.username or '...', name, uti.UserLevel.admin)
                Logger.info(f'User {message.from_user.id} is successfully registered as admin')
                await message.answer(text.greeting, reply_markup=cbk.kb_on_start())
            elif password == pswd_usr:
                Storage.add_new_user(message.from_user.id, message.chat.username or '...', name, uti.UserLevel.user)
                Logger.info(f'User {message.from_user.id} is successfully registered as user')
                await message.answer(text.greeting, reply_markup=cbk.kb_on_start())
            else:
                await message.answer(text.wrong_password)
                Logger.info(f'{message.from_user.id} entered wrong password')
    else:
        await message.answer(text.already_registered)
        Logger.info(f'{message.from_user.id} is trying to registered one more time')


@router.message(Command("reset"))
async def cmd_reset(message: types.Message, state: FSMContext):
    """
    Drop user state data

    """
    if message.from_user.id in Storage.user_data:
        await message.answer(text.reset_message, reply_markup=cbk.kb_on_start())
        await state.set_state(ShiftChoiceState.pre_choosing)
        await state.set_data({})


@router.message(Command("date"))
async def cmd_shift_by_date(message: types.Message, command: CommandObject):
    """
    Send user shift as str by command /date yyyy-mm-dd
    """
    if message.from_user.id in Storage.user_data:
        if command.args is None:
            await message.answer(text.cmd_date_bad_args, reply_markup=cbk.kb_on_start())
        else:
            reply = Storage.load_shift_data_as_str(command.args)
            if reply is None:
                await message.answer(text.cmd_date_bad_args, reply_markup=cbk.kb_on_start(), parse_mode='HTML')
            else:
                await message.answer(reply, reply_markup=cbk.kb_on_start(), parse_mode='HTML')
    else:
        await message.answer(text.pre_start)


@router.message(Command("help"))
async def cmd_shift_by_date(message: types.Message):
    """
    Send week data as str by command /date yyyy-mm-dd
    """
    if message.from_user.id in Storage.user_data:
        await message.answer(text.help)
    else:
        await message.answer(text.pre_start)


@router.message(F.text.lower() == 'schedule')
async def cb_schedule(message: types.Message, state: FSMContext):
    """
    Sends user current week information
    """
    if message.from_user.id in Storage.user_data:
        current_wshift = Storage.info['current_week_id']
        await message.answer(Storage.load_shift_data_as_str(current_wshift),
                             reply_markup=cbk.kb_choose_week(), parse_mode='HTML')
        await state.set_data({'wshift': current_wshift, 'day': None, 'shift_number': None})
        await state.set_state(ShiftChoiceState.choosing_week)
    else:
        await message.answer('You are not registered', reply_markup=types.ReplyKeyboardRemove())


# --------------------------------------------
# processing state ShiftChoiceState.choosing_week
# --------------------------------------------
@router.callback_query(StateFilter(ShiftChoiceState.choosing_week), F.data == '<')
async def cb_prev_week(callback: types.CallbackQuery, state: FSMContext):
    udata = await state.get_data()
    is_first_week = udata['wshift'] <= 2
    udata['wshift'] = 1 if is_first_week else (udata['wshift'] - 1)
    gone_week = udata['wshift'] < Storage.info['current_week_id']
    kb_markup = cbk.kb_choose_week(first_week=is_first_week, gone_week=gone_week)
    await state.update_data(udata)
    await callback.message.edit_text(Storage.load_shift_data_as_str(udata['wshift']), reply_markup=kb_markup,
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_week)


@router.callback_query(StateFilter(ShiftChoiceState.choosing_week), F.data == 'this one')
async def cb_this_week(callback: types.CallbackQuery, state: FSMContext):
    user_shift = await state.get_data()
    await callback.message.edit_text(Storage.load_shift_data_as_str(user_shift['wshift']), reply_markup=cbk.kb_choose_day(),
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_day)


@router.callback_query(StateFilter(ShiftChoiceState.choosing_week), F.data == '>')
async def cb_next_week(callback: types.CallbackQuery, state: FSMContext):
    udata = await state.get_data()
    is_last_week = udata['wshift'] >= (Storage.info['last_week_id'] - 1)
    udata['wshift'] = Storage.info['last_week_id'] if is_last_week else (udata['wshift'] + 1)
    gone_week = udata['wshift'] < Storage.info['current_week_id']
    kb_markup = cbk.kb_choose_week(last_week=is_last_week, gone_week=gone_week)
    await state.update_data(udata)
    await callback.message.edit_text(Storage.load_shift_data_as_str(udata['wshift']), reply_markup=kb_markup,
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_week)


# --------------------------------------------
# processing state ShiftChoiceState.choosing_day
# --------------------------------------------
@router.callback_query(StateFilter(ShiftChoiceState.choosing_day), IsDay(uti.DAYS_OF_WEEK))
async def cb_day_choice(callback: types.CallbackQuery, state: FSMContext):
    udata = await state.get_data()
    udata['day'] = callback.data
    await state.update_data(udata)
    await callback.message.edit_text(Storage.load_shift_data_as_str(udata['wshift']),
                                     reply_markup=cbk.kb_choose_dayshift(),
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_shift)


@router.callback_query(StateFilter(ShiftChoiceState.choosing_day), F.data == 'back')
async def cb_day_choice_back(callback: types.CallbackQuery, state: FSMContext):
    udata = await state.get_data()
    await callback.message.edit_text(Storage.load_shift_data_as_str(udata['wshift']),
                                     reply_markup=cbk.kb_choose_week(),
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_week)


# --------------------------------------------
# processing state ShiftChoiceState.choosing_shift
# --------------------------------------------
@router.callback_query(StateFilter(ShiftChoiceState.choosing_shift), ShiftAction(uti.SHIFT_ACTIONS))
async def cb_choice_dayshift(callback: types.CallbackQuery, state: FSMContext):
    udata = await state.get_data()
    is_first_week = udata['wshift'] < 2
    is_last_week = udata['wshift'] > (Storage.info['last_week_id'] - 1)
    print(is_last_week, udata['wshift'])
    if callback.data == 'del':
        Storage.delete_user_from_shift(week_id=int(udata['wshift']), day=udata['day'], tg_id=callback.from_user.id)
        Logger.info(f'Deleted {callback.from_user.id} '
                    f'{Storage.user_data[callback.from_user.id]} '
                    f'from week_id={udata['wshift']} '
                    f'day={udata['day']} '
                    f'in shift={udata['shift_number']}')
    else:
        if callback.data == '1':
            udata['shift_number'] = 1
        else:
            udata['shift_number'] = 2
        await state.update_data(udata)
        Storage.add_user_to_shift(week_id=int(udata['wshift']), day=udata['day'], tg_id=callback.from_user.id,
                                  shift_number=int(udata['shift_number']))
        Logger.info(f'Added {callback.from_user.id} '
                    f'{Storage.user_data[callback.from_user.id]} '
                    f'to week_id={udata['wshift']} '
                    f'day={udata['day']} '
                    f'in shift={udata['shift_number']}')
    await callback.message.edit_text(Storage.load_shift_data_as_str(udata['wshift']) + uti.shift_update_msg(),
                                     reply_markup=cbk.kb_choose_week(first_week=is_first_week, last_week=is_last_week),
                                     parse_mode='HTML')
    await callback.message.answer('Done', reply_markup=cbk.kb_on_start())
    await state.set_state(ShiftChoiceState.choosing_week)


@router.callback_query(StateFilter(ShiftChoiceState.choosing_shift), F.data == 'back')
async def cb_choice_dayshift_back(callback: types.CallbackQuery, state: FSMContext):
    user_shift = await state.get_data()
    await callback.message.edit_text(Storage.load_shift_data_as_str(user_shift['wshift']), reply_markup=cbk.kb_choose_day(),
                                     parse_mode='HTML')
    await state.set_state(ShiftChoiceState.choosing_day)


# --------------------------------------------
# processing 'update' call back
# --------------------------------------------
@router.callback_query(F.data == 'update')
async def cmd_update(callback: types.CallbackQuery):
    week_id = uti.get_week_number_from_message(callback.message.text[:12])
    if week_id < Storage.get_week_id_by_date(datetime.datetime.now().date()):
        await callback.message.answer('No point in updating completed week')
    else:
        await callback.message.edit_text(
            Storage.load_shift_data_as_str(week_id) + uti.shift_update_msg(),
            reply_markup=cbk.kb_choose_week(), parse_mode='HTML')


# --------------------------------------------
# other
# --------------------------------------------
@router.message(Command('nw'))
async def test(message: types.Message):
    Storage.add_new_week()
    await message.answer(f'Current amount of weeks {str(Storage.info['last_week_id'])}')


@router.message()
async def echo_text(message: types.Message):
    await message.reply(
        random.choice(text.other_inputs))


@router.callback_query()
async def cb_expired(callback: types.CallbackQuery):
    await callback.message.edit_text('This message is expired')
    await callback.message.answer('...', reply_markup=cbk.kb_on_start())
