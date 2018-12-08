# -*- coding: utf-8 -*-

from enum import Enum

token = "700230860:AAEsixffAb5TLY_XasfUjOpKmmeBmdJy7Xw"
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = '0'  # Начало нового диалога
    S_WISH = '1'
    S_NOTIFICATIONS = '2'
    S_SIGHTS = '3'
    S_YESNO = '4'
    S_CHANGES = '5'
    S_YESNO_NOTIF = '6'
    S_NEW_START = '7'
