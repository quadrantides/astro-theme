# coding=utf-8
"""
Created on 2020, April 12th
@author: orion
"""
import numpy

from transcend.constants import ZODIAC

VERSION = "1.0"

STRUCTURE = {

    'zodiac': {
        'angles': [],
        'labels': [],

    },
}


def get_default(zodiac_type="tropical", graphic_offset=180):
    if zodiac_type == "tropical":
        zodiac_offset = 0
    elif zodiac_type == "sidereal":
        zodiac_offset = 0
    else:
        zodiac_offset = 0
    offset = graphic_offset + zodiac_offset

    res = (offset + numpy.array([30 * i for i in range(12)])) % 360
    labels = numpy.array(
        ZODIAC,
    )
    sorted_indexes = numpy.argsort(res)

    return {'angles': res[sorted_indexes].tolist(), 'labels': labels[sorted_indexes].tolist()}
