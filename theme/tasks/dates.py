# coding=utf-8
"""
Created on 2020, September 3rd
@author: orion
"""
import pytz
from datetime import datetime, timezone, timedelta
from django.utils.timezone import now


def get_utc():
    return now()


def parse_date(str_date, str_time):

    try:
        year = int(str_date[0:4])
        month = int(str_date[5:7])
        day = int(str_date[8:10])

        hour = int(str_time[0:2])
        minute = int(str_time[3:5])
        second = int(str_time[6:8])
        microsecond = 0

        success = True

    except ValueError:
        success = False
        year = month = day = hour = minute = second = microsecond = 0

    return success, year, month, day, hour, minute, second, microsecond


def get_utc_from_locale(str_date, str_time, timezone_offset):
    success, year, month, day, hour, minute, second, microsecond = parse_date(str_date, str_time)
    if success:
        minutes = -timezone_offset
        locale_date = \
            datetime(year, month, day, hour, minute, second, microsecond, timezone(timedelta(minutes=minutes)))

        utc_date = locale_date.astimezone(pytz.utc)
    else:
        utc_date = get_utc()

    return utc_date


def get_utc_from_timezone(str_date, str_time, timezone):

    success, year, month, day, hour, minute, second, microsecond = parse_date(str_date, str_time)
    if success:
        naive_date = datetime(year, month, day, hour, minute, second, microsecond)
        locale_date = pytz.timezone(timezone).localize(naive_date, is_dst=None)
        utc_date = locale_date.astimezone(pytz.utc)
    else:
        utc_date = get_utc()

    return utc_date
