# coding=utf-8
"""
Created on 2020, December 6th
@author: orion
"""
import datetime

VERSION = "1.0"


def get_structure():
    return dict(
        begin=dict(
            date=datetime.datetime(2000, 1, 1, 0, 0),
            longitude=0.0,
            longitude_in_zodiac=0.0,
            zodiac="",
        ),
        end=dict(
            date=datetime.datetime(2000, 1, 1, 0, 0),
            longitude=0.0,
            longitude_in_zodiac=0.0,
            zodiac="",
        ),
    )
