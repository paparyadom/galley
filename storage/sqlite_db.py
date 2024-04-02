import datetime
import pickle
import sqlite3
from collections import defaultdict
from typing import Tuple
from storage import db_queries

from utility.utility import DayShift, sqlite_adapt_date_iso, get_user_day_shift


class SqliteDB:
    def __init__(self, db_name: str):
        self._db_name = db_name
        self.info = defaultdict()
        self.user_data = defaultdict()
        self.__init_tables()  # initializing tables
        self.__load_users()   # loading users in database for getting best way to get user data
        self.__load_info()    # loading amount of stored weeks and current week id

        sqlite3.register_adapter(datetime.date, sqlite_adapt_date_iso)  # need for right datetime format

    def add_new_user(self, tg_id: int, tg_name: str, name: str, lvl: int):
        if tg_id not in self.user_data:
            with sqlite3.connect(self._db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(db_queries.ADD_USER, (tg_id, tg_name, name, lvl))
                self.user_data[tg_id] = {'tg_name': tg_name, 'name': name, 'lvl': lvl}

    def add_new_week(self, delta: int = 0, by_delta: bool = False):
        """
        Add to database new week as <week id> <week start> <week end> <DayShift instance>

        Use <by_delta> to add week by delta value. delta = one week * 7.
        If <by_delta> == True  - new week is depended on current date. So in this case new
        week start date will be as current date + delta and week end date as week start date + 6 days
        Note: This case is used only in function <SqliteDB.__fill_tables()> while bot starting.

        By default, new week is added as last week in database + one week
        e.g. if last stored week started in 2024-03-01 so the next week will be 2024-03-08

        """
        day_shift = DayShift()
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            if by_delta:
                today = datetime.date.today()
                start = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=7 * delta)
                end = start + datetime.timedelta(days=6)
            else:
                cursor.execute(db_queries.LOAD_LAST_WEEK_STARTDATE)
                last_date = cursor.fetchone()
                last_date = datetime.datetime.strptime(last_date[0], '%Y-%m-%d')
                start = last_date.date() + datetime.timedelta(days=7)
                end = start + datetime.timedelta(days=6)

            cursor.execute(db_queries.ADD_WEEKSHIFT, (start,
                                                      end,
                                                      pickle.dumps(day_shift)))
        self.__load_info()  # updating self.info

    def add_user_to_shift(self, week_id: int, tg_id: int, day: str, shift_number: int):
        shift: DayShift = self.__load_shift_data(week_id)[3]
        user = f'{self.user_data[tg_id]['name']} (@{self.user_data[tg_id]['tg_name']})'
        day_data = getattr(shift, day)
        current_user_shift = get_user_day_shift(day_data, user)
        if current_user_shift == shift_number:
            pass
        else:
            if current_user_shift == 0:
                day_data[shift_number].add(user)
            elif current_user_shift != shift_number:
                day_data[current_user_shift].remove(user)
                day_data[shift_number].add(user)
            with sqlite3.connect(self._db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(db_queries.UPDATE_SHIFT, (pickle.dumps(shift), week_id))

    def delete_user_from_shift(self, week_id: int, tg_id: int, day: str):
        shift_data = self.__load_shift_data(week_id)
        if shift_data is not None:
            shift: DayShift = shift_data[3]
            user = f'{self.user_data[tg_id]['name']} (@{self.user_data[tg_id]['tg_name']})'
            day_data = getattr(shift, day)
            current_user_shift = get_user_day_shift(day_data, user)
            if current_user_shift == 0:
                pass
            else:
                day_data[current_user_shift].remove(user)
                with sqlite3.connect(self._db_name) as connection:
                    cursor = connection.cursor()
                    cursor.execute(db_queries.UPDATE_SHIFT, (pickle.dumps(shift), week_id))

    def load_shift_data_as_str(self, week_id_or_date: int | datetime.date | str) -> str:
        """
        Representing week data about shifts and workers as text

        """
        shift_data = self.__load_shift_data(week_id_or_date)
        if shift_data is None:
            message = None
        else:
            week_id, start, end, days_shift = shift_data
            message = f'Week #{week_id}\nPeriod {start} - {end}\n{days_shift.__str__()}'
        return message

    def get_week_id_by_date(self, date_in_week: datetime.date | str) -> int:
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(db_queries.LOAD_WEEK_ID_BY_DATE, (date_in_week, date_in_week))
            fetched = cursor.fetchall()
            if len(fetched) != 0:
                week_id = fetched[0][0]
            return week_id

    def update_info(self):
        self.__load_info()

    def __init_tables(self):
        '''
        Creating database if not exists
        Creating tables Users, Workshifts
        Filling table Workshifts by self.__fill_tables

        '''
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(db_queries.CREATE_USER_TABLE)
            cursor.execute(db_queries.CREATE_WORKSHIFTS_TABLE)
            self.__fill_tables()

    def __fill_tables(self):
        """
        Is used to fill table Workshifts when bot starts

        Firstly check if there is current week in database
        if it is there calculate missing ongoing week (should be 4) and add if is needed

        in case of not existing any

        """
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(db_queries.LOAD_WEEK_ID_BY_DATE,
                           (datetime.datetime.now().date(), datetime.datetime.now().date()))
            week_id = cursor.fetchall()
            if len(week_id) != 0:
                cursor.execute(db_queries.LOAD_WSHIFT_ID_COUNT)
                week_count = cursor.fetchall()
                if (missing_weeks := week_count[0][0] - week_id[0][0]) < 4:
                    for i in range(4 - missing_weeks):
                        self.add_new_week(delta=i, by_delta=True)
            else:
                for i in range(4):
                    self.add_new_week(delta=i, by_delta=True)

    def __load_users(self):
        """
        Loading user info {'tg_name', 'name', 'lvl'(useless for now)}
        """
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(db_queries.LOAD_USERS_FROM_DB)
            udata = cursor.fetchall()
            for data_tuple in udata:
                self.user_data[data_tuple[0]] = {'tg_name': data_tuple[1], 'name': data_tuple[2], 'lvl': data_tuple[3]}

    def __load_info(self):
        """
        Loading id of last week stored in database and id of current week
        to avoid unnecessary request to database

        """
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(db_queries.LOAD_WSHIFT_ID_COUNT)
            data = cursor.fetchall()
            self.info['last_week_id'] = data[0][0]
            cursor.execute(db_queries.LOAD_WEEK_ID_BY_DATE,
                           (datetime.datetime.now().date(), datetime.datetime.now().date()))
            data = cursor.fetchall()
            self.info['current_week_id'] = data[0][0]

    def __load_shift_data(self, week_id_or_date: int | datetime.date | str) -> Tuple[int, str, str, DayShift] | None:
        """
        Getting full row from Worshifts by week id or custom date
        """
        with sqlite3.connect(self._db_name) as connection:
            cursor = connection.cursor()
            if isinstance(week_id_or_date, int):
                cursor.execute(db_queries.LOAD_SHIFT_BY_ID, (week_id_or_date,))
            elif isinstance(week_id_or_date, (datetime.date, str)):
                cursor.execute(db_queries.LOAD_SHIFT_BY_DATE, (week_id_or_date, week_id_or_date))
            fetched = cursor.fetchall()
            if len(fetched) != 0:
                week_id, start, end, days_shift = fetched[0]
                return week_id, start, end, pickle.loads(days_shift)
            else:
                return None
