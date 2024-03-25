# coding=utf-8
"""
Created on 2020, April 16th
@author: orion
"""
from transcend.constants import ZODIAC_COLORS
VERSION = "1.0"

blue = "#668cff"
green = "#33cc33"
brown = "#bf8040"
red = "#ff1a1a"

# ordre
# ['libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo']
COLORS = [
    brown,
    blue,
    red,
    green,
    brown,
    blue,
    red,
    green,
    brown,
    blue,
    red,
    green,
]

# COLORS = ZODIAC_COLORS


def get_domain(pie_width):

    domain_px = 1.0 - pie_width
    domain_dy = domain_px

    domain = {
        'x':
            [
                0 + domain_px / 2,
                1 - domain_px / 2,
            ],

        'y':
            [
                0 + domain_dy / 2,
                1 - domain_dy / 2,
            ],
    }
    return domain
