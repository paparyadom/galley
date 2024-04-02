import datetime
import enum
import re
from configparser import ConfigParser
from dataclasses import dataclass, field, fields
from typing import Tuple, Dict, Set

import aiogram.client.session.aiohttp

DAYS_OF_WEEK = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
SHIFT_ACTIONS = ('1', '2', 'del')


@dataclass
class DayShift:
    """
    Stored data in following format:
    day of week : shift number : ([user number] user name (@ telegram name or @ ... if not telegram name not exists))
    ...
    """
    monday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    tuesday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    wednesday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    thursday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    friday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    saturday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)
    sunday: Dict[int: Set[str], int: Set[str]] = field(default_factory=dict)

    def __post_init__(self):
        self.monday = {1: set(), 2: set()}
        self.tuesday = {1: set(), 2: set()}
        self.wednesday = {1: set(), 2: set()}
        self.thursday = {1: set(), 2: set()}
        self.friday = {1: set(), 2: set()}
        self.saturday = {1: set(), 2: set()}
        self.sunday = {1: set(), 2: set()}

    def __str__(self):
        res = ''
        for field in fields(self):
            res += f'\n<b>{field.name.capitalize()}:</b>\n'
            for k in getattr(self, field.name).keys():
                res += f'\u2022 #{str(k)}\n'
                for number, worker in enumerate(getattr(self, field.name)[k], start=1):
                    res += f'[{number}] {worker}\n'
        return res


class UserLevel(enum.IntEnum):
    """
    for now functions are not separated by user level
    """
    admin = 0
    user = 1


def init_bot_cfg(with_proxy: bool = None) -> Tuple[str, aiogram.client.session.aiohttp.AiohttpSession | None, int]:
    """
    Initializing bot config (bot token, session (with proxy or not))
    """
    cfg = ConfigParser()
    cfg.read('config.cfg')
    token = cfg['main']['token']
    admin = cfg['main']['admin']
    session = None
    if with_proxy:
        from aiogram.client.session.aiohttp import AiohttpSession
        proxy = cfg['main']['proxy']
        session = AiohttpSession(proxy=proxy)
    return token, session, int(admin)


def init_db_cfg() -> Tuple[str, str, str]:
    """
    Initializing database config (admin password, user password, database name)
    """
    cfg = ConfigParser()
    cfg.read('config.cfg')
    pswd_adm = cfg['database']['pswd_adm']
    pswd_usr = cfg['database']['pswd_usr']
    db_name = cfg['database']['name']
    return pswd_adm, pswd_usr, db_name


def sqlite_adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()


def get_user_day_shift(day: Dict, user) -> int:
    """
    Returns: current shift number of user if exists else 0
    """

    for shift in day.keys():
        if user in day[shift]:
            return shift
    return 0


def shift_update_msg() -> str:
    """
    adding datetime string for updated shift message to avoid aiogram.exceptions.TelegramBadRequest
    """
    return f'\n<i>Last update: {str(datetime.datetime.now())}</i>'


def get_week_number_from_message(text: str) -> int:
    pattern = r'Week #(\d*)'
    res = re.search(pattern, text)
    return int(res.group(1))
